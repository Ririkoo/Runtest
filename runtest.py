#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import re
import glob
import subprocess

class Tester:
    SERVERDIR="/home/pzhe/Desktop/planner/Planner-release-2.07-src/bin" #Server Dir
    CLIENTDIR="/home/pzhe/Desktop/planner/Planner-release-2.07-src/bin" #Client Dir

    def __init__(self, mode, stage, probdir):
        self.probdir = probdir
        self.mode = mode
        self.stage = stage
        self.dirmap = None

    def conftests(self, teams):
        self.dirmap = teams

    def runtest(self):
        cnt=1
        while cnt<=self.probdir:
            servercmd = "./cserver -td ../tests/sim@home13.demo/stage.II \
            -mode {0}  -to 10000 -test {2} -eval ../lib/libasp -log log_{0}_{1} ".format(self.mode, self.stage, cnt)
            print "Run Server  ", servercmd

            os.chdir(self.SERVERDIR)
            if not os.path.exists("log_{0}_{1}".format(self.mode, self.stage)):
                os.mkdir("log_{0}_{1}".format(self.mode, self.stage))
            os.system("pkill cserver")
            cserver = subprocess.Popen(servercmd,shell=True)
            #os.system(servercmd)
            cnt=cnt+1
            for client in self.dirmap:
                os.chdir(self.CLIENTDIR)
                os.system("sleep 4")
                print "\n################Now Testing... {0}".format(client)
                os.chdir(client)
                os.system("chmod +x " + self.dirmap[client])
                os.system("./" + self.dirmap[client])
                cserver.kill()
                os.system("kill -9 $(ps ax|grep 'cserver'|grep -v 'grep'|awk '{print $1}') 1>/dev/null 2>/dev/null")
                print "\n################ Test Over"


    def genlogs(self):
        print "\n\n################################################################"
        print "Test Mode: {0}, Stage:{1}".format(self.mode, self.stage)
        print "The Results:"
        os.chdir(self.CLIENTDIR)
        outf = open("{0}_{1}_all.txt".format(self.mode, self.stage), 'w')
        os.chdir(self.SERVERDIR + "/log_{0}_{1}".format(self.mode, self.stage))
        for f in glob.glob("*.log"):
            tscore = 0
            for line in open(f):
                if line.startswith("TeamName:"):
                    teamname = line.split(':')[1].strip()
                elif line.startswith("Total Score"):
                    tscore = line.split(':')[1].strip()
            outf.write("{0}\t:{1}\n".format(teamname, tscore))
            print "{0}\t:{1}".format(teamname, tscore)
        outf.close()
        print "################################################################"

    def testall(self):
        self.runtest()
        #self.genlogs()

if __name__ == '__main__':
    ts = Tester("it", 1, "")
    teams = {"test": "pytest.py"
    }
    ts.conftests(teams)
    ts.testall()
