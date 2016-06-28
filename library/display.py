from IPython.core import display


def hide_code(button=False):
    display.display_html('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery('
                   '".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)
    if button:
        display.display_html('''<button onclick="jQuery('.input_area').toggle(); jQuery('.prompt').toggle();">Toggle
        code</button>''', raw=True)
