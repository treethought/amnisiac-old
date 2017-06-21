var saveBtns = document.getElementsByClassName('save-btn');

Array.from(saveBtns).forEach(function(elem, i) {
    var postRow = elem.parentElement.parentElement
    var trackId = elem.id.split('-save')[0];
    var rawTitle = document.getElementById(trackId + '-title').innerHTML;
    var trackSource = null;

    if (postRow.className.includes('reddit-row')) {
       trackSource = 'reddit';
    } else {
       trackSource = 'sc'
    }


    console.log(rawTitle + ' -- ' + trackId);

    elem.addEventListener('click', function() {
      $.ajax({
        url: $SCRIPT_ROOT + '/save_item',
        type: 'POST',
        dataType: 'json',
        data:{track_id: trackId, raw_title: rawTitle, source: trackSource},
      })
      .done(function() {
        console.log('sent ' + trackId)
        console.log("success");
      })
      .fail(function() {
        console.log("error");
      })
      .always(function() {
        console.log("complete");
      });
      
    });
  });