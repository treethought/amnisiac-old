// # js for creating youtube play buttons from invisible video player
// $( document ).ready(function() {




function onYouTubeIframeAPIReady() {

    console.log('In youtubeready');

    var playerItems = document.getElementsByClassName('youtube-item');

    Array.from(playerItems).forEach( function(elem, i) {
        // statements
   
    // for (var i = 0; i < playerItems.length; i++) {
        // var elem = playerItems[i];
        console.log('Working on ' + elem.id)

        var icon = document.createElement("img");
        icon.setAttribute("id", "youtube-icon" + i);
        icon.setAttribute("src", "https://i.imgur.com/" + 'IDzX9gL.png');

        icon.style.cssText = "cursor:pointer;cursor:hand";
        icon.style.height = '50px';
        icon.style.width = '50px';
        icon.setAttribute('class', "img-responsive")
        elem.appendChild(icon);
        console.log(elem.getElementsByTagName('img'));


        var div = document.createElement("div");
        div.setAttribute("id", "youtube-player-"+ elem.id);
        elem.appendChild(div);
        console.log('Added player div to the element');

        var divImg = elem.getElementsByTagName('img')

        var toggleButon = function(e) {
        var iconSource = e ? "IDzX9gL.png" : "quyUPXN.png";

        icon.setAttribute("src", "https://i.imgur.com/" + iconSource);
        };
        console.log('Added iconSource to player');

        elem.onclick = function() {
        if (player.getPlayerState() === YT.PlayerState.PLAYING
            || player.getPlayerState() === YT.PlayerState.BUFFERING) {

            player.pauseVideo();
            toggleButon(false);
        }
        else {
            player.playVideo();
            toggleButon(true);
        }
    };

        var player = new YT.Player("youtube-player-"+ elem.id, {
        height: "0",
        width: "0",
        videoId: elem.dataset.video,
        playerVars: {
            autoplay: elem.dataset.autoplay,
            loop: elem.dataset.loop
        },
        events: {
            onReady: function(e) {
                e.target.setPlaybackQuality("small");
                toggleButon(e.target.getPlayerState() !== YT.PlayerState.CUED);
            },
            onStateChange: function(e) {
                if (e.data === YT.PlayerState.ENDED) {
                    toggleButon(false);
                  }

              }
          }
      });


    

     });

}

// });


//     'use strict';
//     console.log('working on ' + elemID);
//     var e = document.getElementById(elemID);
//     var t = document.createElement("img");
//     t.setAttribute("id", "youtube-icon");
//     t.style.cssText = "cursor:pointer;cursor:hand";
//     e.appendChild(t);

//     var div = document.createElement("div");
//     div.setAttribute("id", "youtube-player");
//     e.appendChild(div);


//     var toggleButon = function(e) {
//         var img = e ? "IDzX9gL.png" : "quyUPXN.png";
//         t.setAttribute("src", "https://i.imgur.com/" + img);
//     };

//     e.onclick = function() {
//         if (player.getPlayerState() === YT.PlayerState.PLAYING
//             || player.getPlayerState() === YT.PlayerState.BUFFERING) {

//             player.pauseVideo();
//             toggleButon(false);
//         }
//         else {
//             player.playVideo();
//             toggleButon(true);
//         }
//     };



//     var r = new YT.Player("youtube-player", {
//         height: "10",
//         width: "10",
//         videoId: e.dataset.video,
//         playerVars: {
//             autoplay: e.dataset.autoplay,
//             loop: e.dataset.loop
//         },
//         events: {
//             onReady: function(e) {
//                 r.setPlaybackQuality("small");
//                 toggleButon(r.getPlayerState() !== YT.PlayerState.CUED);
//             },
//             onStateChange: function(e) {
//                 if (e.data === YT.PlayerState.ENDED) {
//                     toggleButon(false);
//                 }

//             }
//         }
//     });
// }
// var $ = jQuery;
// $(document).ready(function() {
//     'use strict';



// console.log('starting yotube.js');







//     console.log('Selecting elements');
//     var elements = document.getElementsByClassName("youtube-item");
//     console.log('elements are ' + elements);

//     for (var i = 0; i < elements.length; i++) {
//         console.log('calling func for ' + elements.id);
//         onYouTubeIframeAPIReady(elements[i].id);
//     }
// });















