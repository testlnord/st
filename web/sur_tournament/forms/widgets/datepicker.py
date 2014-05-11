from django.forms.widgets import Input

class DatepickerInput(Input):
    def __init__(self, attrs = None):
        self.attrs = attrs


    def render(self, name, value, attrs=None):
        format = "dd-mm-yyyy"
        if attrs is not None:
            format = attrs.pop('format', format)

        a = """
            <div class="input-append date" id="dp3" data-date="12-02-2012" data-date-format="%s">
            <input class="span2" size="16" type="text" value="%s">
            <span class="add-on"><i class="icon-th"></i></span>
            </div>
        """%(format, format)

        print(a)
        return a