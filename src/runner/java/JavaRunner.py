import os

__author__ = 'stanis'

import subprocess
import threading

import util.register
import util.exceptions


class JavaRunner:
    def __init__ (self, src, timeout):
        path, fileName = os.path.split(src)
        self.proc = subprocess.Popen(["java -cp %s %s"%(path,fileName)], shell= True, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        self.timeout = timeout
        print(src)

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
            raise util.exceptions.TimeOutError(self.timeout)
        if res[1]:
            print (res[1])
            raise util.exceptions.RunError(res[1].decode("UTF8"))

        return res[0].decode("UTF8")

util.register.runners["java"] = JavaRunner

if __name__ == "__main__":
    r = JavaRunner("/home/stanis/test/Main")
    print (r.run('---o-----',1))