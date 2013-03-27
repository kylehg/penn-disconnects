# Main

pdc = pdc || {}

# Initalize everything
pdc.init = ->
  $('#email-field').val (window.localStorage['email'] || '')
  $('#name-field').val (window.localStorage['name'] || '')
  $('#interest-form').on 'submit', pdc.formSubmit
  $('#interest-form input').on 'keyup', pdc.formCheck
  $('#tell-me-more a').on 'click', pdc.interestSubmit
  pdc.formCheck()


pdc.interestSubmit = (e) ->
  e.preventDefault()
  $('#tell-me-more a').fadeOut ->
    $('#tell-me-more .post-submit').fadeIn ->
      data =
        name: window.localStorage['name']
        email: window.localStorage['email']
        is_interested: true
      $.post '/submit', data, 'json'



# Submit the form
pdc.formSubmit = (e) ->
  console.log $(this).serialize()
  if $('input[type="submit"]').hasClass('ready')
    for item in $(this).serializeArray
      window.localStorage[item['name']] = item['value']
    $.post '/submit', $(this).serialize(), pdc.postSubmit, 'json'
  false # Prevent actual submit


# Form validate
pdc.formCheck = (e) ->
  form = $('#interest-form')
  email = $('#email-field').val()
  if ($('#name-field').val() and
      (0 < email.indexOf('@') < (email.indexOf('.') - 1) < (email.length - 3)))
    $('input[type="submit"]').addClass('ready')
  else
    $('input[type="submit"]').removeClass('ready')


# On server response
pdc.postSubmit = (data, status, jqxhr) ->
  console.log " erro#{status}: #{data}"
  if not data.error
    $('#side1').fadeOut ->
      $('#side2').fadeIn()
      for key, val of data['data']
        console.log "#{key}: #{val}"
        window.localStorage[key] = val



# Kick it off
$ pdc.init