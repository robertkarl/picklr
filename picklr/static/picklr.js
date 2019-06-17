(function() {
  var do_submit = function(frm) {
    $.ajax({
      url: '/doratings',
      data: frm.serialize(),
      method: 'post',
      success: function(data) {
        $('#content').html('');
        for (item in data) {
          $('#content').append($('<p>' + data[item] + '</p>'));
        }
        console.log(data);
      },
    });
  }


  var frm = $("#doit");
  frm.submit(function(e) {
    e.preventDefault();
    do_submit(frm);
  });
})();

