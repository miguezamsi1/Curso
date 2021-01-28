// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player1;
var player2;

// 4. The API will call this function when the video player is ready.
function onPlayerReady1(event) {
    //event.target.playVideo();
    console.log("VIDEO READY 1");
    player1.addEventListener('onStateChange', onPlayerStateChange1);
}
function onPlayerReady2(event) {
    //event.target.playVideo();
    console.log("VIDEO READY 2");
    player2.addEventListener('onStateChange', onPlayerStateChange2);
}

function onPlayerError1(event){
    console.log("ERROR PLAYER 1 : " + event.data);
}
function onPlayerError2(event){
    console.log("ERROR PLAYER 2 : " + event.data);
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done1 = false;
function onPlayerStateChange1(event) {
    console.log("Video STATE 1 CHANGE :: " + event.data);
    $('#videos-carousel').carousel('pause');
    //console.log("PLAYER CHANGE 1" + event);
    if (event.data == YT.PlayerState.PLAYING) {
        //setTimeout(stopVideo1, 6000);
        //$('#videos-carousel').carousel('pause');
        //console.log("VIDEO  1 PLAYING");
        done1 = false;
    }
}


var done2 = false;
function onPlayerStateChange2(event) {
    console.log("Video STATE 1 CHANGE :: " + event.data);
    $('#videos-carousel').carousel('pause');
    //console.log("PLAYER CHANGE 2" + event);
    //console.log("VIDEO  2 PLAYING");
    if (event.data == YT.PlayerState.PLAYING) {
        //setTimeout(stopVideo2, 6000);
        //$('#videos-carousel').carousel('pause');
        //console.log("VIDEO  2 PLAYING");
        done2 = false;
    }
}

function stopVideo1() {
    player1.stopVideo();
}

function stopVideo2() {
    player2.stopVideo();
}
      