import util.register
import util.exceptions
import subprocess

class JavaBuilder:
    EXIT_OK = 0        # Compilation completed with no errors.
    EXIT_ERROR = 1,    # Completed but reported errors.
    EXIT_CMDERR = 2,   # Bad command-line arguments
    EXIT_SYSERR = 3,   # System error or resource exhaustion.
    EXIT_ABNORMAL = 4  #Compiler terminated abnormally

    def_src_name = "Main.java"
    def_out_name = "Main"
    def build(self, src, outPath):

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
            raise util.exceptions.BuildFailedException(err.decode("UTF8"))

        return fileName


util.register.builders["java"] = JavaBuilder()

if __name__ == "__main__":
    a = JavaBuilder()
    try:
        executable = a.build("../../Main.java","../../bin/")
        print (executable)
    except util.exceptions.BuildFailedException as e:
        print (e)