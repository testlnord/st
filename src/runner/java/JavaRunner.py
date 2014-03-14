__author__ = 'stanis'

import subprocess
import threading

class UserProgramError(Exception):
    pass

class RunError(UserProgramError):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)

class TimeOutError(UserProgramError):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)


class Runner:
    def __init__ (self, src):
        sep=src.rfind("/")+1
        fileName = src[sep:]
        path=src[:sep]
        self.proc = subprocess.Popen(["java -cp %s %s"%(path,fileName)], shell= True, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE)


    def run(self, arg,timeout):

        def target(res):
            (o, e) = self.proc.communicate(bytes(arg, "UTF8"))
            res.append(o)
            res.append(e)

        res = []
        thread = threading.Thread(target=target, args = (res,))
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            self.proc.terminate()
            thread.join()
            raise TimeOutError(timeout)
        if res[1]:
            raise RunError(res[1].decode("UTF8"))

        return res[0].decode("UTF8")


if __name__ == "__main__":
    r = Runner("/home/stanis/test/Main")
    print (r.run('---o-----',1))