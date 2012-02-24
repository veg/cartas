google.setOnLoadCallback(initChart);

var chart, data, form, formatter;
var options = {
    backgroundColor: '#eee',
    colorAxis: {
        colors: ["green", "yellow", "red"],
        maxValue: 100.0,
        minValue: 0.0
    }
};
var countries = [];

function hmean(vals) {
    var r = 0;
    for (var i = 0; i < vals.length; i++) {
        if (vals[i] == 0)
            return 0;
        else
            r = r + ( 1.0 / vals[i] );
    }
    if (r > 0)
        return Math.round( vals.length / r );
    else
        return 0;
}

function initChart() {
    for (var country in countrydata)
        countries.push(country);

    var geodata = [];
    for (var i = 0; i < countries.length; i++)
        geodata.push([countries[i], 0]);

    chart = new window.google.visualization.GeoChart(document.getElementById("chart"));
    data = new window.google.visualization.DataTable();
    form = document.getElementById('form');
    formatter = new window.google.visualization.NumberFormat({fractionDigits: 0, suffix:"%"});

    data.addColumn("string", "Country");
    data.addColumn("number", "Resistance");
    data.addRows(geodata);

    drawChart([]);
};

function drawChart(abs) {
    for (var i = 0; i < countries.length; i++) {
        var vals = [];
        for (var j = 0; j < abs.length; j++)
            vals.push(countrydata[countries[i]][abs[j]]);
        data.setValue(i, 1, hmean(vals));
    }
    formatter.format(data, 1);
    chart.draw(data, options);
}

$(document).ready(function() {
    $('#selector').height($(window).height() - 102);

    var abset = {};
    for (var country in countrydata)
        for (var ab in countrydata[country])
            abset[ab] = 0;
    var antibodies = [];
    for (var ab in abset)
        if (ab !== '#')
            antibodies.push(ab);
    antibodies = antibodies.sort();
    delete abset;

    var checkboxes = [];
    for (var i = 0; i < antibodies.length; i++)
        checkboxes.push('<div><input class="antibody" type="checkbox" name="antibody" value="' + antibodies[i] + '" />' + antibodies[i] + '</div>');
    $("#form").html(checkboxes.join(""));

    $(".antibody").click(function() {
        var abs = [];
        for (var i = 0; i < form.elements.length; i++)
            if (form.elements[i].type == "checkbox")
                if (form.elements[i].checked == true)
                    abs.push(form.elements[i].value);
        drawChart(abs);
    });

    $(window).resize(function() {
        $('#selector').height($(window).height() - 102);
    });

    $("#clearall").click(function() {
        var clear = false;
        for (var i = 0; i < form.elements.length; i++)
            if (form.elements[i].type == "checkbox")
                if (form.elements[i].checked) {
                    clear = true;
                    form.elements[i].checked = false;
                }
        if (clear)
            drawChart([]);
    });
});
