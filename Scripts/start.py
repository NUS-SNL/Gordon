import csv
import subprocess
import tcpClassify
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
import time
import re
import sys

urlFilePath = "./alexa-sites/unfinished-urls.csv" #./retestLinks.csv"
urlFile = open(urlFilePath)
csvReader = csv.reader(urlFile)
urlInfos = list(csvReader)
#print(urlInfos)
urlFile.close()

#measure 150 websites from the strat point.
start = int(sys.argv[1])
i = start

while i < start + len(urlInfos):
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&  CURRENT OFFSET   ===", i, "=== &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    analysisResult = open("./domainResult.csv")
    if urlInfos[i][1] not in analysisResult.read().splitlines():
        analysisResult.close()
        if urlInfos[i][3] == '':
            #print(urlInfos[i][1])
            
            targetURL = "http://" + urlInfos[i][2]
            print("===================================================>", targetURL, "\n================", urlInfos[i][0], urlInfos[i][1], urlsInfos[i][2])

            try:
                response = subprocess.check_output(
                    ['ping', '-c', '1', urlInfos[i][1]],
                    stderr=subprocess.STDOUT,  # get all output
                    universal_newlines=True  # return string not bytes
                )
            except subprocess.CalledProcessError:
                response = None

            if response == None:
                pingTime = -1
            else:
                pingTime = float(re.search('time=.*', response).group().replace(" ms", '')[5:])

            if int(pingTime/2) >= 50:
                delayTime = 1
            elif pingTime == -1:
                delayTime = 50
            else:
                delayTime = 50 - int(pingTime/2)

            print(targetURL, delayTime)
            
            try:
                subprocess.call(["mm-delay "+ str(delayTime) + " ./multi-launch.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
                #subprocess.call(["./multi-launch.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
            except Exception as e:
                print(e)
            finally:
                subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
                subprocess.call(["cp ../Data/windows.csv ../Windows/"+urlInfos[i][1]+".csv"], shell=True, executable="/bin/bash")
                #subprocess.call(["exit"], shell=True, executable="/bin/bash")
            
            print("over")
            type = tcpClassify.classify()
            csvOutputFile = open("./analysisResult.csv", 'a')
            csvWriter = csv.writer(csvOutputFile)
            csvWriter.writerow([urlInfos[i][1], type, targetURL])
            csvOutputFile.close()
            csvOutputFile = open("./domainResult.csv", 'a')
            csvWriter = csv.writer(csvOutputFile)
            csvWriter.writerow([urlInfos[i][1]])
            csvOutputFile.close()
            i += 1
            time.sleep(10)

        else:
            """
            while True:
                print(urlInfos[i][1], urlInfos[i][2:])
                try:
                    request = Request(urlInfos[i][2])
                    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0')
                    html = urlopen(request)
                except HTTPError as e:
                    if e.code == 404:
                        print(e)
                        i += 1
                except Exception as e:
                    print(e)
                    i += 1
                else:
                    break
            """
        
            j = i

            try:
                response = subprocess.check_output(
                    ['ping', '-c', '1', urlInfos[i][1]],
                    stderr=subprocess.STDOUT,  # get all output
                    universal_newlines=True  # return string not bytes
                )
            except subprocess.CalledProcessError:
                response = None

            if response == None:
                pingTime = -1
            else:
                pingTime = float(re.search('time=.*', response).group().replace(" ms", '')[5:])

            if int(pingTime/2) >= 50:
                delayTime = 1
            elif pingTime == -1:
                delayTime = 50
            else:
                delayTime = 50 - int(pingTime/2)

            print(urlInfos[i][3], delayTime)

            try:
                subprocess.call(["mm-delay " + str(delayTime) + " ./multi-launch.sh '"+urlInfos[i][2]+"' 10"], shell=True, executable='/bin/bash')
                #subprocess.call(["./multi-launch.sh "+urlInfos[j][2]+" 10"], shell=True, executable='/bin/bash')
            except Exception as e:
                print(e)
            finally:
                subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
                subprocess.call(["cp ../Data/windows.csv ../Windows/"+urlInfos[i][0]+"-"+urlInfos[i][1]+".csv"], shell=True, executable="/bin/bash")
                #subprocess.call(["exit"], shell=True, executable="/bin/bash")
            
            type = tcpClassify.classify()
            #type = "undecided"
            csvOutputFile = open("./analysisResult.csv", 'a')
            csvWriter = csv.writer(csvOutputFile)
            csvWriter.writerow([urlInfos[i][1], type, urlInfos[j][3]])
            csvOutputFile.close()
            csvOutputFile = open("./domainResult.csv", 'a')
            csvWriter = csv.writer(csvOutputFile)
            csvWriter.writerow([urlInfos[i][1]])
            csvOutputFile.close()
            while urlInfos[j][1] == urlInfos[i][1]:
                j+=1
            i = j
            time.sleep(10)
            #input()
            
            """
            while urlInfos[j][0] == urlInfos[i][1]:
                try:
                    subprocess.call(["./multi-launch.sh "+urlInfos[j][2]], shell=True, executable='/bin/bash')
                except Exception as e:
                    print(e)
                finally:
                    subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
                
                type = tcpClassify.classify()
                csvOutputFile = open("./analysisResult.csv", 'a')
                csvWriter = csv.writer(csvOutputFile)
                csvWriter.writerow([urlInfos[i][1], type, urlInfos[j][2]])
                csvOutputFile.close()
                csvOutputFile = open("./domainResult.csv", 'a')
                csvWriter = csv.writer(csvOutputFile)
                csvWriter.writerow([urlInfos[i][1]])
                csvOutputFile.close()
                input()
                j += 1
            #targetURL = urlInfos[i][2]
            i = j
            """

    else:
        analysisResult.close()
        print("Already Done, Next...")
        i += 1
    
    
    
    #input()

