from mcstatus import JavaServer
import threading
import time
import requests
import asyncio
import os

file=input("Do you need to download an IPs file (y/n): ")
if file=="y" or file=="Y":
    os.popen("curl -f https://poopenheimer.tk/static/files/ips.txt -o ips.txt")
else:
    pass
version=input("version to search for (leave blank for all): ")
threads = int(input('How many threads so you want to use? (Recommended 2500- more threads may fuck up your bandwith): '))
time.sleep(2)

masscan = []
url="https://poopenheimer.tk/peer"
inputfile = "ips.txt"
fileHandler = open (inputfile, "r")
listOfLines = fileHandler.readlines()
fileHandler.close()

for line in listOfLines:
    if line.strip()[0] != "#":
        masscan.append(line.strip().split(' ',4)[3])

def split_array(L,n):
    return [L[i::n] for i in range(n)]

if len(masscan) < int(threads):
    threads = len(masscan)

split = list(split_array(masscan, threads))

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting Thread " + self.name)
        time.sleep(5)
        asyncio.run(print_time(self.name))
        print ("Exiting Thread " + self.name)

async def print_time(threadName):
    for z in split[int(threadName)]:
        ip = z
        server = JavaServer(ip,25565)
        try:
            status=server.status()
            query = server.query()
            try:
                server = JavaServer(ip,25565)
                print("[QUERY} Found server: " + ip + " " + query.software.version + " " + str(query.players.online))
                post = {"IP": ip,"MOTD":query.motd,"Version": query.software.version, "Players": str(query.players.online)+"/"+str(query.players.max), "Latency": status.latency,"playerlist":query.players.names,"Found_with":"QUERY","plugin_list":query.software.plugins,"P2W":"False"}
                requests.post(url,json=post)
            except:
                try:
                    print("[STATUS] Found server: " + ip + " " + status.version.name + " " + str(status.players.online))
                    post = {"IP": ip, "Version": status.version.name, "Players": str(status.players.online)+"/"+str(status.players.max), "Latency": status.latency,"Found_with":"STATUS","P2W":"False"}
                    requests.post(url,json=post)
                except:
                    pass
        except:
            pass

for x in range(threads):
    thread = myThread(x, str(x)).start()