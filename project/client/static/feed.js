var postItems = document.getElementsByClassName('post-item');

var toggleButon = function(e, elem, i) {
    var iconSource = e ? "IDzX9gL.png" : "quyUPXN.png";

    if (!elem.classList.contains('active')) {
        elem.classList.add('active');
        elem.style.backgroundColor = '#efd2eb';
        elem.parentElement.style.backgroundColor = '#efd2eb';
    }

    icon = document.getElementById("post-icon-" + i);

    icon.setAttribute("src", "https://i.imgur.com/" + iconSource);
    console.log(elem);
};

var startNext = function (i) {
            document.getElementById('post-icon-'+(i+1)).click();
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
        console.log('clicked post ' + i + '-- videoId: ' + elem.id);

        if (elem.className.includes('reddit')) {
            clickYT(elem, i);
        } else {
            clickSC(elem, i);
        }

        // toggleButon(true);
        var now = document.getElementById('#now-playing-display')
        var btn = document.getElementById('#toggle-player')

        $('#now-playing-display').show('slow');
        $('#toggle-player').show('slow');



    })

})




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
                    toggleButon(false, elem, i);
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

        console.log('CREATED FIRST PLAYER with:' + elem.id);

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
            player.destroy();
            toggleButon(false, elem, i);
            renderYT(elem, i);

            // player.playVideo()
            toggleButon(true, elem, i)

        }
    }
}
// }
