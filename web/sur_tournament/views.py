from django.shortcuts import render
from django.template import loader
import os

# Create your views here.
def main(request, template_name='main.html'):

    return render(request, template_name)