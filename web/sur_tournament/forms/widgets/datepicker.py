from django.forms.widgets import Input
from django import forms


class DatepickerInput(forms.TextInput):



    def render(self, name, value, attrs=None):
        format = "dd-mm-yyyy"
        if attrs is not None:
            format = attrs.pop('format', format)

        a = """

            <div class="input-append date" id="dp3" data-date="12-02-2012" data-date-format="%s">
            <input class="span" size="16" type="text" value="%s">
            <span class="add-on"><i class="icon-th"></i></span>
            </div>
            <script>
    if (top.location != location) {
    top.location.href = document.location.href ;
  }
        $(function(){
            window.prettyPrint && prettyPrint();
            $('#dp3').datepicker();

        });
    </script>
        """%(format, format)

        return a