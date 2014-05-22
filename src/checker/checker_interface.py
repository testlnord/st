__author__ = 's'


class Checker_interface:
    def __init__(self, r1, r2):
        self.log_data = ""
        self.r1 = r1
        self.r2 = r2
        self.turn = 1
        self._win = 0
        self._pts1 = 0
        self._pts2 = 0

    def play(self):
        while True:
            self._step()
            if self._win != 0:
                if self._win == 1:
                    self._pts1 = 2
                elif self._win == 2:
                    self._pts2 = 2
                break
        if(self._win is 0):
            self._pts1 = 1
            self._pts2 = 1
        return self._win


    def log(self):
        return self.log_data


    def points(self):
        return self._pts1, self._pts2

    def _step(self):
        res = ''
        if self.turn == 1:
            try:
                res = self.r1.step(self.field)
            except:  # runner failed? runner lost!
                self._win = 2
                return
            turn = 2
        else:
            try:
                res = self.r2.step(self.field)
            except:  # see above. runner lost.
                self._win = 1
                return
            turn = 1
        try:
            i = int(res[0])
            j = int(res[2])
        except Exception:
            self._win = turn  #wrong output format
            return
        if self.field[(i) * 3 + (j)] != '-':
            self._win = turn  #wrong move (out of rules)
            return
        else:
            fld = list(self.field)
            fld[(i) * 3 + (j)] = self.figs[self.turn]
            self.field = ''.join(fld)
        self.log_data += "\n" + self.field
        self._check()
        self.turn = turn

    def _check(self):
       pass
