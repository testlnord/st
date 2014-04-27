from django import forms


class RegUser(forms.Form):
    tour = forms.CharField(widget=forms.HiddenInput())
    user = forms.CharField(widget=forms.HiddenInput())
    _errors = ''

    def __init__(self, user, tour, *args, **kwargs):
        super(RegUser, self).__init__(*args, **kwargs)
        self.fields['tour'].initial = tour
        self.fields['user'].initial = user


class SendSolution(forms.Form):
    tour = forms.CharField(widget=forms.HiddenInput())
    user = forms.CharField(widget=forms.HiddenInput())
    type = forms.ChoiceField()
    solution = forms.FileField()
    _errors = ''

    def __init__(self, user, tour,types, *args, **kwargs):
        super(SendSolution, self).__init__(*args, **kwargs)
        self.fields['tour'].initial = tour
        self.fields['user'].initial = user
        self.fields['type'].choices = [(x,x) for x in types]


