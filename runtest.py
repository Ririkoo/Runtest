#!/usr/bin/env python


import os
import re
import glob
import subprocess
import time

class Tester:
    SERVERDIR="" #Server Dir
    CLIENTDIR="" #Client Dir

    def __init__(self, mode, stage, pronum):
        self.pronum = pronum
        self.mode = mode
        self.stage = stage
        self.dirmap = None

    def conftests(self, teams):
        self.dirmap = teams

    def runtest(self):
        cnt=1
        totscore=0
        dircreat="mkdir log_{0}_{1}/".format(self.mode, self.stage)
        os.chdir(self.SERVERDIR)
        os.system("cp -p ../res/iclingo ../res/*.lp .")
        if not os.path.exists("log/log_{0}_{1}".format(self.mode, self.stage)):
         	os.system(dircreat)
        while cnt<=self.pronum:
            servercmd = "./cserver -td ../tests/it-stage1 \
            -mode {0}  -to 5000 -test {2} -eval ../lib/libasp -log log_{0}_{1}/{2} ".format(self.mode, self.stage, cnt)
            os.chdir(self.SERVERDIR)
            if not os.path.exists("log_{0}_{1}/{2}".format(self.mode, self.stage,cnt)):
                os.mkdir("log_{0}_{1}/{2}".format(self.mode, self.stage,cnt))
            os.system("pkill cserver")
            cserver = subprocess.Popen(servercmd,shell=True)
            
            for client in self.dirmap:
                os.chdir(self.CLIENTDIR)
                os.system("sleep 3")
                print "\n################Now Testing... {0}".format(client)
                #os.chdir(client)
                os.system("chmod +x " + self.dirmap[client])
                os.system("./" + self.dirmap[client])
                cserver.kill()
                os.system("kill -9 $(ps ax|grep 'cserver'|grep -v 'grep'|awk '{print $1}') 1>/dev/null 2>/dev/null")
                os.system("pkill "+ self.dirmap[client])
                print "\n################ Test Over"

            os.chdir(self.SERVERDIR + "/log_{0}_{1}/{2}".format(self.mode, self.stage,cnt))
            for f in glob.glob("*.log"):
            	tscore = 0
            	for line in open(f):
            	    if line.startswith("TeamName:"):
            	     teamname = line.split(':')[1].strip()
            	    elif line.startswith("# Score:"):
            	     tscore = line.split(':')[1].strip()
            totscore=totscore+int(tscore)
            if cnt == self.pronum :  
            	print "{0} : \t  {1}".format(teamname, totscore)
            	outf = open("../{2}_{0}_{1}_res.txt".format(self.mode, self.stage,self.dirmap[client]), 'w')
            	outf.write("{0}\t:{1}\n".format(teamname, totscore))
            	outf.close()
            cnt=cnt+1
  
        

    def testall(self):
        self.runtest()

if __name__ == '__main__':
    ts = Tester("it", 1, "")
    teams = {"test": "pytest.py"
    }
    ts.conftests(teams)
    ts.testall()
