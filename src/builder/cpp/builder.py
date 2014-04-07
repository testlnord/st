import os
import util.register
import util.exceptions
import subprocess


class CppBuilder:
    def_out_name = "a.out"
    def_src_name = "main.cpp"
    def build(self, src, dst):
        out_path = os.path.join(dst, self.def_out_name)
        proc = subprocess.Popen(["g++ %s -o %s"%(src, out_path)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            raise util.exceptions.BuildFailedException(err.decode("UTF8"))
        return self.def_out_name


util.register.builders["cpp"] = CppBuilder()

if __name__ == "__main__":
    a = CppBuilder()
    try:
        executable = a.build("../../../test/tictactoe/cpp/main.cpp", "")
        print (executable)
    except util.exceptions.BuildFailedException as e:
        print (e)
