document.addEventListener('DOMContentLoaded', () => {

    // Populate content body with all calls

    populateBody()

    // Datetime Filter

    const datepicker = document.getElementById('datepicker')

    let startDate = getCookie('filterStartDate')
    let filterStartDate = undefined
    if (startDate != '') {
        console.log(startDate)
        filterStartDate = new Date(startDate)
    }
    let endDate = getCookie('filterEndDate')
    let filterEndDate = undefined
    if (endDate != '') {
        filterEndDate = new Date(endDate)
    }

    const picker = new easepick.create({
        element: datepicker,
        css: [
            'https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.0/dist/index.css',
        ],
        lang: 'pt-BR',
        plugins: ['RangePlugin', 'AmpPlugin'],
        RangePlugin: {
            startDate: filterStartDate,
            endDate: filterEndDate,
            locale: {
                one: 'dia',
                other: 'dias',
            },
        },
        AmpPlugin: {
            resetButton: true,
            darkMode: false,
            locale: {
                resetButton: 'Resetar'
            },
        },
        zIndex: 1000,
        autoApply: false,
        locale: {
            cancel: 'Cancelar',
            apply: 'Aplicar'
        },
        setup(picker) {
            picker.on('select', (e) => {
                startDate = picker.getStartDate().format('YYYY-MM-DD') + 'T00:00:01-0300';
                endDate = picker.getEndDate().format('YYYY-MM-DD') + 'T23:59:00-0300';
                document.cookie = `filterStartDate=${startDate}; path=/`;
                document.cookie = `filterEndDate=${endDate}; path=/`;
                clearBody()
                populateBody()
            });
            picker.on('clear', (e) => {
                document.cookie = `filterStartDate=${startDate}; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
                document.cookie = `filterEndDate=${endDate}; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
                clearBody()
                populateBody()
            });
        },
    });

    // Strategy Filter handler

    // Get all options of select
    const msOptions = document.querySelectorAll('.multi-select-option')
    var optionsList = [];
    msOptions.forEach(option => {
        optionsList.push(option.innerText)
    })

    // Every time the an option of the filter is clicked, filter the items
    var filteredStrats = []
    if (getCookie('filterStrategies') != '') {
        filteredStrats = getCookie('filterStrategies').split(',');
        $('.selectpicker').selectpicker('val', filteredStrats);
    }
    $('#strat-filter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
        filteredStrats = previousValue
        if (isSelected == true) {
            filteredStrats.push(optionsList[clickedIndex])
        } else {
            const index = filteredStrats.indexOf(optionsList[clickedIndex])
            if (index > -1) {
                filteredStrats.splice(index, 1)
            }
        }
        document.cookie = `filterStrategies=${filteredStrats}; path=/`
        clearBody()
        populateBody()
    });

})


function clearBody() {
    allCards = document.querySelectorAll('.strategy-card')
    allCards.forEach(card => {
        card.remove()
    })
}


function populateBody() {

    // Load fisrt calls
    let has_next = false

    fetch('calls/1')
    .then(response => response.json())
    .then(calls => {

        has_next = calls['has_next']

        calls['data'].forEach(call => {
            createCallCard(call)
        })

    })

    // Scroll tracker to load more calls

    let page_num = 2;
    document.onscroll = () => {

        // Only load when a next page exists and scrolled to bottom of page
        if (has_next && window.scrollY + window.innerHeight >= document.body.offsetHeight) {

            fetch(`calls/${page_num}`)
            .then(response => response.json())
            .then(calls => {

                has_next = calls['has_next']

                calls['data'].forEach(call => {
                    createCallCard(call)
                })

                page_num++;

            })

        }

    }
}


function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


function createCallCard(call) {

    // Creating general div

    const div = document.createElement('div')
    div.classList.add('strategy-card', 'col', 'mb-4', 'align-self-center')
    div.id = `fullcardof-${call['id']}`
    document.getElementById('row-main').appendChild(div)

    // Creating card div

    const divCard = document.createElement('div')
    divCard.classList.add('card')
    divCard.id = `cardof-${call['id']}`
    div.appendChild(divCard)

    // Creating and populating card header

    const divHeader = document.createElement('div')
    divHeader.classList.add('card-header', 'text-center')
    divHeader.id = `headerof-${call['id']}`
    divCard.appendChild(divHeader)

        // Header Badge

        const divBadge = document.createElement('div')
        divBadge.classList.add('strategy-badge')
        divHeader.appendChild(divBadge)

            // Badge Content

            const spanBadge = document.createElement('span')
            spanBadge.classList.add('strategy-badge-text')
            spanBadge.innerText = call['symbol']['ticker']
            divBadge.appendChild(spanBadge)

        // Strategy Type

        const spanType = document.createElement('span')
        spanType.classList.add('strategy-type')
        spanType.innerText = call['strategy']['stype']
        if (spanType.innerText === 'DT') {
            spanType.style.backgroundColor = 'salmon'
        } else {
            spanType.style.backgroundColor = '#87aeff'
        }
        divHeader.appendChild(spanType)

        // Strategy Name

        const spanName = document.createElement('span')
        spanName.classList.add('strategy-name')
        spanName.innerText = call['strategy']['name']
        divHeader.appendChild(spanName)

    // Creating and populating card body

    const divBody = document.createElement('div')
    divBody.classList.add('card-body')
    divBody.id = `bodyof-${call['id']}`
    divCard.appendChild(divBody)

        // Card Body Header

        const divBodyHeader = document.createElement('div')
        divBodyHeader.classList.add('body-header', 'row', 'align-items-center', 'mb-1')
        divBody.appendChild(divBodyHeader)

            // Call Date Time

            const divDateTime = document.createElement('div')
            divDateTime.classList.add('col-4', 'call-datetime')
            divBodyHeader.appendChild(divDateTime)

                const timeBR = new Date(call['timestamp']);

                const pDate = document.createElement('p')
                pDate.classList.add('call-date')
                pDate.innerText = timeBR.getDate() + '/' + (timeBR.getMonth() + 1) + '/' + timeBR.getFullYear()
                divDateTime.appendChild(pDate)

                const pTime = document.createElement('p')
                pTime.classList.add('call-time')
                pTime.innerText = `as ${timeBR.getHours() + ':' + timeBR.getMinutes()}`
                divDateTime.appendChild(pTime)
            
            // Separator Line

            const divLine = document.createElement('div')
            divLine.classList.add('col-4', 'justify-content-center', 'p-0', 'm-0')
            divBodyHeader.appendChild(divLine)

                const spanLine = document.createElement('p')
                spanLine.classList.add('call-header-line', 'm-0')
                divLine.appendChild(spanLine)
            
            // Call Direction

            const divDirection = document.createElement('div')
            divDirection.classList.add('col-4', 'call-direction')
            divDirection.innerText = call['direction']
            if (call['direction'] === 'Compra') {
                divDirection.style.color = 'rgb(48 171 57)'
            } else {
                divDirection.style.color = 'red'
            }
            divBodyHeader.appendChild(divDirection)
        
        // Call Result

        const divResult = document.createElement('div')
        divResult.classList.add('body-result', 'align-items-center')
        divBody.appendChild(divResult)

            const divResult2 = document.createElement('div')
            divResult2.classList.add('row', 'align-items-center')
            divResult.appendChild(divResult2)

                const pToolTip = document.createElement('p')
                pToolTip.classList.add('col-5', 'm-0', 'p-0')
                pToolTip.innerText = 'Resultado:'
                divResult2.appendChild(pToolTip)

                const pResult = document.createElement('p')
                pResult.classList.add('col', 'm-0', 'p-0', 'text-right')
                let resultInnerText = ''
                if (call['trade_status'] == 'open') {
                    resultInnerText = 'Trade Aberto'
                } else if (call['trade_status'] == 'closed') {
                    if (call['result'] > 0) {
                        resultInnerText = 'Gain de '
                    } else if (call['result'] < 0) {
                        resultInnerText = 'Loss de '
                    } else {
                        resultInnerText = 'Breakeven'
                    }
                    if (resultInnerText != 'Breakeven') {
                        let result = call['result']
                        if (call['symbol']['denomination'] == '%') {
                            result = 100 * call['result'] / call['entry']
                        }
                        result = result.toLocaleString('pt-BR', {maximumFractionDigits: call['symbol']['decimal_places']}) + ' ' + call['symbol']['denomination']
                        resultInnerText = resultInnerText + result
                    }
                }
                pResult.innerText = resultInnerText
                divResult2.appendChild(pResult)

        // Call Description

        const divBodyDesc = document.createElement('div')
        divBodyDesc.classList.add('body-desc', 'mb-3')
        if (call['comment']) {
            divBodyDesc.innerText = '...'
            //divBodyDesc.innerText = call['comment']
        } else {
            divBodyDesc.innerText = '...'
        }
        divBody.appendChild(divBodyDesc)

        // Call per se

        const divBodyCall = document.createElement('div')
        divBodyCall.classList.add('body-call')
        divBody.appendChild(divBodyCall)

            // Formatting the prices

            localeOptions = {
                minimunFractionDigits: call['symbol']['decimal_places'],
                maximumFractionDigits: call['symbol']['decimal_places'],
            }

            let entryPrice = call['entry'].toLocaleString('pt-BR', localeOptions)
            let targetPrice = call['target'].toLocaleString('pt-BR', localeOptions)
            let stopPrice = call['stop'].toLocaleString('pt-BR', localeOptions)
            const callPrices = [entryPrice, targetPrice, stopPrice]
            
            if (call['symbol']['decimal_places'] > 0) {
                for (i in callPrices) {
                    const temp = callPrices[i].split(',')
                    if (temp[1] == undefined) {
                        temp[1] = String('0' * call['symbol']['decimal_places'])
                    }
                    temp[1] = temp[1].padEnd(call['symbol']['decimal_places'], '0')
                    
                    callPrices[i] = call['symbol']['prefix'] + temp[0] + ',' + temp[1]
                }
            }

            // Entry price

            const divEntry = document.createElement('div')
            divEntry.classList.add('row', 'call-entry')
            divBodyCall.appendChild(divEntry)

                const divEntryTip = document.createElement('div')
                divEntryTip.classList.add('col-5')
                divEntryTip.innerText = 'Entrada'
                divEntry.appendChild(divEntryTip)

                const divEntryPrice = document.createElement('div')
                divEntryPrice.classList.add('col', 'text-center')
                divEntryPrice.innerText = callPrices[0]
                divEntry.appendChild(divEntryPrice)

            // Target

            const divTarget = document.createElement('div')
            divTarget.classList.add('row', 'call-target')
            divBodyCall.appendChild(divTarget)

                const divTargetTip = document.createElement('div')
                divTargetTip.classList.add('col-4')
                divTargetTip.innerText = 'Alvo'
                divTarget.appendChild(divTargetTip)

                const spanTargetDisplay = document.createElement('span')
                spanTargetDisplay.classList.add('toggle-target-display', 'col-1', 'text-center', 'p-0')
                spanTargetDisplay.innerText = '$'
                divTarget.appendChild(spanTargetDisplay)

                const divTargetPrice = document.createElement('div')
                divTargetPrice.classList.add('col', 'text-center')
                divTargetPrice.innerText = callPrices[1]
                divTarget.appendChild(divTargetPrice)

                spanTargetDisplay.onclick = () => {
                    if (spanTargetDisplay.innerText == '$') {
                        spanTargetDisplay.innerText = '⇅';
                        let price = Math.abs(call['target'] - call['entry']).toLocaleString('pt-BR', localeOptions)
                        const temp = price.split(',')
                        if (temp[1] == undefined) {
                            temp[1] = String('0' * call['symbol']['decimal_places'])
                        }
                        temp[1] = temp[1].padEnd(call['symbol']['decimal_places'], '0')
                        price = call['symbol']['prefix'] + temp[0] + ',' + temp[1]
                        divTargetPrice.innerText = price
                    }
                    else if (spanTargetDisplay.innerText == '⇅') {
                        spanTargetDisplay.innerText = '%';
                        let price = (100 * Math.abs(call['target'] - call['entry']) / call['entry']).toLocaleString('pt-BR', {maximumFractionDigits: 2})
                        divTargetPrice.innerText = price + '%'
                    }
                    else if (spanTargetDisplay.innerText == '%') {
                        spanTargetDisplay.innerText = '$';
                        divTargetPrice.innerText = callPrices[1]
                    }
                }

            // Stop

            const divStop = document.createElement('div')
            divStop.classList.add('row', 'call-stop')
            divBodyCall.appendChild(divStop)

                const divStopTip = document.createElement('div')
                divStopTip.classList.add('col-4')
                divStopTip.innerText = 'Stop'
                divStop.appendChild(divStopTip)

                const spanStopDisplay = document.createElement('span')
                spanStopDisplay.classList.add('toggle-stop-display', 'col-1', 'text-center', 'p-0')
                spanStopDisplay.innerText = '$'
                divStop.appendChild(spanStopDisplay)

                const divStopPrice = document.createElement('div')
                divStopPrice.classList.add('col', 'text-center')
                divStopPrice.innerText = callPrices[2]
                divStop.appendChild(divStopPrice)

                spanStopDisplay.onclick = () => {
                    if (spanStopDisplay.innerText == '$') {
                        spanStopDisplay.innerText = '⇅';
                        let price = Math.abs(call['stop'] - call['entry']).toLocaleString('pt-BR', localeOptions)
                        const temp = price.split(',')
                        if (temp[1] == undefined) {
                            temp[1] = String('0' * call['symbol']['decimal_places'])
                        }
                        temp[1] = temp[1].padEnd(call['symbol']['decimal_places'], '0')
                        price = call['symbol']['prefix'] + temp[0] + ',' + temp[1]
                        divStopPrice.innerText = price
                    }
                    else if (spanStopDisplay.innerText == '⇅') {
                        spanStopDisplay.innerText = '%';
                        let price = (100 * Math.abs(call['stop'] - call['entry']) / call['entry']).toLocaleString('pt-BR', {maximumFractionDigits: 2})
                        divStopPrice.innerText = price + '%'
                    }
                    else if (spanStopDisplay.innerText == '%') {
                        spanStopDisplay.innerText = '$';
                        divStopPrice.innerText = callPrices[2]
                    }
                }

}
