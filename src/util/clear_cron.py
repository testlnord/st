__author__ = 's'
import os

script = "run_runner.py"
cur_cron = os.popen('crontab -l > current_crontab.txt')
cur_cron.read()
cur_cron.close()
fi = open('current_crontab.txt', 'r')
lines = fi.readlines()
fi.close()
fo = open('current_crontab.txt', 'w')

for line in lines:
     if script not in line:
        fo.write(line)
fo.close()
load = os.popen('crontab current_crontab.txt')
load.read()
load.close()
os.remove("current_crontab.txt")