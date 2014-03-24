import sys, os
#############################
##        Main paths       ##
#############################
cpp_builder_path = os.path.abspath("./builder/cpp")
java_builder_path = os.path.abspath("./builder/java")
cpp_runner_path = os.path.abspath("./runner/cpp")
java_runner_path = os.path.abspath("./runner/java")


checker_path = os.path.abspath("./checker")

server = os.path.abspath("./server/testServer.py")
sender = os.path.abspath("./server/sender.py")
serverHost = "localhost"
serverPort = 8080

db_path = os.path.abspath("./database")

#addind main paths to sys.path
sys.path.append(cpp_builder_path)
sys.path.append(java_builder_path)
sys.path.append(cpp_runner_path)
sys.path.append(java_runner_path)
sys.path.append(checker_path)


#############################
#    Stuff for start.py     #
#############################
start_list = [cpp_builder_path, java_builder_path, cpp_runner_path, java_runner_path, checker_path]

