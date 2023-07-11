from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='main_home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    #path('create_strategies', views.import_calls, name='import_calls'),

    # API
    path('calls/<int:page_id>', views.calls, name='calls'),
    path('new_call', views.calls_api, name='calls_api'),
]
