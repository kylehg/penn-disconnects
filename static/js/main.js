(function() {
  var pdc;

  pdc = pdc || {};

  pdc.init = function() {
    $('#email-field').val(window.localStorage['email'] || '');
    $('#name-field').val(window.localStorage['name'] || '');
    $('#interest-form').on('submit', pdc.formSubmit);
    $('#interest-form input').on('keyup', pdc.formCheck);
    $('#tell-me-more a').on('click', pdc.interestSubmit);
    return pdc.formCheck();
  };

  pdc.interestSubmit = function(e) {
    e.preventDefault();
    return $('#tell-me-more a').fadeOut(function() {
      return $('#tell-me-more .post-submit').fadeIn(function() {
        var data;
        data = {
          name: window.localStorage['name'],
          email: window.localStorage['email'],
          is_interested: true
        };
        return $.post('/submit', data, 'json');
      });
    });
  };

  pdc.formSubmit = function(e) {
    var item, _i, _len, _ref;
    console.log($(this).serialize());
    if ($('input[type="submit"]').hasClass('ready')) {
      _ref = $(this).serializeArray;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        item = _ref[_i];
        window.localStorage[item['name']] = item['value'];
      }
      $.post('/submit', $(this).serialize(), pdc.postSubmit, 'json');
    }
    return false;
  };

  pdc.formCheck = function(e) {
    var email, form, _ref, _ref2;
    form = $('#interest-form');
    email = $('#email-field').val();
    if ($('#name-field').val() && (((0 < (_ref2 = email.indexOf('@')) && _ref2 < (_ref = email.indexOf('.') - 1)) && _ref < (email.length - 3)))) {
      return $('input[type="submit"]').addClass('ready');
    } else {
      return $('input[type="submit"]').removeClass('ready');
    }
  };

  pdc.postSubmit = function(data, status, jqxhr) {
    console.log(" erro" + status + ": " + data);
    if (!data.error) {
      return $('#side1').fadeOut(function() {
        var key, val, _ref, _results;
        $('#side2').fadeIn();
        _ref = data['data'];
        _results = [];
        for (key in _ref) {
          val = _ref[key];
          console.log("" + key + ": " + val);
          _results.push(window.localStorage[key] = val);
        }
        return _results;
      });
    }
  };

  $(pdc.init);

}).call(this);
