import subprocess
import threading
import util.register
import util.exceptions


class Runner:
    def __init__ (self, path, timeout):
        self.path = path
        self.proc = None
        self.timeout = timeout

    def step(self, arg):

        def target(res):
            self.proc = subprocess.Popen([self.path], shell= True, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE)
            (o, e) = self.proc.communicate(bytes(arg, "UTF8"))
            res.append(o)
            res.append(e)

        res = []
        thread = threading.Thread(target=target, args = (res,))
        thread.start()
        thread.join(self.timeout)

        if thread.is_alive():
            self.proc.terminate()
            thread.join()
            raise util.exceptions.TimeOutError(self.timeout)


        return res[0].decode("UTF8")

util.register.runners["cpp"] = Runner
util.register.runners["makefile"] = Runner