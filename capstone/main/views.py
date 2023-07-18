from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Strategy, StrategyStat, StrategyParam, Symbol, StrategyCall
from .forms import UserRegisterForm
import json
import csv
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


@login_required
def home(request):
    all_strategies = Strategy.objects.order_by("name").all()
    return render(request, "main/index.html", {
        'strategies': all_strategies
    })


@login_required
def calls(request, page_id):
    all_calls = StrategyCall.objects.order_by("-timestamp").all()

    # Datetime filter
    try:
        start_date = request.COOKIES['filterStartDate']
        end_date = request.COOKIES['filterEndDate']
        all_calls = all_calls.order_by("-timestamp").filter(timestamp__lte=end_date, timestamp__gte=start_date)
    except KeyError:
        pass

    # Strategies Filter
    try:
        strategies_filtered = request.COOKIES['filterStrategies'].split(',')
        if strategies_filtered[0] != '':
            all_calls = all_calls.order_by("-timestamp").filter(strategy__name__in=strategies_filtered)
    except KeyError:
        pass

    calls = [call.serialize() for call in all_calls]

    paginator = Paginator(calls, 20)
    if page_id not in paginator.page_range:
        page_obj = None
        return JsonResponse(page_obj, safe=False, status=400)

    page_obj = paginator.get_page(page_id)

    return JsonResponse({
        "has_previous": page_obj.has_previous(),
        "data": list(page_obj),
        "has_next": page_obj.has_next(),
    })


@csrf_exempt
def calls_api(request):

    call = {
        'symbol': 'WIN1!',
        'strategy': 'HANCOCK',
        'direction': 'buy',
        'market_position': 'long',
        'prev_market_position': 'flat',
        'comment': '',
        'order_price': 104000,
        'target_price': 105000,
        'stop_price': 104500,
    }

    strategy, strategy_created = Strategy.objects.get_or_create(
        key=call['strategy'],
        defaults={
            'name': call['strategy'].replace('_', ' ').title(),
            'stype': 'DT',
        },
    )

    if strategy_created:
        StrategyParam.objects.create(
            strategy=strategy,
            calls_currency='BRL',
        )

    symbol, symbol_created = Symbol.objects.get_or_create(
        ticker=call['symbol'],
        defaults={
            'name': call['symbol'],
        },
    )

    try:
        last_call = StrategyCall.objects.filter(strategy=strategy,symbol=symbol).latest('id')
    except ObjectDoesNotExist:
        last_call = 'first_trade'

    # Entrying trade
    if call['prev_market_position'] == 'flat' and call['market_position'] != 'flat':

        if last_call == 'first_trade':
            pass
        elif last_call.trade_status == 'open':
            return JsonResponse({
                'status': 'trade already open'
            })

        new_call = StrategyCall(
            strategy = strategy,
            symbol = symbol,
            direction = call['direction'].capitalize(),
            entry_price = call['order_price'],
            target_price = call['target_price'],
            stop_price = call['stop_price'],
            comment = call['comment'],
            trade_status = 'open',
            result = 0,
        )

        new_call.save()

        return JsonResponse({
            'status': 'trade entry'
        })

    # Closing trade
    elif call['prev_market_position'] != 'flat' and call['market_position'] == 'flat':

        if last_call.trade_status != 'open':
            return JsonResponse({
                'status': f'trade {last_call.trade_status}'
            })

        if call['direction'] == 'buy' and last_call.direction == 'Sell':
            result = (call['order_price'] - last_call.entry_price) * (-1)
        elif call['direction'] == 'sell' and last_call.direction == 'Buy':
            result = (call['order_price'] - last_call.entry_price)
        else:
            return JsonResponse({
                'status': 'invalid call'
            })

        last_call.result = result
        last_call.trade_status = 'closed'
        last_call.save()

        return JsonResponse({
            'status': last_call.result
        })

    # Other trade types
    else:
        return JsonResponse({
            'status': 'trade not supported'
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("main_home")
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")


def logout_view(request):
    logout(request)
    return redirect("main_home")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main_home")

    else:
        form = UserRegisterForm()
    return render(request, "main/register.html", {
        'form': form
    })
