import json
import urllib
from django.shortcuts import render
from django.template import loader

import stserver_config
# Create your views here.
def main(request, template_name='index.html'):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_user_info?name="+"asdf"
    response = urllib.request.urlopen(url)
    json_data= response.read().decode('utf-8')
    json_data=json.loads(json_data)
    json_data=json_data[0]
    return render(request, template_name, {'user_info':json_data})

