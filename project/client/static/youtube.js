
var player = null;


function onYouTubeIframeAPIReady() {

    // player = function () {
    //     return YT.get('youtube-player');
    // }
    console.log(player)

    console.log('In youtubeready');

    var postItems = document.getElementsByClassName('post-item');
    console.log('Number of reddit posts: ' + postItems.length)

    Array.from(postItems).forEach(function(elem, i) {
        console.log(elem.classList.contains('reddit-post'));

        if (elem.classList.contains('reddit-post')) {

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


        var toggleButon = function(e) {
            var iconSource = e ? "IDzX9gL.png" : "quyUPXN.png";

            if (!elem.classList.contains('active')) {
                elem.classList.add('active');
                elem.style.backgroundColor = '#efd2eb';
            } 


            icon.setAttribute("src", "https://i.imgur.com/" + iconSource);
            console.log(elem);
        };

        var startNext = function () {
            document.getElementById('post-icon-'+(i+1)).click();

        }

        elem.addEventListener('click', function() {
            console.log('clicked ' + elem.id);

            if (!YT.get('youtube-player')) {
                renderPlayer(elem.id);
                $('#now-playing-display').show('slow');
                $('#toggle-player').show('slow');
                console.log('CREATED FIRST PLAYER with:' + elem.id);
            }

            if (player.a.src.toString().includes(elem.id)) {
                console.log(elem.id+ ' is ' + player.getPlayerState());

                if (player.getPlayerState() === YT.PlayerState.PLAYING
                    || player.getPlayerState() === YT.PlayerState.BUFFERING) {


                    console.log('pausing video ' + elem.id)
                    player.pauseVideo();
                    toggleButon(false);
                }

                if (player.getPlayerState() === YT.PlayerState.CUED) {
                
                    // console.log(elem.id + ' is cued');
                    player.playVideo();
                    toggleButon(true);
                }


            } else { // start new vid
                console.log('starting new video ' + elem.id)
                player.destroy();
                toggleButon(false)
                renderPlayer(elem.id);

                player.playVideo()
                toggleButon(true)

            }




        })


        function renderPlayer(postVideoID) {

            console.log('rendering for ' + postVideoID);

            player = new YT.Player("youtube-player", {
                // // height: "100",
                // width: "0",
                videoId: postVideoID,
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
                        toggleButon(e.target.getPlayerState() !== YT.PlayerState.CUED);

                    },
                    onStateChange: function(e) {
                        if (e.data === YT.PlayerState.ENDED) {
                            toggleButon(false);
                            startNext();
                            // start next post
                        }
                    }
                }
            });
            return player





        };

    }
});

}

