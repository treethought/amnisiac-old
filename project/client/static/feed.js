

var postItems = document.getElementsByClassName('post-item');

var toggleButon = function(playing, elem, i) {
    var iconSource = playing ? "IDzX9gL.png" : "quyUPXN.png";  // if playing set pause symbol, else set play symbol

    if (!elem.classList.contains('active')) {
        elem.classList.add('active');
        elem.style.backgroundColor = '#efd2eb';
        elem.parentElement.style.backgroundColor = '#efd2eb';
    }

    icon = document.getElementById("post-icon-" + i);

    icon.setAttribute("src", "https://i.imgur.com/" + iconSource);
};

var startNext = function(i) {
    document.getElementById('post-icon-' + (i + 1)).click();
}

Array.from(postItems).forEach(function(elem, i) {

    // Render Icon
    var icon = document.createElement("img");
    icon.setAttribute("id", "post-icon-" + i);
    icon.setAttribute("class", 'icon');
    icon.setAttribute("src", "https://i.imgur.com/" + "quyUPXN.png");

    icon.style.cssText = "cursor:pointer;cursor:hand";
    icon.style.height = '50px';
    icon.style.width = '50px';
    icon.setAttribute('class', "img-responsive")
    elem.appendChild(icon);


    elem.addEventListener('click', function() {
        console.log('clicked post ' + i);

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

// Soundcloud

var widget = null;





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
            toggleButon(true, elem, i);

        });

        w.bind(SC.Widget.Events.PAUSE, function() {
            w.getCurrentSound(function(currentSound) {
                console.log('playback paused for  ' + currentSound.title + '-- track ' + i);
            });
            toggleButon(false, elem, i);

        });



        w.bind(SC.Widget.Events.FINISH, function() {
            console.log('finishing track ' + i);
            widget = null; // assign null to global widget var used to check
            frame.remove();
            toggleButon(false, elem, i);
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

var trackUrl = function(trackId) {
    return 'http://api.soundcloud.com/tracks/' + trackId;
}

var widgetUrl = function(trackId) {
    // src contains widget api url + the track api url
    // var trackUrl = 'http://api.soundcloud.com/tracks/' + elem.id;
    return 'https://w.soundcloud.com/player/?url=' + trackUrl(trackId);
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

var scPausedCallback = function(paused, elem, i) {
    console.log('element ' + i + 'paused: ' + paused);
    if (paused) {
        widget
    }
}

var clickSC = function(elem, i) {
    if (widget) { // prbly a better way tto do this
        console.log('widget exists')


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
            }

        })

    } else {
        console.log('creating first sc widget')
        renderSC(elem, i);
        $('#now-playing-display').show('slow');
        $('#toggle-player').show('slow');


    }
}


// Youtube Iframe creation and controls

var renderYT = function(elem, i) {
    console.log('creating youtube-player frame for ' + elem.id);

    console.log('in ytready')

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
                // toggleButon(e.target.getPlayerState() !== YT.PlayerState.CUED);

            },
            onStateChange: function(e) {
                if (e.data === YT.PlayerState.ENDED) {
                    console.log('Finished video for post ' + i);
                    toggleButon(false, elem, i);
                    player.destroy();
                    startNext(i);
                }
            }
        }
    });
    return player
};



var player = null;


function clickYT(elem, i) {


    if (!YT.get('youtube-player')) {

        renderYT(elem, i);
        toggleButon(true, elem, i);
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
                toggleButon(false, elem, i);
            }

            // cued 
            if (player.getPlayerState() === 5 || player.getPlayerState() === 2) {

                console.log('playing current video ' + elem.id);
                player.playVideo();
                toggleButon(true, elem, i);
            }


        } else { // start new vid
            console.log('starting new video ' + elem.id)
            toggleButon(false, elem, i);
            renderYT(elem, i);

            // player.playVideo()
            toggleButon(true, elem, i)

        }
    }
}
// }
