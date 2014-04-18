from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from helpers import game_server
import forms.add_tournament



def main(request, template_name='index.html'):
    tours = game_server.get_tournaments()
    return render(request, template_name, {'user_info': tours})

def add_tour(request, template_name='a_tour.html'):
    checkers = game_server.get_checkers()
    if not isinstance(checkers, (list, tuple)) or isinstance(checkers, str):
            checkers = [checkers]
    if request.method == 'POST': # If the form has been submitted...
        form = forms.add_tournament.AddTournamentForm(checkers, request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form_data = form.cleaned_data
            game_server.sendCreateTournament(form_data["name"], form_data["checker"],
                                             form_data["timelimit"], form_data["start_time"], form_data["end_time"] )
            return HttpResponseRedirect('/') # Redirect after POST
    else:


        form = forms.add_tournament.AddTournamentForm(checkers) # An unbound form

    return render_to_response(template_name, {
        'form': form,
    }, context_instance = RequestContext(request))