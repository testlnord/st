from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from helpers import game_server
import forms.add_tournament
import forms.tournament


def main(request, template_name='index.html'):
    tours = game_server.get_tournaments()
    return render(request, template_name, {'tours_info': tours})





def tour(request, id = None, template_name='tour.html'):

    if id is None:
        return HttpResponseRedirect('/') # Redirect after none ID
    try:
        id = int(id)
    except ValueError:
        return HttpResponseRedirect('/') # Redirect after bad ID

    tours = game_server.get_tournaments()
    cur_tour = None

    for tour in tours:
        if tour["id"] == id:
            cur_tour = tour
            break
    if cur_tour is None:
        return HttpResponseRedirect('/') # Redirect after bad ID

    form = None
    if request.user.is_authenticated():
        user_registered = True    #todo Check user register or not
        builders = game_server.get_builders()
        username = request.user.username
        if request.method == 'POST': # If the form has been submitted...
            if user_registered:
                form = forms.tournament.SendSolution(username, cur_tour['name'], builders, request.POST, request.FILES)
                if form.is_valid():
                    form_data = form.cleaned_data
                    game_server.send_solution(form_data['user'],form_data['tour'],
                                              form_data['type'], request.FILES['solution'])
                    return HttpResponseRedirect('/tour/%d'%id) # Redirect after POST
            else:
                form = forms.tournament.RegUser(username, cur_tour['name'], request.POST)
                if form.is_valid():
                    form_data = form.cleaned_data
                    game_server.add_user_to_tour(form_data['user'],form_data['tour'])
                    return HttpResponseRedirect('/tour/%d'%id) # Redirect after POST
        else:
            if user_registered:
                form = forms.tournament.SendSolution(username, cur_tour['name'], builders)
            else:
                form = forms.tournament.RegUser(username, cur_tour['name'])

    return render(request, template_name, {'tour':cur_tour, 'form': form})


def users(request, name = None, template_name = 'users.html'):
    if name is None:
        return HttpResponseRedirect('/add_tour/') # Redirect after none ID

    user_info = game_server.getUserInfoByName(name)
    #todo check for illegal user
    return render(request, template_name, {'user_info': user_info})

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