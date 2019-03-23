//list of functions to call asap
window.onload = function start() {
    leaderboard();
    
}
var datas;
function leaderboard() {
    d3.json('/leaderboard').then((data) => {
        piechart();
        datas=data;
        character(datas);
        characterfull(datas);
    });
}

function character(datas) {
    console.log('Character function');
     d3.select("#charactersection")
       .selectAll(".bio")
       .data(datas)
       .enter()
       .append(`div`)
       .html(data => { return `<h4 class="ranking"><strong>Rank ${data.ranking}</strong></h4><h4 class="rating" style="margin-left:10px"><strong> Rating ${data.rating}</strong></h4><br>
             <div class="row" style="margin-left:20px">
              <img src="/static/Resources/Class/${data.classId}.jpg" width="30" height="30"></img>
              <img src="/static/Resources/Specialization/${data.classId}/${data.specId.toLowerCase()}.jpg" width="30" height="30"></img>
              <a href="https://worldofwarcraft.com/en-us/character/us/${data.realmSlug}/${data.name}" style="text-decoration: underline;color:black" target="_blank" rel="nofollow">${data.name} </a>
              <p style="margin-left:10px; color:black">${data.tier} Tier</><img src="/static/Resources/tier/${data.tier}.png" width="30" height="30"></img>
              </div>
              <div class="row" style="margin-left:20px">
              <img src="/static/Resources/faction/${data.factionId}.jpg" width="30" height="30"></img>
              <p style="color:black">Wins:${data.seasonWins} Played:${data.seasonWins + data.seasonLosses}</p>
              </div>`
         }
       )
       .attr("class", data => {return `${data.classId}`});
 }

 function characterfull(datas) {
    console.log('Character function');
    d3.select("#test2")
    .selectAll(".bio")
    .data(datas)
    .enter()
    .append(`div`)
    .html(data => { return `<h4 class="ranking"><strong>Rank ${data.ranking}</strong></h4><h4 class="rating" style="margin-left:10px"><strong> Rating ${data.rating}</strong></h4><br>
          <div class="row" style="margin-left:20px">
           <img src="/static/Resources/Class/${data.classId}.jpg" width="30" height="30"></img>
           <img src="/static/Resources/Specialization/${data.classId}/${data.specId.toLowerCase()}.jpg" width="30" height="30"></img>
           <a href="https://worldofwarcraft.com/en-us/character/us/${data.realmSlug}/${data.name}" style="text-decoration: underline;color:black" target="_blank" rel="nofollow">${data.name} </a>
           <p style="margin-left:10px; color:black">${data.tier} Tier</><img src="/static/Resources/tier/${data.tier}.png" width="30" height="30"></img>
           </div>
           <div class="row" style="margin-left:20px">
           <img src="/static/Resources/faction/${data.factionId}.jpg" width="30" height="30"></img>
           <p style="color:black">Wins:${data.seasonWins} Played:${data.seasonWins + data.seasonLosses}</p>
           </div>`
      }
    )
    .attr("class", data => {return `${data.classId}`})
    .classed("col-md-4", true);    
 };

function piechart(classname='allclasses') {
    keys = Array();
    values = Array();
    $.getJSON('/filter', {classfilter:classname}, function( data ) {
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
            visible:true,
            showlegend:true,
            responsive: true,
            paper_bgcolor:'#272B30',
            font: {
                color: "#ffffff"
            },
            margin: {
                t:10, 
                l:0,
                r:0,
                b:10,
                pad:0}
        };
        $('.spinner-border').hide()
        Plotly.newPlot("pie", data1, layout1);
        $('.card').show()
    });
    
}  

$('#classfilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    piechart($(this).val())});
  /*  $.getJSON('/filter', {classfilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
        changeData(data);
    })});    */  

$('#racefilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {racefilter:$(this).val()}, function(data) {
        console.log(data);
    })});   

$('#specfilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {specfilter:$(this).val()}, function(data) {
        console.log(data);
    })});      
