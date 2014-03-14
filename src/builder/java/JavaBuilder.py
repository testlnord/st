import os,sys
# path = os.path.abspath("./")
# path = os.path.abspath("./runner/java")
path = os.path.abspath("../../runner/java")
# print (path)
sys.path.append(path)
from JavaRunner import Runner



import subprocess

class BuildFailedException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)


class JavaBuilder:
    EXIT_OK = 0        # Compilation completed with no errors.
    EXIT_ERROR = 1,    # Completed but reported errors.
    EXIT_CMDERR = 2,   # Bad command-line arguments
    EXIT_SYSERR = 3,   # System error or resource exhaustion.
    EXIT_ABNORMAL = 4  #Compiler terminated abnormally


    def build(self, src,outPath):

        sep=src.rfind("/")+1
        fileName = src[sep:].replace(".java", "")

        proc = subprocess.Popen(["javac -d %s %s"%( outPath,src)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            print("return code=",proc.returncode)
            raise BuildFailedException(err.decode("UTF8"))

        return Runner(outPath.__add__(fileName))


if __name__ == "__main__":
    a = JavaBuilder()
    try:
        executable = a.build("../../Main.java","../../bin/")
        print (executable)
    except BuildFailedException as e:
        print (e)