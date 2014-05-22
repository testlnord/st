import util.register
from checker_interface import Checker_interface

class Checker (Checker_interface):
    def __init__(self):
        super().__init__()
        self.field = "---------"


    figs = {1: 'x', 2: 'o'}
    def _check(self,res):
        try:
            i = int(res[0])
            j = int(res[2])
        except Exception:
            self._win = self.turn  #wrong output format
            return "wrong output"
        if self.field[(i) * 3 + (j)] != '-':
            self._win = self.turn  #wrong move (out of rules)
            return "wrong move"
        else:
            fld = list(self.field)
            fld[(i) * 3 + (j)] = self.figs[self.curr_turn]
            self.field = ''.join(fld)

        if self.field[0:3] == 'xxx' or \
                        self.field[3:6] == 'xxx' or \
                        self.field[6:] == 'xxx' or \
                        self.field[0::3] == 'xxx' or \
                        self.field[1::3] == 'xxx' or \
                        self.field[2::3] == 'xxx' or \
                        self.field[0::4] == 'xxx' or \
                        self.field[2:7:2] == 'xxx':
            self._win = 1
        elif self.field[0:3] == 'ooo' or \
                        self.field[3:6] == 'ooo' or \
                        self.field[6:] == 'ooo' or \
                        self.field[0::3] == 'ooo' or \
                        self.field[1::3] == 'ooo' or \
                        self.field[2::3] == 'ooo' or \
                        self.field[0::4] == 'ooo' or \
                        self.field[2:7:2] == 'ooo':
            self._win = 2

        return "gg"


util.register.checkers["tictactoe"] = Checker

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
    print(winner)

