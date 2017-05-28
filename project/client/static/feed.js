// Feed Table 

var postItems = document.getElementsByClassName('post-item');


var removeHighights = function() {
    console.log('removing highlights');
    for (var i = postItems.length - 1; i >= 0; i--) {
        postItems[i].parentNode.classList.remove('active');
        toggleButon(false, i);
    }
}

var highlightRow = function(elem, i) {
    console.log('clicked icon for elem ' + i);
    removeHighights();
    elem.parentNode.classList.add('active');
    toggleButon(true, i);

}

var toggleButon = function(playing, i) {
    var iconSource = playing ? "IDzX9gL.png" : "quyUPXN.png"; // if playing set pause symbol, else set play symbol

    icon = document.getElementById("post-icon-" + i);

    icon.setAttribute("src", "https://i.imgur.com/" + iconSource);
};

var startNext = function(i) {

    console.log('in start next')


    for (var next = i + 1; next < postItems.length; next++) {
        console.log('checking if ' + next + 'is visible')

        var item = $('#post-icon-' + next);

        if (item.is(':visible')) {
            item.click();
            break;
        }

    }
};

Array.from(postItems).forEach(function(elem, i) {

    // Render Icon
    var icon = document.createElement("img");
    icon.setAttribute("id", "post-icon-" + i);
    icon.setAttribute("class", 'icon img-responsive');
    icon.setAttribute("src", "https://i.imgur.com/" + "quyUPXN.png");

    icon.style.cssText = "cursor:pointer;cursor:hand";
    icon.style.height = '50px';
    icon.style.width = '50px';

    elem.appendChild(icon);

    icon.addEventListener('click', function() {
        highlightRow(elem, i);
    })


    elem.addEventListener('click', function() {
        console.log('clicked post ' + i);

        // highlightRow(i);

        if (elem.className.includes('reddit')) {
            console.log('Reddit: yt_id: ' + elem.id);
            clickYT(elem, i);
        } else {
            console.log('Soundcloud: sc_id: ' + elem.id);
            clickSC(elem, i);
        }

        $('#now-playing-display').show('slow');
        $('#toggle-player').show('slow');

    })

})


//////////////
// Youtube //
/////////////

var player = null;

var removeYT = function() {
    if (YT.get('youtube-player')) {
        console.log('destroying current yt frame');
        YT.get('youtube-player').destroy();
    }
}

var renderYT = function makePlayer(elem, i) {
    console.log('creating youtube-player frame for ' + elem.id);

    player = new YT.Player("youtube-player", {
        // // height: "100",
        // width: "0",
        videoId: elem.id,
        playerVars: {
            autoplay: true,
            loop: false,
            color: 'purple',
            controls: 2,
            enablejsapi: 1
        },
        events: {
            onReady: function(e) {
                e.target.setPlaybackQuality("medium");
                console.log('new video is ready');
                e.target.playVideo();
                toggleButon(true, i);

            },
            onStateChange: function(e) {
                if (e.data === YT.PlayerState.ENDED) {
                    console.log('Finished video for post ' + i);
                    toggleButon(false, i);
                    player.destroy();
                    player = null;
                    startNext(i);
                }
            }
        }
    });
    return player
};


function clickYT(elem, i) {

    removeSC();

    if (!YT.get('youtube-player')) {

        if (document.contains(document.getElementById("sc-player"))) {
            document.getElementById("sc-player").remove();
        }

        renderYT(elem, i);
        toggleButon(true, i);
        $('#now-playing-display').show('slow');
        $('#toggle-player').show('slow');

        console.log('created first yt player with:' + elem.id);

    } else {
        console.log('clicked while iframe exists')

        if (player.a.src.toString().includes(elem.id)) {
            console.log('Clicked current item');
            console.log(player.getPlayerState());

            // playing or buffering
            if (player.getPlayerState() === 1 || player.getPlayerState() === 3) {

                console.log('pausing current video ' + elem.id)
                player.pauseVideo();
                toggleButon(false, i);
            }

            // cued 
            if (player.getPlayerState() === 5 || player.getPlayerState() === 2) {

                console.log('playing current video ' + elem.id);
                player.playVideo();
                toggleButon(true, i);
            }


        } else { // start new vid
            console.log('starting new video ' + elem.id)
            toggleButon(false, i);
            player.destroy();
            renderYT(elem, i);
            toggleButon(true, i)

        }
    }
}




/////////////////
// Soundcloud //
////////////////
var widget = null;

var trackUrl = function(trackId) {
    return 'http://api.soundcloud.com/tracks/' + trackId;
}

var widgetUrl = function(trackId) {
    // src contains widget api url + the track api url
    return 'https://w.soundcloud.com/player/?url=' + trackUrl(trackId);
}

var removeSC = function() {
    if (document.contains(document.getElementById('sc-player'))) {
        console.log('removing current sc widget')
        document.getElementById('sc-player').remove();
    }
}

var renderSC = function(elem, i) {
    console.log('creating widget for elem ' + i);
    var widgetDiv = document.getElementById('sc-player-div');
    var widgetIframe = document.createElement('iframe');

    widgetIframe.setAttribute('src', widgetUrl(elem.id));
    widgetIframe.setAttribute('id', 'sc-player');
    widgetIframe.setAttribute('width', '100%');

    widgetDiv.append(widgetIframe);
    widget = SC.Widget(widgetIframe);
    setUpWidget(widget, widgetIframe, elem, i);
}

var setUpWidget = function(w, frame, elem, i) {

    w.bind(SC.Widget.Events.LOAD_PROGRESS, function() {
        console.log('loading');
    });

    w.bind(SC.Widget.Events.READY, function() {
        console.log('widget ready')

        w.bind(SC.Widget.Events.PLAY, function() {
            // get information about currently playing sound
            w.getCurrentSound(function(currentSound) {
                console.log('playback started for  ' + currentSound.title + '-- track ' + i);
            });
            toggleButon(true, i);

        });

        w.bind(SC.Widget.Events.PAUSE, function() {
            w.getCurrentSound(function(currentSound) {
                console.log('playback paused for  ' + currentSound.title + '-- track ' + i);
            });
            toggleButon(false, i);

        });



        w.bind(SC.Widget.Events.FINISH, function() {
            console.log('finishing track ' + i);
            widget = null; // assign null to global widget var used to check
            frame.remove();

            toggleButon(false, i);
            startNext(i);

        });

        // get current level of volume
        w.getVolume(function(volume) {
            // console.log('current volume value is ' + volume);
        });
        // set new volume level
        w.setVolume(50);
        // get the value of the current position

        w.play();
    });
}

var clickSC = function(elem, i) {

    removeYT();

    if (widget) { // prbly a better way tto do this
        console.log('widget exists');


        widget.getCurrentSound(function(currentSound) {

            if (currentSound.id.toString() === elem.id) {
                console.log('clicked on current sc element')

                widget.isPaused(function(paused) {
                    console.log('paused is ' + paused);
                    if (paused) {
                        console.log('playing')
                        widget.play();
                    } else {
                        console.log('pausing');
                        widget.pause();

                    }
                })
            } else {
                console.log('creating new widget')
                widget.load(trackUrl(elem.id));
                widget.play();
            }

        })

    } else {
        console.log('creating first sc widget')
        renderSC(elem, i);
        $('#now-playing-display').show('slow');
        $('#toggle-player').show('slow');


    }
}
