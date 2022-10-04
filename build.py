import glob
import os
import shutil
import subprocess
import sys
from distutils.command.build_ext import Extension
from distutils.command.install import install
from pathlib import Path


class Track(install):
    """A class that enables the compilation of LIGGGHTS-PUBLIC from github"""

    def do_pre_install_stuff(self):

        files = glob.glob(os.path.join("cc", "src", "*.cpp"))

        count = 0
        os.chdir(os.path.join("cc", "src"))
        self.spawn(cmd=["make", "clean-all"])

        print("Compiling LIGGGHTS as a shared library\n")

        for path in self.execute(cmd="make mpi"):
            count += 1
            self.print_progress(
                count, prefix="Progress:", suffix="Complete", total=len(files) * 2.05
            )

        self.spawn(cmd=["make", "-f", "Makefile.shlib", "mpi"])
        sys.stdout.write("\nInstallation of LIGGGHTS-PUBLIC complete\n")
        shutil.copy("libliggghts.so", "../../liggghts", follow_symlinks=True)

    def execute(self, cmd, cwd="."):
        popen = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, universal_newlines=True, cwd=cwd, shell=True
        )

        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line

        popen.stdout.close()
        return_code = popen.wait()

        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    def print_progress(self, iteration, prefix="", suffix="", decimals=1, total=100):
        """
        Call in a loop to create terminal progress bar
        @params:
                iteration   - Required  : current iteration (Int)
                total       - Required  : total iterations (Int)
                prefix      - Optional  : prefix string (Str)
                suffix      - Optional  : suffix string (Str)
                decimals    - Optional  : positive number of decimals in percent complete (Int)
                bar_length  - Optional  : character length of bar (Int)
        """
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        sys.stdout.write("\r %s%s %s" % (percents, "%", suffix))
        sys.stdout.flush()

    def run(self):
        self.do_pre_install_stuff()


def build(setup_kwargs):
    setup_kwargs.update(
        ext_modules=[
            Extension(
                "liggghts",
                include_dirs=["cc/include"],
                sources=glob.glob(os.path.join("cc", "src", "*.cpp")),
            ),
        ],
        cmdclass={
            "build_ext": Track,
        },
    )
