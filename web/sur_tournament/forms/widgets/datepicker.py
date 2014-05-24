from datetime import datetime
from django.forms.widgets import Input
from django import forms


class DatepickerInput(forms.TextInput):
    id = 0

    def __init__(self, type="text", attrs = None):
        self.input_type = type
        super(DatepickerInput, self).__init__(attrs)
        self.inst_id = DatepickerInput.id
        DatepickerInput.id += 1

    def render(self, name, value, attrs=None):
        date_format = "yyyy-mm-dd"
        if attrs is not None:
            date_format = attrs.pop('format', date_format)
        if not value:
            value = datetime.now().strftime("%Y-%m-%d")
        text_inp = super(DatepickerInput, self).render(name, value, attrs)
        a = """
            <div class="input-append date" id="dp{0}" data-date="{1}" data-date-format="{2}">
            {3}
            <span class="add-on"><i class="icon-th"></i></span>
            </div>
            <script>
    if (top.location != location) {{
    top.location.href = document.location.href ;
  }}
        $(function(){{
            window.prettyPrint && prettyPrint();
            $('#dp{0}').datepicker();

        }});
    </script>
        """.format(self.inst_id, value, date_format, text_inp)

        return a