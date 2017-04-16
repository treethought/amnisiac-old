
$(function() {
  var widget = null;


  var postItems = document.getElementsByClassName('post-item');
  console.log('Number of soundcoud posts: ' + postItems.length)

  Array.from(postItems).forEach(function(elem, i) {
    if (elem.classList.contains('sc-post')) {

        

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

            icon.setAttribute("src", "https://i.imgur.com/" + iconSource);
        };

        var startNext = function() {
            console.log('finishing track ' + i);
            document.getElementById('post-icon-' + (i + 1)).click();

        }

        function createWidget(trackUrl) {

            var widgetDiv = document.getElementById('sc-player-div');
            var widgetIframe = document.createElement('iframe');

            // src contains widget api url + the track api url
            widgetIframe.setAttribute('src', 'https://w.soundcloud.com/player/?url=' + trackUrl);
   
            widgetIframe.setAttribute('id', 'sc-player');
            widgetIframe.setAttribute('width', '100%');
            // widgetIframe.setAttribute('height', 465)
            widgetDiv.append(widgetIframe);

            widget = SC.Widget(widgetIframe);
        
            widget.bind(SC.Widget.Events.READY, function() {

                widget.bind(SC.Widget.Events.PLAY, function() {

                    // get information about currently playing sound
                    widget.getCurrentSound(function(currentSound) {
                      console.log('playing '+ trackUrl);
                      // console.log('sound ' + currentSound + 'began to play');
                    });

                });

                widget.bind(SC.Widget.Events.FINISHED, function() {
                    console.log('finishing')
                      console.log('finishing track ' + i);
                        document.getElementById('post-icon-' + (i + 1)).click();
                  });

                // get current level of volume
                widget.getVolume(function(volume) {
                  console.log('current volume value is ' + volume);
                });
                // set new volume level
                widget.setVolume(50);
                // get the value of the current position
                console.log('Just made widget for icon ' + i);

            widget.play();
            });

        }



        elem.addEventListener('click', function() {
            console.log('clicked ' + elem.id);
            var trackUrl = 'http://api.soundcloud.com/tracks/' + elem.id;
            
            if (widget) { // prbly a better way tto do this
                document.getElementById('sc-player').remove();
            }

            createWidget(trackUrl);
            toggleButon();

            $('#now-playing-display').show('slow');
            $('#toggle-player').show('slow');
            console.log('CREATED FIRST SC PLAYER with:' + elem.id);
            
        })
             
  }
})
});





















