import sys, os
CUR_PATH=os.path.dirname(__file__)
#############################
##     DataBase paths      ##
#############################
db_path = os.path.abspath("./database/")
db_name = "Tournament.db"
db_creation_script = "create.sql"


#############################
##        Main paths       ##
#############################
cpp_builder_path = os.path.abspath("./builder/cpp")
java_builder_path = os.path.abspath("./builder/java")
cpp_runner_path = os.path.abspath("./runner/cpp")
java_runner_path = os.path.abspath("./runner/java")
checker_path = os.path.abspath("./checker")
out_path = os.path.abspath("../out/")

#############################
##      Server configs     ##
#############################
server_path = os.path.abspath("./server")
sender = os.path.abspath("./server/sender.py")
serverHost = "localhost"
serverPort = 8080
num_of_server_threads=10



#addind main paths to sys.path
sys.path.append(cpp_builder_path)
sys.path.append(java_builder_path)
sys.path.append(cpp_runner_path)
sys.path.append(java_runner_path)
sys.path.append(checker_path)
sys.path.append(server_path)
sys.path.append(db_path)

def sys_append (path):
    path = path[1:]
    sys.path.append(os.path.join(CUR_PATH,path))

sys_append(cpp_builder_path)
sys_append(java_builder_path)
sys_append(cpp_runner_path)
sys_append(java_runner_path)
sys_append(checker_path)
sys_append(server_path)
sys_append(db_path)





#############################
#    Stuff for start.py     #
#############################
start_list = [cpp_builder_path, java_builder_path, cpp_runner_path, java_runner_path, checker_path, db_path,server_path]


