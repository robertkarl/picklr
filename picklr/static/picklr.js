var ENTERKEY = 13;
var URL_PREFIX = URL_PREFIX || '';
(function() {
    var do_submit = function(frm) {
        $.ajax({
            url: URL_PREFIX + '/ratings/mh1',
            data: frm.serialize(),
            method: 'post',
            success: function(data) {
                $('#content').html('');
                for (item in data) {
                    var nameText = data[item][0];
                    var name = $('<td><a href="https://scryfall.com/search?q=set:mh1 ' + nameText + '">' + nameText + '</a></td>');
                    var rating = $('<td>' + data[item][1] + '</td>');
                    var row = $('<tr>');
                    row.append(name);
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