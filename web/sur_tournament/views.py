import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
import time
from helpers import game_server
import forms.add_tournament
import forms.tournament


def main(request, template_name='index.html'):
    tours = game_server.get_tournaments()
    return render(request, template_name, {'tours_info': tours})


def tour(request, id = None, template_name='tour.html', s={}):

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

    result = game_server.get_tour_results(cur_tour['name'])
    print (result)
    #result = ''

    formSend = None
    formReg = None
    if request.user.is_authenticated():
        user_registered = bool(game_server.is_user_in_tour(request.user.username, cur_tour['name']))

        builders = game_server.get_builders()
        username = request.user.username
        if request.method == 'POST': # If the form has been submitted...
            if user_registered:
                formSend = forms.tournament.SendSolution(username, cur_tour['name'], builders, request.POST, request.FILES)
                if formSend.is_valid():
                    form_data = formSend.cleaned_data
                    status = game_server.send_solution(form_data['user'],form_data['tour'],
                                              form_data['type'], request.FILES['solution'])
                    return render(request,
                                  template_name,
                                  {'tour':cur_tour, 'formSend': formSend, 'formReg': formReg, 'status': status,
                                   'result': result}
                    )
                    #return HttpResponseRedirect('/tour/%d'%id, s=status) # Redirect after POST
            else:
                formReg = forms.tournament.RegUser(username, cur_tour['name'], request.POST)
                if formReg.is_valid():
                    form_data = formReg.cleaned_data
                    game_server.add_user_to_tour(form_data['user'],form_data['tour'])
                    return HttpResponseRedirect('/tour/%d'%id) # Redirect after POST
        else:
            if user_registered:
                formSend = forms.tournament.SendSolution(username, cur_tour['name'], builders)
            else:
                formReg = forms.tournament.RegUser(username, cur_tour['name'])

    return render(request, template_name, {'tour':cur_tour, 'formSend': formSend, 'formReg': formReg, 'status': s,
                                           'result': result})


def users(request, name = None, template_name = 'users.html'):
    if name is None:
        return HttpResponseRedirect('/') # Redirect after none name

    all_user_info = game_server.getUserInfoByName(name)
    if all_user_info is None:
        return HttpResponseRedirect('/') # Redirect after bad user ID

    verbose = False
    if request.user.is_authenticated() and request.user.username == all_user_info["name"]:
        verbose = True
    #todo check for illegal user
    user_info = {"name": all_user_info["name"]}
    if verbose:
        user_info["email"] = all_user_info["email"]
    tour_info = None
    old_tours = []
    cur_tours = []
    tour_info = game_server.get_user_tour_info(all_user_info["name"])

    if tour_info is None:
        tour_info = []
    for info in tour_info:
        if "runs" in info.keys():
            prev = None
            run_number = 0
            for r in info["runs"]:
                if prev is None or prev != r[0]:
                    prev = r[0]
                    run_number += 1

                r[0] = run_number
            for r in info["runs"]:
                r[0] = run_number + 1 - r[0]

        if info["end_time"] < datetime.datetime.now():
            old_tours.append(info)
        else:
            cur_tours.append(info)


    return render(request, template_name, {'user_info': user_info, 'old_tour_info': old_tours, 'tour_info': cur_tours})


def get_game_log(request):
    game_log = ''
    if request.method == 'GET':
        game_id = request.GET['gamid']
        game_log = game_server.get_game_log(game_id)

    return HttpResponse(game_log)


def add_tour(request, template_name='a_tour.html'):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/') # Redirect if not auth
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

def contact(request, template_name='contact.html'):
    return render(request, template_name)

