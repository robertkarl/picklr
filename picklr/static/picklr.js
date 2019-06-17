var ENTERKEY = 13;
(function() {
  var do_submit = function(frm) {
    $.ajax({
      url: '/ratings/mh1',
      data: frm.serialize(),
      method: 'post',
      success: function(data) {
        $('#content').html('');
        for (item in data) {
            var name = $('<td>'+data[item][0] + '</td>');
            var rating = $('<td>'+data[item][1] + '</td>');
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
})();

