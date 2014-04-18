from django import forms

class AddTournamentForm(forms.Form):
    name = forms.CharField(max_length=100)
    checker = forms.ChoiceField()
    timelimit = forms.IntegerField()
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    _errors = ''
    def __init__(self, checkers, *args, **kwargs):
        super(AddTournamentForm, self).__init__(*args, **kwargs)
        if checkers:
            self.fields['checker'].choices = [(x,x) for x in checkers]
