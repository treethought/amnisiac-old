// # js for creating youtube play buttons from invisible video player
// $( document ).ready(function() {




function onYouTubeIframeAPIReady() {

    console.log('In youtubeready');

    var playerItems = document.getElementsByClassName('youtube-item');

    Array.from(playerItems).forEach( function(elem, i) {
        // statements
   
    // for (var i = 0; i < playerItems.length; i++) {
        // var elem = playerItems[i];
        console.log('Working on ' + i)

        var icon = document.createElement("img");
        icon.setAttribute("id", "youtube-icon-" + i);
        icon.setAttribute("src", "https://i.imgur.com/" + 'IDzX9gL.png');

        icon.style.cssText = "cursor:pointer;cursor:hand";
        icon.style.height = '50px';
        icon.style.width = '50px';
        icon.setAttribute('class', "img-responsive")
        elem.appendChild(icon);
        console.log(elem.getElementsByTagName('img'));


        var div = document.createElement("div");
        div.setAttribute("id", "youtube-player-"+ i);
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

        // var play_next = function () {
        //     var nextId = 'youtube-player-' + (i+1);
        //     console.log('trying to play ' + nextId)
        //     // callPlayer(nextId, 'PlayVideo');

        //     var nextElem = document.getElementById(nextId);
        //     nextElem.style.background = 'red';


        //     var nextPlayer = new YT.Player(nextId, {});
        //     nextPlayer.playVideo();
        // };

        
            

        var player = new YT.Player("youtube-player-"+ i, {
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





/**
 * @author       Rob W <gwnRob@gmail.com>
 * @website      http://stackoverflow.com/a/7513356/938089
 * @version      20131010
 * @description  Executes function on a framed YouTube video (see website link)
 *               For a full list of possible functions, see:
 *               https://developers.google.com/youtube/js_api_reference
 * @param String frame_id The id of (the div containing) the frame
 * @param String func     Desired function to call, eg. "playVideo"
 *        (Function)      Function to call when the player is ready.
 * @param Array  args     (optional) List of arguments to pass to function func*/
function callPlayer(frame_id, func, args) {
    console.log('calling player')
    if (window.jQuery && frame_id instanceof jQuery) frame_id = frame_id.get(0).id;
    var iframe = document.getElementById(frame_id);
    if (iframe && iframe.tagName.toUpperCase() != 'IFRAME') {
        iframe = iframe.getElementsByTagName('iframe')[0];
    }

    // When the player is not ready yet, add the event to a queue
    // Each frame_id is associated with an own queue.
    // Each queue has three possible states:
    //  undefined = uninitialised / array = queue / 0 = ready
    if (!callPlayer.queue) callPlayer.queue = {};
    var queue = callPlayer.queue[frame_id],
        domReady = document.readyState == 'complete';

    if (domReady && !iframe) {
        // DOM is ready and iframe does not exist. Log a message
        window.console && console.log('callPlayer: Frame not found; id=' + frame_id);
        if (queue) clearInterval(queue.poller);
    } else if (func === 'listening') {
        // Sending the "listener" message to the frame, to request status updates
        if (iframe && iframe.contentWindow) {
            func = '{"event":"listening","id":' + JSON.stringify(''+frame_id) + '}';
            iframe.contentWindow.postMessage(func, '*');
        }
    } else if (!domReady ||
               iframe && (!iframe.contentWindow || queue && !queue.ready) ||
               (!queue || !queue.ready) && typeof func === 'function') {
        if (!queue) queue = callPlayer.queue[frame_id] = [];
        queue.push([func, args]);
        if (!('poller' in queue)) {
            // keep polling until the document and frame is ready
            queue.poller = setInterval(function() {
                callPlayer(frame_id, 'listening');
            }, 250);
            // Add a global "message" event listener, to catch status updates:
            messageEvent(1, function runOnceReady(e) {
                if (!iframe) {
                    iframe = document.getElementById(frame_id);
                    if (!iframe) return;
                    if (iframe.tagName.toUpperCase() != 'IFRAME') {
                        iframe = iframe.getElementsByTagName('iframe')[0];
                        if (!iframe) return;
                    }
                }
                if (e.source === iframe.contentWindow) {
                    // Assume that the player is ready if we receive a
                    // message from the iframe
                    clearInterval(queue.poller);
                    queue.ready = true;
                    messageEvent(0, runOnceReady);
                    // .. and release the queue:
                    while (tmp = queue.shift()) {
                        callPlayer(frame_id, tmp[0], tmp[1]);
                    }
                }
            }, false);
        }
    } else if (iframe && iframe.contentWindow) {
        // When a function is supplied, just call it (like "onYouTubePlayerReady")
        if (func.call) return func();
        // Frame exists, send message
        iframe.contentWindow.postMessage(JSON.stringify({
            "event": "command",
            "func": func,
            "args": args || [],
            "id": frame_id
        }), "*");
    }
    /* IE8 does not support addEventListener... */
    function messageEvent(add, listener) {
        var w3 = add ? window.addEventListener : window.removeEventListener;
        w3 ?
            w3('message', listener, !1)
        :
            (add ? window.attachEvent : window.detachEvent)('onmessage', listener);
    }
}