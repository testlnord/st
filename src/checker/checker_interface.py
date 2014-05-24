__author__ = 's'
import sys

from util.exceptions import TimeOutError

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

class Checker_interface:
    def __init__(self, r1, r2):
        self.field = ""
        self.log_data = ""
        self.r1 = r1
        self.r2 = r2
        self.turn = 1
        self._win = 0
        self._pts1 = 0
        self._pts2 = 0
        self.turn_counter = 0

    def play(self):
        while True:
            status = self._step()
            self.turn_counter += 1
            self.log_data += self.log_entry()
            if self._win != 0:
                if self._win == 1:
                    self._pts1 = 2
                elif self._win == 2:
                    self._pts2 = 2
                break

        self.log_data += self.log_entry(status=status)
        if(self._win is 0):
            self._pts1 = 1
            self._pts2 = 1
            self.log_data += self.log_entry(result="tide")
            return self._win
        self.log_data += self.log_entry(result="win")
        tprint(self.log_data)
        return self._win

    def log_entry(self, status=None, result=None):
        if status is not None:
            return "\n status: "+status
        if result is not None:
            if result == "tide":
                return "tide"
            else:
                return "\n player"+str(self._win)+" won"
        return "\nturn " + str(self.turn_counter)+"\n" + self.get_field()

    def get_field(self):
        return self.field

    def log(self):
        return self.log_data


    def points(self):
        return self._pts1, self._pts2

    def _step(self):
        res = ''
        self.curr_turn = self.turn

        if self.turn == 1:
            try:
                res = self.r1.step(self.field)
            except TimeOutError:
                self._win = 2
                return "time limit"
            except:  # runner failed? runner lost!
                self._win = 2
                return "runtime err"
            self.turn = 2
        else:
            try:
                res = self.r2.step(self.field)
            except TimeOutError:
                self._win = 1
                return "time limit"
            except:  # see above. runner lost.
                self._win = 1
                return "runtime err"
            self.turn = 1

        return self._check(res)




    def _check(self,res):
       pass
