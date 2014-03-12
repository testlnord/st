
import subprocess

class BuildFailedException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)


class CppBuilder:
    path_to_output = "../../../out/"

    def build(self, src):
        out_path = self.path_to_output + "a.out"
        proc = subprocess.Popen(["g++ %s -o %s"%(src, out_path)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            raise BuildFailedException(err.decode("UTF8"))

        return out_path



if __name__ == "__main__":
    a = CppBuilder()
    try:
        executable = a.build("../../../test/tictactoe/cpp/main.cpp")
        print (executable)
    except BuildFailedException as e:
        print (e)
