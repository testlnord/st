__author__ = 's'
from sender import *



s=Sender('127.0.0.1',8080)
# s.sendUserInfo("Kolyan2","kolyan@ya.ru")
# s.sendCreateTournament("test2","tictactoe",10,123123,123124123)
# s.add_user_to_tour("Kolyan2","test5")
#  s.send_solution("Kolyan","test5","cpp","/home/s/PycharmProjects/st/test/tictactoe/cpp/main.cpp")
# response = s.getUserInfoByName('Barybasyan')
# print(s.dict(response))
# s.run_tournament("test5")
response = s.getUserInfoByName("Kolyaasdn2")
#response = s.sendUserInfo("Kolyan2","kolyan@ya.ru")
print(s.dict(response))
