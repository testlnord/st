import util.register
import util.exceptions
import subprocess


class CppBuilder:
    path_to_output = "../../../out/"

    def build(self, src, dst):
        out_path = dst + "a.out"
        proc = subprocess.Popen(["g++ %s -o %s"%(src, out_path)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            raise util.exceptions.BuildFailedException(err.decode("UTF8"))
        return util.register.runners["cpp"](out_path)


util.register.builders["cpp"] = CppBuilder()

if __name__ == "__main__":
    a = CppBuilder()
    try:
        executable = a.build("../../../test/tictactoe/cpp/main.cpp", "")
        print (executable)
    except util.exceptions.BuildFailedException as e:
        print (e)
