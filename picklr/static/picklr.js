var ENTERKEY = 13;
var URL_PREFIX = URL_PREFIX || '';
console.log(URL_PREFIX);
(function() {
    var do_submit = function(frm) {
        var ajax_url = 'ratings'; // it matters whether or not this begins with a slash
        console.log(ajax_url);
        $.ajax({
            url: ajax_url,
            data: frm.serialize(),
            method: 'post',
            success: function(data) {
                $('#content').html('');
                console.log(data);
                for (index in data) {
                    var item = data[index];
                    var nameText = item.Card;
                    var name = $('<td><a href="https://scryfall.com/search?q=set:mh1 ' + item.Card + '">' + item.Card + '</a></td>');
                    var rating = $('<td>' + item.Rating + '</td>');
                    var img = $('<a class="col" href="' + item.uri + '"><img style="max-width:190px" src="'+ item.image_uri + '"></a>');
                    var row = $('<tr>');
                    row.append(name);
                    row.append(img)
                    row.append(rating);
                    $('#content').append(row);
                }
            },
        });
    }
    var frm = $("#doit");
    frm.submit(function(e) {
        e.preventDefault();
        do_submit(frm);
    });

    $('#cards-input').on('keypress', function(e) {
        if (e.keyCode == ENTERKEY) {
            do_submit(frm);
            return true;
        }
    });

    $('#clear-text').on('click', function(e) {
        $('#cards-input').val('');
    });

    do_submit(frm);
})();