# Main

pdc = pdc || {}

# Initalize everything
pdc.init = ->
  $('#interest-form').on 'submit', (e) ->
    console.log $(this).serialize()
    $.post '/submit', $(this).serialize(), pdc.postSubmit, 'json'

    false # Prevent actual submit


# On server response
pdc.postSubmit = (data, status, jqxhr) ->
  console.log data



# Kick it off
$ pdc.init