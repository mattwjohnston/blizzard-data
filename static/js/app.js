//list of functions to call asap
window.onload = function start() {
    blizzard_connection();
    leaderboard();
}

//calls the leaderboard route.  Anything that route's method returns, which be in the response.
function leaderboard() {
    d3.json('/leaderboard').then((response) => response.json()).then((data) => {
        console.log(data);
        document.getElementById('leaderboard').value = data; //this isn't right i was just seeing what pulls over to the html
    });
}

//calls the api_connect route which connects to both parts of the API
function blizzard_connection() {
    d3.json('/api_connect').then((response) => response.json()).then((messages) => {console.log("messages")});
}