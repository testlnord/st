import util.register
from checker_interface import Checker_interface

class Checker (Checker_interface):
    def __init__(self,r1,r2):
        super().__init__(r1,r2)
        self.field = "---------"

    def _gameover(self):
        return ("-" not in self.field)

    def get_field(self):
        result = "<table class=\"table-bordered game-field-table\">"
        for i in range(3):
            result += "<tr class=\"game-field-row\">"
            for j in range(3):
                result += "<td class=\"game-field-cell\">"+self.field[i*3+j]+"</td>"
            result += "</tr>"
        result += "</table><br/>"
        return result

    def log_entry(self, status=None, result=None):

        if status is not None:
            return "status: "+status +"<br/>"
        if result is not None:
            if result == "tide":
                return "tide<br/>"
            else:
                return "<b> player"+str(self._win)+" won</b><br/>"
        return "turn " + str(self.turn_counter)+"<br/>" + self.get_field()


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
            return "wrong move ("+str(res) + ")"
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

