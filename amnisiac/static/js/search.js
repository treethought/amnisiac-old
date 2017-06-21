$(function() {

    // Autocomplete reddit search with select2

    // build sources from table
    var source_data = []
    $("#source-table tr td").each(function() {
        source_data.push($(this).text());
    });

    // initialize w/ select2
    $('#reddit-search-bar').select2({
        multiple: true,
        placeholder: '/r/',
        data: source_data,
        tags: true,

    });


    $('#source-list').hide();
    $('#nav').hide();


    // toggling source table
    var btn = $('#toggle-sources');
    var sources = $('#source-list');
    btn.click(function() {
        if (sources.is(':visible')) {
            sources.hide();
            btn.text('show list')
        } else {
            sources.show();
            btn.text('hide list')
        }


    });


    // Autocomplete sc search w/ jquery autocomplete ajax call

    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

    $("#sc-search-bar").autocomplete({
        source: function(request, response) {
            console.log(request.term)
            $.getJSON($SCRIPT_ROOT + '/sc_autocomplete', {
                q: extractLast(request.term), // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                console.log(data.results);
                var source_data = data.results;
                response(data.results); // matching_results from jsonify
            });
        },
        minLength: 3,
        select: function(event, ui) {
            // console.log(ui.item.value); // not in your question, but might help later
            var terms = split(this.value);
            terms.pop();
            terms.push(ui.item.value);
            terms.push("");
            this.value = terms.join(", ");
            return false;
        }
    })

});