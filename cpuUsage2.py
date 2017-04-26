#!/usr/bin/python

import multiprocessing
import subprocess
import time
import sys
import json
import os.path

PERIOD = int(sys.argv[1]) if ((len(sys.argv) > 1 and int(sys.argv[1]) > 20)) else 20
CORENUMBER = multiprocessing.cpu_count()



class Meassure:
        'This is a meassure'
        
        count = list()
        
        def __init__(self, coreUsage, processList):
            self.time = time.strftime("%d/%m/%Y %H:%M:%S")
            self.coreUsage = coreUsage
            self.processList = processList
                        
        def getCoreUsage(self):
            return self.coreUsage
            
        def getTime(self):
            return self.time


def getMeassure():
    'Runs top and get the data as a Meassure object'
    
    info = subprocess.check_output(['top','-b', '-d 5', '-n 2'])
    
    # Parser
    coreInfo = info.split("\n")[19+CORENUMBER:(2*CORENUMBER+19)]
    coreInfo = [i.split("usuario")[0].split(":")[1].strip() for i in coreInfo]

    processList = info.split("\n")[(2*CORENUMBER+23):-1]
    processList = [filter(None, i.split(" ")) for i in processList]
    processList = [(i[8], i[11]) for i in processList]
    # End Parser
    
    meassure = Meassure(coreInfo, processList)
    
    return meassure


def  main():
    
    # Initializing output files
    pwd = subprocess.check_output(["pwd"])[:-1]
    dump = pwd +"/dump.log"
    csv = pwd +"/coreUsage.csv"
    
    header = [("core "+str(i)) for i in range(0, CORENUMBER) ]
    header = ["time"] + header
    with open(csv,  "w") as csv_data:
        csv_data.write(", ".join(header))
        csv_data.write("\n")
        csv_data.close()
        
    with open(dump,  "w") as json_data:
        json_data.write("[]")
        json_data.close()

    # Launch the logger
    while(1):
        m = getMeassure()
        curDump = [m.__dict__]
        
        with open(dump) as json_data:
            storedDump = json.load(json_data)
            curDump = storedDump + curDump
            json_data.close()
        
        with open(dump, "w") as json_data:
            json_data.write(json.dumps(curDump))
            json_data.close()
            
        with open(csv, "a") as csv_data:
            body = [ i.replace(",", ".")  for i in m.getCoreUsage() ]
            body = m.getTime() + ", " + ", ".join(body)+"\n"
            csv_data.write(body)
            csv_data.close()
        
        
        time.sleep(PERIOD)




main()
