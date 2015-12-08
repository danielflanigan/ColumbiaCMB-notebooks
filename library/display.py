from IPython.core import display


def hide_code(button=False):
    display.display_html('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery('
                   '".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)
    if button:
        display.display_html('''<button onclick="jQuery('.input_area').toggle(); jQuery('.prompt').toggle();">Toggle
        code</button>''', raw=True)


# Deprecated
def toggle_input_code():
    try:
        from ipywidgets import HTML
    except ImportError:
        from IPython.display import HTML
    return HTML('''<script>
        code_show=true;
        function code_toggle() {
         if (code_show){
         $('div.input').hide();
         } else {
         $('div.input').show();
         }
         code_show = !code_show
        }
        $( document ).ready(code_toggle);
        </script>
        <form action="javascript:code_toggle()"><input type="submit" value="Hide/show the input code."></form>''')



