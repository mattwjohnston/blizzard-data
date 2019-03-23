//list of functions to call asap
window.onload = function start() {
    leaderboard();
}
datas = {};
function leaderboard() {
    d3.json('/leaderboard').then((data) => {
        datas+=data;
        characters(datas);
        piechart();
    });
}

function piechart() {
    const keys = Array();
    const values = Array();

    $.getJSON('/filter', {allclasses:'allclasses'}, function( data ) {
        $.each( data, function( key, val ) {
            keys.push(key);
            values.push(val);
        });
    
    });

  //  [1:]
    var layout = {
        title: "Character Class Breakdown",
        autosize:true,
        paper_bgcolor:'#7f7f7f',
        plot_bgcolor: '#c7c7c7',
        margin: {
            l: 50,
            r: 20,
            b: 50,
            t: 50,
            pad: 10
          }
    };
    var data = [{
        values: values.valueOf(),
        labels: keys.valueOf(),
        type: "pie",
        visible: true
    }]; 
    Plotly.newPlot("pie", data, layout, {responsive: true});
}
  
function updatePlotly(newdata) {
    var PIE = document.getElementById("pie");
    Plotly.restyle(PIE, "values", [newdata]);
}
  
function changeData(classfilter) {
    dataset = $.getJSON('/filter', {classfilter:classfilter}, (data) => {return(data)});
    updatePlotly(dataset);
}
  

$('#classfilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {classfilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
        changeData($('#classfilter').val());
    })});      
$('#racefilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {racefilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
    })});   
$('#specfilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {specfilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
    })});      

function characters(data) {
    document.getElementById("leaderboard").innerHTML = data;
    $('.spinner-border').hide();
};