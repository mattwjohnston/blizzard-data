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

function character(datas) {
    console.log('Character function');
     d3.select("#test2")
       .selectAll(".bio")
       .data(datas)
       .enter()
       .append(`div`)
       .html(data => { return `<h4 class="ranking"><strong>Rank ${data.ranking}</strong></h4><h4 class="rating" style="margin-left:10px"><strong> Rating ${data.rating}</strong></h4><br>
             <div class="row">
              <img src="/static/Resources/Class/${data.classId}.jpg" width="30" height="30"></img>
              <img src="/static/Resources/specialization/${data.classId}/${data.specId}.jpg" width="30" height="30"></img>
              <a href="https://worldofwarcraft.com/en-us/character/us/${data.realmSlug}/${data.name}" style="text-decoration: underline;color:black" target="_blank" rel="nofollow">${data.name} </a>
              <p style="margin-left:10px">${data.tier} Tier</><img src="/static/Resources/tier/${data.tier}.png" width="30" height="30"></img>
              </div>
              <div class="row">
              <img src="/static/Resources/faction/${data.factionId}.jpg" width="30" height="30"></img>
              <p>Wins:${data.seasonWins} Played:${data.seasonWins + data.seasonLosses}</p>
              </div>`})
       .attr("class", data => {return `${data.classId}`})
       .classed("col-md-4", true);
 }


function piechart() {
    const keys = Array();
    const values = Array();

    $.getJSON('/filter', {allclasses:'allclasses'}, function( data ) {
        $.each( data, function( key, val ) {
            keys.push(key);
            values.push(val);
        });
        data1 = [{
            values: values.valueOf(),
            labels: keys.valueOf(),
            type: "pie"
        }];
        layout1 = {
            title: "Character Class Breakdown",
            autosize:true,
            visible:true,
            showlegend:true,
            bgcolor:"rgb(41, 41, 41)",
            responsive: true
        };
        Plotly.newPlot("pie", data1, layout1);
    });
    
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