google.setOnLoadCallback(initChart);

var chart, data, form, formatter;
var options = {
    backgroundColor: "#eee",
    colorAxis: {
        colors: ["green", "yellow", "red"],
        maxValue: 100.0,
        minValue: 0.0
    }
};
var countries = [];

function min(vals) {
    if (vals.length > 0) {
        var m = vals[0];
        for (var i = 1; i < vals.length; i++)
            m = vals[i] < m ? vals[i] : m;
        return m;
    } else
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
    form = document.getElementById("form");
    formatter = new window.google.visualization.NumberFormat({fractionDigits: 0, suffix:"%"});

    data.addColumn("string", "Country");
    data.addColumn("number", "Resistance");
    data.addRows(geodata);

    drawChart([]);
};

function drawChart(abs) {
    if (typeof(abs) == "undefined") {
        abs = [];
        for (var i = 0; i < form.elements.length; i++)
            if (form.elements[i].type == "checkbox")
                if (form.elements[i].checked)
                    abs.push(form.elements[i].value);
    }
    for (var i = 0; i < countries.length; i++) {
        var vals = [];
        for (var j = 0; j < abs.length; j++)
            vals.push(countrydata[countries[i]][abs[j]]);
        data.setValue(i, 1, min(vals));
    }
    formatter.format(data, 1);
    chart.draw(data, options);
}

$(document).ready(function() {
    $("#selector").height($(window).height() - 102);

    var abset = {};
    for (var country in countrydata)
        for (var ab in countrydata[country])
            abset[ab] = 0;
    var antibodies = [];
    for (var ab in abset)
        if (ab !== "#")
            antibodies.push(ab);
    antibodies = antibodies.sort();
    delete abset;

    var checkboxes = [];
    for (var i = 0; i < antibodies.length; i++)
        checkboxes.push('<div class="antibody"><input type="checkbox" name="antibody" value="' + antibodies[i] + '" />' + antibodies[i] + '</div>');
    $("#form").html(checkboxes.join(""));

    $(".antibody > input").change(
        function() {
            drawChart();
        }
    ).click(
        function(ev) {
            ev.stopPropagation();
        }
    );

    $(".antibody").click(function() {
        var box = $(this).find(":checkbox");
        box.prop("checked", !box.is(":checked")).change();
    });

    $(window).resize(function() {
        $("#selector").height($(window).height() - 102);
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
