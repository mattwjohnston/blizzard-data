//list of functions to call asap
window.onload = function start() {
    leaderboard();
}
var datas;
//calls the leaderboard route.  Anything that route's method returns, which be in the response.
function leaderboard() {
    d3.json('/leaderboard').then((data) => {
        console.log(data);
        datas = data;
         //this isn't right i was just seeing what pulls over to the html
         character(datas);
    });
}

//calls the api_connect route which connects to both parts of the API

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
             </div>`
        }
      )
      .attr("class", data => {return `${data.classId}`})
      .classed("col-md-4", true);
      
};