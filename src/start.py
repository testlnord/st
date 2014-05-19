import config
import util.register
import os
import run_runner

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

run_runner.add_cron_entry()


# with server.Server() as s:
#     s.run(config.serverHost,config.serverPort)

s = zmq_server.ServerTask();
s.run()
