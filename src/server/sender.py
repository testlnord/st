__author__ = 's'

import urllib.parse
import urllib.request

class Sender:
    def sendUserInfo(self,host,port,name):
        url = 'http://'+str(host)+':'+str(port)
        user_agent = 'Mozilla/5.0 (compatible; Chrome/22.0.1229.94; Windows NT)'
        values = {'User' : name}
        headers = {'User-Agent': user_agent }
        data = urllib.parse.urlencode(values)
        binary_data = data.encode('utf-8')
        req = urllib.request.Request(url, binary_data)
        response = urllib.request.urlopen(req)
        # the_page = response.read()

if __name__ == "__main__":
    s=Sender()
    s.sendUserInfo('127.0.0.1',8080,'Jhon')





