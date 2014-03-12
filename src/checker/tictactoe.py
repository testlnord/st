import sys, os
path = os.path.abspath("../builder/cpp")
print (path)
sys.path.append(path)
path = os.path.abspath("../runner/cpp")
print (path)
sys.path.append(path)

from builder import CppBuilder, BuildFailedException
from runner import Runner, UserProgramError

class Checker:
    figs = {1:'x', 2:'o'}
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        self.field = "---------"
        self.turn = 1
        self._win = 0

    def play(self):
        while True:
            self._step()
            if self._win != 0:
                break
        return self._win

    def _step(self):
        res = ''
        if self.turn == 1:
            res = self.r1.step(self.field)
            turn = 2
        else:
            res = self.r2.step(self.field)
            turn = 1
        try:
            i = int(res[0])
            j = int(res[2])
        except Exception:
            self._win = turn #wrong output format
            return
        if self.field[(i)*3+(j)] != '-':
            self._win = turn #wrong move (out of rules)
            return
        else:
            fld = list(self.field)
            fld[(i)*3+(j)] = self.figs[self.turn]
            self.field = ''.join(fld)
        self._check()
        self.turn = turn

    def _check(self):
        if  self.field[0:3] == 'xxx' or\
            self.field[3:6] == 'xxx' or\
            self.field[6:] == 'xxx' or\
            self.field[0::3] == 'xxx' or\
            self.field[1::3] == 'xxx' or\
            self.field[2::3] == 'xxx' or\
            self.field[0::4] == 'xxx' or\
            self.field[2:7:2] == 'xxx':
            self._win = 1
        elif self.field[0:3] == 'ooo' or\
            self.field[3:6] == 'ooo' or\
            self.field[6:] == 'ooo' or\
            self.field[0::3] == 'ooo' or\
            self.field[1::3] == 'ooo' or\
            self.field[2::3] == 'ooo' or\
            self.field[0::4] == 'ooo' or\
            self.field[2:7:2] == 'ooo':
            self._win = 2

if __name__ == "__main__":
    winner = 0
    b1 = CppBuilder()
    b1.path_to_output = "../../out/"
    r1 = Runner(b1.build("../../test/tictactoe/cpp/main.cpp"), 1)
    b2 = CppBuilder()
    b2.path_to_output = "../../out/"
    r2 = Runner(b2.build("../../test/tictactoe/cpp/main.cpp"), 1)
    c = Checker(r1, r2)
    winner = c.play()
    print (winner)
