//list of functions to call asap
window.onload = function start() {
    blizzard_connection();
    leaderboard();
};
datas = {}

function leaderboard() {
    d3.json('/leaderboard').then((data) => {
        datas+=data;
        characters(datas);
    });
};



$('#classfilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {classfilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
    })});      
$('#racefilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {racefilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
    })});   
$('#specfilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    $.getJSON('/filter', {specfilter:$(this).val()}, function(data) {
        document.getElementById("filtertest").innerHTML = data;
    })});      

//calls the api_connect route which connects to both parts of the API
function blizzard_connection() {
    d3.json('/api_connect').then((response) => response.json()).then((messages) => {console.log("messages")});
};

function characters(data) {
    document.getElementById("leaderboard").innerHTML = data;
    $('.spinner-border').hide();
};