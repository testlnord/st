import config
import util.register
import os

for path in config.start_list:
    if os.path.isdir(path):
        for (dir, dirs, files) in os.walk(path):
            for file in files:
                if file[-3:] == ".py":
                    exec("import %s"%(file[:-3]))
    else:
        if path[-3:] == ".py":
            exec("import %s"%(path[:-3]))

print(util.register.runners)
print(util.register.builders)
print(util.register.checkers)


with server.Server() as s:
    s.run(config.serverHost,config.serverPort)
