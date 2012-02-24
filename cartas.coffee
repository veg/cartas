
chart = data = form = formatter = null
options =
    backgroundColor: '#eee',
    colorAxis:
        colors: ['green', 'yellow', 'red'],
        maxValue: 100.0,
        minValue: 0.0

countries = []

min = (vals) ->
    if vals.length > 0
        vals.reduce( ((a, b) -> if b < a then b else a), 100 )
    else
        0

drawChart = (abs) ->
    if not abs?
        abs = (element.value for element in form when element.type == 'checkbox' and element.checked)

    for i in [0...countries.length]
        vals = (countrydata[countries[i]][ab] for ab in abs)
        data.setValue(i, 1, min vals)

    formatter.format(data, 1)
    chart.draw(data, options)


google.setOnLoadCallback ->
    countries = (country for country of countrydata)

    chart = new window.google.visualization.GeoChart (document.getElementById 'chart')
    data = new window.google.visualization.DataTable()
    form = document.getElementById 'form'
    formatter = new window.google.visualization.NumberFormat {fractionDigits: 0, suffix:'%'}

    data.addColumn('string', 'Country')
    data.addColumn('number', 'Resistant')
    data.addRows(([country, 0] for country in countries))

    drawChart []

    $('#selector').height ($(window).height() - 102)
    $(window).resize -> $('#selector').height ($(window).height() - 102)

    abset = {}
    for country of countrydata
        for ab of countrydata[country]
            abset[ab] = 0
    antibodies = (ab for ab of abset when ab != '#').sort()
    delete abset

    $('#form').html( ("<div class='antibody'><input type='checkbox' name='antibody' value='#{ab}'/>#{ab}</div>" for ab in antibodies).join('') )

    $('.antibody > input').change( -> drawChart() ).click( (ev) -> ev.stopPropagation() )

    $('.antibody').click ->
        box = $(this).find ':checkbox'
        box.prop( 'checked', not box.is ':checked' ).change()

    $('#clearall').click ->
        clear = false
        for element in form.elements
            if element.type == 'checkbox' and element.checked
                clear = true
                element.checked = false
        if clear
            drawChart []
