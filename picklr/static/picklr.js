(function() {
  var do_submit = function(frm) {
    $.ajax({
      url: '/picklr/doratings',
      data: frm.serialize(),
      method: 'post',
      success: function(data) {
        $('#content').html('');
        for (item in data) {
          $('#content').append($('<tr><td>' + data[item] + '</td></tr>'));
        }
      },
    });
  }
  var frm = $("#doit");
  frm.submit(function(e) {
    e.preventDefault();
    do_submit(frm);
  });
})();

