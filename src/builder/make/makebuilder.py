__author__ = 'arkady'


import os
import zipfile
import util.register
import util.exceptions
import subprocess


class MakeBuilder:
    def_out_name = "main"
    def_src_name = "main.zip"

    def build(self, srczip, dst):
        #out_path = os.path.join(dst, self.def_out_name)
        if not zipfile.is_zipfile(srczip):
            raise util.exceptions.BuildFailedException("Bad zip archive file.")
        src = zipfile.ZipFile(srczip)
        src.extractall(dst)
        proc = subprocess.Popen(["make"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                cwd=dst)
        (out, err) = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            raise util.exceptions.BuildFailedException(err.decode("UTF8"))
        return self.def_out_name


util.register.builders["makefile"] = MakeBuilder()