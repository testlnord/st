import database.db
import support
mdb = database.db.DB()
mdb.addUser("asdf", "")
mdb.addUser("qwer", "")
mdb.addTournament("t1", "tictactoe", 2, "", "")
mdb.addSolution(1, 1, 0, "", "cpp", "a.out")
mdb.addSolution(2, 1, 0, "", "cpp", "a.out")
support.run(mdb, "t1")
print(mdb.getRunResult(1))