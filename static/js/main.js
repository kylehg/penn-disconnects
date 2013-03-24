(function() {
  var pdc;

  pdc = pdc || {};

  pdc.init = function() {
    return $('#interest-form').on('submit', function(e) {
      console.log($(this).serialize());
      $.post('/submit', $(this).serialize(), pdc.postSubmit, 'json');
      return false;
    });
  };

  pdc.postSubmit = function(data, status, jqxhr) {
    return console.log(data);
  };

  $(pdc.init);

}).call(this);
