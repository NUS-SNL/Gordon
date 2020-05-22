import numpy as np 
import warnings
#from matplotlib import pyplot as plt
import sys
import os
plotting = False
url_map = {}

def classify(tcpFile): #, filename, plotPath):
    global plotting
    global url_map
    answer = {}
    warnings.filterwarnings("ignore")
    try:
        tcpDatas = np.loadtxt(fname=tcpFile, delimiter=' ', usecols=(0,2))
        tcpDatas[:,[0,-1]] = tcpDatas[:,[-1, 0]]
        tcpRounds = tcpDatas[:,0]
        tcpWindows = tcpDatas[:,-1]
        tcpPackets = list(np.loadtxt(fname=tcpFile, delimiter=' ', usecols=(1)))
        """
	if(plotting):
            plt.title("Congestion Window vs RTT")
            plt.xlabel("RTT Number")
            plt.ylabel("Congestion Window")
            plt.plot(tcpRounds, tcpWindows, 'b', label=((url_map[int(filename.split('.')[0])]).split('/')[2]))
            plt.legend()
            plt.savefig(plotPath+'/'+ filename.split('.')[0] + '_' + (url_map[int(filename.split('.')[0])]).split('/')[2]+'.png')
            plt.close()
    	"""
    except Exception as e:
        answer['method'] = "short_flow_no_data"
        return answer['method']
    
    def getBeta(window1, window2):
        return round((window2/window1)+0.0005, 3)
    tcpLossPoints = []
    tcpBeta = 0
    tcpBetaSecond = 0

    for i in range(len(tcpDatas)-1):
        if tcpWindows[i] > 80:
            tcpLossPoints.append(i)
            tcpBeta =  round(getBeta(tcpWindows[i], tcpWindows[i+1]),1)
            try:
                tcpBetaSecond = round(getBeta(tcpWindows[i+1], tcpWindows[i+2]),1)
            except Exception as e:
                # print("short flow")
                answer['method'] = "short_flow_data_low_after_backoff"
                return answer['method']
            break
    if tcpBeta>=1 and tcpBetaSecond<1 and tcpBetaSecond>0:
        tcpBeta = tcpBetaSecond
        tcpLossPoints[0]=tcpLossPoints[0]+1


    def checkTypeIII():
        for i in range(len(tcpWindows)-1,0,-1):
            if tcpWindows[i] < 10:
                continue 
            elif tcpWindows[i-1] - tcpWindows[i] > 5:
                #print(tcpWindows[i-1], tcpWindows[i])
                try:
                    beforeStep = []
                    afterStep = []
                    for j in range(1,6):
                        beforeStep.append(tcpWindows[i-j])
                    for j in range(0,5):
                        afterStep.append(tcpWindows[i+j])
                    #print(beforeStep, afterStep)
                    # print(np.std(beforeStep), np.std(afterStep))
                    if np.std(beforeStep) < 2 and np.std(afterStep) <2:
                        if 65<np.average(afterStep) <75 and 95<np.average(beforeStep) <115:
                            return False
                        elif 95<np.average(afterStep) <115:
                            return False
                        else:
                            return True
                    return False
                except Exception as e:
                    return False
                
    if len(tcpLossPoints) == 0:
        #print("unknown")
        if checkTypeIII():
            # print("Type III")
            answer['method'] = "Type_III"
            return answer['method']
        # print("unknown never go up 80")
        answer['method'] = "unknown_never_go_up_80"
        return answer['method']

    answer['Beta'] = tcpBeta
    # print("Beta", tcpBeta)
    if tcpBeta < 1:
        for i in range(tcpLossPoints[0]+1, len(tcpDatas)-1):
            if tcpWindows[i] > tcpWindows[i+1]:
                if getBeta(tcpWindows[i], tcpWindows[i+1]) <= 0.3:
                    tcpLossPoints.append(i)
    
    for i in range(len(tcpWindows)-1,0,-1):
        x = tcpWindows[i]
        y = tcpWindows[i-1]
        if x>y and y != 0 and x>10 and y >10:
            #print(i)
            tcpLossPoints.append(i)
            tcpLossPoints[1]=i
            break

    if len(tcpLossPoints) > 1:
        tcpWindowAvoidCongestion = tcpWindows[tcpLossPoints[0]+1:tcpLossPoints[1]+1]
    else:
        tcpWindowAvoidCongestion = tcpWindows[tcpLossPoints[0]+1:]
    answer['TCP Windows Congestion Avoid'] = tcpWindowAvoidCongestion
    # print("TCP Windows Congestion Avoid", tcpWindowAvoidCongestion)

    lossValue = tcpWindows[tcpLossPoints[0]]
    stableIndex = []
    stable = []
    backoffIndex = []
    backoff = []
    probeIndex = []
    probe = []
    stableRange = 3
    
    for i in range(len(tcpWindowAvoidCongestion)):
        if tcpWindowAvoidCongestion[i] < lossValue - stableRange:
            backoffIndex.append(i)
        elif tcpWindowAvoidCongestion[i] > lossValue + stableRange:
            probeIndex.append(i)
        else:
            stableIndex.append(i)
    
    def findLargestInterval(interval):
        if len(interval) == 0:
            return -1,-1
        startPoint = [interval[0]]
        endPoint = []
        if len(interval) == 1:
            endPoint.append(interval[0])
        for i in range(1,len(interval)):
            if interval[i] != interval[i-1]+1:
                endPoint.append(interval[i-1])
                startPoint.append(interval[i])
            if i == len(interval) -1:
                endPoint.append(interval[i])
        maxLength = -1
        maxIndex = 0
        #print(startPoint)
        #print(endPoint)
        for i in range(len(endPoint)):
            length = endPoint[i] - startPoint[i]
            if length > maxLength:
                maxLength = length
                maxIndex = i
        #print(maxIndex,'max')
        #print(startPoint[0],endPoint[0])
        return startPoint[maxIndex],endPoint[maxIndex]

    #print(backoffIndex)
    s,e = findLargestInterval(backoffIndex)
    if(s==-1):
        backoff = None
    else:
        backoff = list(tcpWindowAvoidCongestion[s:e+1])
    #print(tcpWindowAvoidCongestion[s:e+1])
    #print(stableIndex)
    s,e = findLargestInterval(stableIndex)
    if(s==-1):
        stable = None
    else:
        stable = list(tcpWindowAvoidCongestion[s:e+1])
    #print(tcpWindowAvoidCongestion[s:e+1])
    #print(probeIndex)
    s,e = findLargestInterval(probeIndex)
    if(s==-1):
        probe = None
    else:
        probe = list(tcpWindowAvoidCongestion[s:e+1])
    #print(tcpWindowAvoidCongestion[s:e+1])
    answer['backoff'] = backoff
    answer['stable'] = stable
    answer['probe'] = probe
    # print("backoff:", backoff)
    # print("stable:", stable)
    # print("probe:", probe)

    def isConcave(interval, significant=-2, flag="cubic"):
        try:
            dy = np.gradient(interval)
            d2y = np.gradient(dy)
        except Exception as e:
            return False
        negPercentage = len(list(filter(lambda x:x<=-0.5, d2y))) / len(d2y)
        #print(dy)
        #print(sum(dy))
        #print(dy, sum(dy)/len(dy))
        #print(d2y)
        #print(negPercentage)
        #print(d2y,sum(d2y))
        #print(significant)
        #print(sum(d2y)/len(d2y))
        #if negPercentage >= 0.5:
        """
        flag = 0
        for i in d2y:
            if i <=-1:
                flag=1
        """
        #print(flag)
        
        if flag=="bic":
            if sum(d2y) <= -5:
                return True
            else:
                return False
        
        if sum(d2y) <= significant and sum(dy)/len(dy)>=2 or sum(dy)/len(dy)>=1.9:  #or sum(d2y)/len(d2y)<-0.1:
            #print("here")
            return True
        else:
            return False

    def isConvex(interval):
        try:
            dy = np.gradient(interval)
            d2y = np.gradient(dy)
        except:
            return True
        posPercentage = len(list(filter(lambda x:x>0, d2y))) / len(d2y)
        #print(d2y)
        #print(sum(d2y))
        #print(posPercentage)
        #if posPercentage >= 0.5:
        #if sum(d2y) >= 0:
        if len(dy)>3:
            if sum(dy)/len(dy)>1:
                return True
            else:
                return False
        return True

    def isStable(interval):
        dy = np.gradient(interval)
        d2y = np.gradient(dy)
        # print(dy)
        # print(sum(dy))
        # print(d2y)
        # print(sum(d2y))
    #isStable(stable)
    #print("backoff concave:", isConcave(backoff))
    #print("probe canvex:", isConvex(probe))
    #print(backoff)
    def isCUBIC():
        if backoff != None and stable != None and probe != None and tcpBeta < 1:
            if isConcave(backoff, significant=-2) and isConvex(probe):
                if len(stable) >= 3:
                    #print("here")
                    return True
        elif backoff != None and stable != None and probe==None and tcpBeta < 1:
            if isConcave(backoff):
                if len(stable) >= 3:
                    #print(stable)
                    return True
                else:
                    if isConcave(backoff):
                        return True
        elif backoff != None and stable==None and probe==None and tcpBeta < 1:
            #print("here")
            if isConcave(backoff):
                #print("here")
                if len(backoff)>3:
                    return True
        return False

    def isBIC():
        if stable == None and probe == None and tcpBeta < 1:
            if isConcave(backoff, flag="bic"):
                return True
        elif probe == None and stable!=None and backoff != None and tcpBeta < 1:
            if isConcave(backoff, flag="bic"):
                return True
        return False

    def isHTCP():
        if backoff != None and probe != None and tcpBeta < 1:
            if stable == None or len(stable) <3:
                if len(probe) > 3 and tcpBeta < 1 and len(backoff)>7:
                    return True
        return False

    tcpIncreRate = []
    for i in range(1, len(tcpWindowAvoidCongestion)):
        tcpIncreRate.append(round(tcpWindowAvoidCongestion[i] / tcpWindowAvoidCongestion[i-1], 4))
    averageRate = np.mean(tcpIncreRate)
    answer['averageRate'] = averageRate
    # print("average rate", averageRate)

    averageIncre = np.mean(np.diff(tcpWindowAvoidCongestion))
    #averageIncre = np.mean(dy)
    answer['averageIncre'] = averageIncre
    # print("average incre", averageIncre)

    def isScalable():
        if tcpBeta >= 0.8 and tcpBeta<1:
            if round(averageRate, 2) == 1.01 and round(averageIncre, 1) >= 1:
                #print("scalable")
                return True
        return False

    def isYEAH():
        if tcpBeta >= 0.8 and tcpBeta<1:
            if averageIncre < 1:
                #print("YEAH")
                return True
        return False

    def isIllinois():
        if averageIncre > 0.5 and tcpBeta==0.7:
            #print("illinois")
            return True
        return False

    def isVegas():
        if tcpBeta <= 0.5:
            if round(averageIncre, 1) < 1 :
                #print("Vegas")
                return True
        return False

    def isReno():
        if round(averageIncre, 1) == 1:
            #print("Reno")
            return True
        return False

         #dirty fix for checking for ratebased
    validWindows = 0
    flatness = []
    bbrWindows = []
    for i in range(len(tcpDatas)-1):
        if tcpWindows[i] > 10:
    	    validWindows += 1 
        if tcpWindows[i] > 50 and tcpWindows[i]-tcpWindows[i-1] < 10:
    	    bbrWindows.append(tcpWindows[i])
    	    flatness.append(np.floor(np.std(tcpWindows[i-2:i])))
    flatness.sort()
    #print(flatness)
        
    def isRateBased():
        try:
            if tcpBeta >= 1:
                if flatness[len(flatness)//2] < 5 and len(flatness)/validWindows > 0.66:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            # print("short flow")
            answer['error'] = "short flow"
            return answer['method']
    #dirty fix for checking for bbr
    def bbr(): 
        #print("here")
        count = 0
        # print(bbrWindows)
        for p in bbrWindows:
            if 100 <= p <= 120 or 65 <= p <= 75:
                count += 1
        try:
            ratio = count/len(bbrWindows)
        except Exception as e:
            return False
        # print(ratio)
        firstFlag = True if ratio>0.5 else False
        
        bandWidthCheckPoit = 0
        packetSize=[]
        for i in range(len(tcpPackets)):
            if tcpPackets[i]>=1500:
                bandWidthCheckPoit = i
                break
        for i in range(5):
            packetSize.append(tcpWindows[bandWidthCheckPoit-i-1])
        # print(packetSize)
        if len(list(filter(lambda x:x<=110 and x >= 90, packetSize))) > 2:
            secondFlag= True
        else:
            secondFlag=  False
        return firstFlag or secondFlag

    # buzzfeed
    def isTypeI():
        if tcpBeta == 1:
            checkStart = 0
            packetSize=[]
            for i in range(len(tcpPackets)):
                if tcpPackets[i]>=1500:
                    checkStart = i
                    break
            if checkStart == 0:
                return False
            for i in range(len(tcpWindowAvoidCongestion)-1,-1,-1):
                if i+tcpLossPoints[0] == checkStart:
                    # print(i,checkStart,tcpWindowAvoidCongestion[i])
                    break
                else:
                    packetSize.append(tcpWindowAvoidCongestion[i])
            #print(packetSize)
            #print(np.average(packetSize))
            if np.average(packetSize) > 120:
                return True
        return False
    
    # radio.co
    def isTypeII():
        if tcpBeta > 1:
            if len(probe) < 3:
                return True
        return False

    # jd.com
    def isTooShort():
        if tcpBeta < 1:
            if backoff == None or len(backoff) < 3:
                return True
        return False


    lossReact = "_loss" if tcpBeta < 1 else "_nonLoss"
    if isCUBIC():
        answer["method"] = "cubic" + lossReact   
    elif isBIC():
        answer["method"] = "bic" + lossReact   
    elif isHTCP():
        answer["method"] = "htcp" + lossReact   
    elif isScalable():
        answer["method"] = "scalable" + lossReact   
    elif isYEAH():
        answer["method"] = "YEAH" + lossReact   
    elif isIllinois():
        answer["method"] = "illinois" + lossReact   
    elif isVegas():
        answer["method"] = "vegas" + lossReact   
    elif isReno():
        answer["method"] = "reno" + lossReact   
    elif bbr():
        answer["method"] = "bbr" + lossReact   
    elif isTypeI():
        answer["method"] = "Type_I" + lossReact   
    elif isTypeII():
        answer["method"] = "Type_II" + lossReact   
    elif isTooShort():
        answer["method"] = "short_flow" + lossReact   
    else:
        answer["method"] = "unknown" + lossReact   
    return answer['method']
    """
    elif isRateBased()!="short flow" and isRateBased():
        if bbr():
            return "bbr"
        else:
            return "Rate Base"
    elif isRateBased()=="short flow":
        return "short flow"
    """

folder = sys.argv[1]

for i in range(5000,50000):
    print( i, classify(folder+str(i)+.csv))
