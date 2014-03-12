import os,sys
path = os.path.abspath("../../builder/cpp")
print (path)
sys.path.append(path)
from builder import CppBuilder

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
    def __init__ (self, path, timeout):
        self.proc = subprocess.Popen([path], shell= True, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        self.timeout = timeout

    def step(self, arg):

        def target(res):
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
            raise TimeOutError(self.timeout)
        if res[1]:
            raise RunError(res[1].decode("UTF8"))

        return res[0].decode("UTF8")


if __name__ == "__main__":
    b = CppBuilder()
    r = Runner(b.build("../../../test/tictactoe/cpp/main.cpp"), 1)
    print (r.step('---o-----'))