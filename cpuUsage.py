#!/usr/bin/python

import multiprocessing
import subprocess
import time
import sys
import signal
import json

PERIOD = int(sys.argv[1]) if ((len(sys.argv) > 1 and int(sys.argv[1]) > 20)) else 20
CORENUMBER = multiprocessing.cpu_count()



class Meassure:
        'This is a meassure'
        
        count = list()
        
        def __init__(self, coreUsage, processList):
            self.time = time.strftime("%d/%m/%Y %H:%M:%S")
            self.coreUsage = coreUsage
            self.processList = processList
            
            Meassure.count.append(self)
            
        def getCoreUsage(self):
            return self.coreUsage
            


def getMeassure():
    'Runs top and get the data as a Meassure object'
    
    info = subprocess.check_output(['top','-b', '-d 5', '-n 2'])
    f = open( 'top', 'w' )
    f.write(info)
    f.write("\n")
    
    # Parser
    coreInfo = info.split("\n")[19+CORENUMBER:(2*CORENUMBER+19)]
    coreInfo = [i.split("usuario")[0].split(":")[1].strip() for i in coreInfo]

    processList = info.split("\n")[(2*CORENUMBER+23):-1]
    processList = [filter(None, i.split(" ")) for i in processList]
    processList = [(i[8], i[11]) for i in processList]
    # End Parser
    
    meassure = Meassure(coreInfo, processList)
    
    return meassure

def dumpData():
    meassures = [i.__dict__ for i in Meassure.count]    
    f = open( 'dump.log', 'w' )
    f.write(json.dumps(meassures))
    f.close()
    print("Generated the complete dump on " + str(subprocess.check_output(["pwd"]))[:-1]+"/dump.log")

def exportDataAsCSV():
    meassures = [i.getCoreUsage() for i in Meassure.count]
    meassures = [([(j).replace(",", ".") for j in i]) for i in meassures]
    header = [("core "+str(i)) for i in range(0, CORENUMBER) ]
    body = [(",".join(i)) for i in meassures]
    f = open( 'coreUsage.csv', 'w' )
    f.write(" ".join(header))
    f.write("\n")
    f.write("\n".join(body))
    f.close()
    print("Generated a csv with basic info in " + str(subprocess.check_output(["pwd"]))[:-1]+"/coreUsage.csv")

def signal_handler(signal, frame):
    print('\n\nDumping data...')

    dumpData()
    
    exportDataAsCSV()
    
    print('Execution finished! Bye.')
    sys.exit(0)

def  main():
    signal.signal(signal.SIGINT, signal_handler)
    
    while(1):
        getMeassure()
        print("go")
        time.sleep(PERIOD)
        
        
        
        
main()
