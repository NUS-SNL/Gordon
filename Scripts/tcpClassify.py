import numpy as np 
import warnings
#from matplotlib import pyplot as plt

def classify(tcpFile = "../Data/windows.csv"):
    warnings.filterwarnings("ignore")

    tcpDatas = np.loadtxt(fname=tcpFile, delimiter=' ', usecols=(1,2))
    tcpDatas[:,[0,-1]] = tcpDatas[:,[-1, 0]]
    tcpRounds = tcpDatas[:,0]
    tcpWindows = tcpDatas[:,-1]
    #print("TCP Windows", tcpWindows)

    def getBeta(window1, window2):
        return round((window2/window1)+0.0005, 3)

    tcpLossPoints = []
    tcpBeta = 0
    for i in range(len(tcpDatas)-1):
        if tcpWindows[i] > 80:
            tcpLossPoints.append(i)
            tcpBeta =  round(getBeta(tcpWindows[i], tcpWindows[i+1]),1)
            break
    if len(tcpLossPoints) == 0:
        #print("unknown")
        return "unknown"
    #print("First Loss Point", tcpLossPoints[0])
    print("Beta", tcpBeta)
    if tcpBeta < 1:
        for i in range(tcpLossPoints[0]+1, len(tcpDatas)-1):
            if tcpWindows[i] > tcpWindows[i+1]:
                if getBeta(tcpWindows[i], tcpWindows[i+1]) < 0.6:
                    tcpLossPoints.append(i)
        #print("Whole Loss Point", tcpLossPoints)

    if len(tcpLossPoints) > 1:
        tcpWindowAvoidCongestion = tcpWindows[tcpLossPoints[0]+1:tcpLossPoints[1]+1]
    else:
        tcpWindowAvoidCongestion = tcpWindows[tcpLossPoints[0]+1:]
    print("TCP Windows Congestion Avoid", tcpWindowAvoidCongestion)

    #dy = np.diff(tcpWindowAvoidCongestion)
    try:
        dy = np.gradient(tcpWindowAvoidCongestion)
    except Exception as e:
        return "unknown"
    print("derivative", dy, len(dy))

    averageIncre = np.mean(np.diff(tcpWindowAvoidCongestion))
    #averageIncre = np.mean(dy)
    print("average incre", averageIncre)

    #d2y = np.diff(tcpWindowAvoidCongestion, n=2)
    try:
        d2y = np.gradient(np.gradient(tcpWindowAvoidCongestion))
    except Exception as e:
        return "unknown"
    print("second derivative", d2y, len(d2y))

    tcpIncreRate = []
    for i in range(1, len(tcpWindowAvoidCongestion)):
        tcpIncreRate.append(round(tcpWindowAvoidCongestion[i] / tcpWindowAvoidCongestion[i-1], 4))
    averageRate = np.mean(tcpIncreRate)
    print("average rate", averageRate)
    
    #plt.figure()
    #plt.plot(tcpRounds, tcpWindows)
    #plt.legend([tcpFile])
    #plt.show()
    """
    if len(tcpLossPoints) > 1:
        polyCoef = np.polyfit(tcpRounds[tcpLossPoints[0]+1:tcpLossPoints[1]+1], tcpWindowAvoidCongestion, 6)
        polyFunc = np.poly1d(polyCoef)
        polyValue = polyFunc(tcpRounds[tcpLossPoints[0]+1:tcpLossPoints[1]+1])
        plt.plot(tcpRounds[tcpLossPoints[0]+1:tcpLossPoints[1]+1], polyValue)
        plt.show()
    else:
        polyCoef = np.polyfit(tcpRounds[tcpLossPoints[0]+1:], tcpWindowAvoidCongestion, 6)
        polyFunc = np.poly1d(polyCoef)
        polyValue = polyFunc(tcpRounds[tcpLossPoints[0]+1:])
        plt.plot(tcpRounds[tcpLossPoints[0]+1:], polyValue)
        plt.show()
    """
    #print(polyValue)

    # find zero region 
    d2yZeroRegions = []
    zeroScope = (-0.5, 0, 0.5)
    lossPointRange = (tcpWindows[tcpLossPoints[0]]-2, tcpWindows[tcpLossPoints[0]]+2)
    i = 0
    while i < len(d2y):
        if lossPointRange[0] <= tcpWindowAvoidCongestion[i] <= lossPointRange[1] and i < len(d2y)-2:
            #if zeroScope[0] <= d2y[i] <= zeroScope[2] and zeroScope[0] <= d2y[i+1] <= zeroScope[2] and zeroScope[0] <= d2y[i+2] <= zeroScope[2]:
            if lossPointRange[0] <= tcpWindowAvoidCongestion[i] <= lossPointRange[1] and lossPointRange[0] <= tcpWindowAvoidCongestion[i+1] <= lossPointRange[1] and lossPointRange[0] <= tcpWindowAvoidCongestion[i+2] <= lossPointRange[1]:
                j = i
                #while zeroScope[0] <= d2y[j] <= zeroScope[2]:
                while lossPointRange[0] <= tcpWindowAvoidCongestion[j] <= lossPointRange[1]:
                    if j == len(d2y)-3:
                        break
                    j += 1
                d2yZeroRegions.append((i, j-1))
                i = j
                if i == len(d2y)-3:
                    #if zeroScope[0] <= d2y[i+1] <= zeroScope[2]:
                    if lossPointRange[0] <= tcpWindowAvoidCongestion[i+1] <= lossPointRange[1]:
                        i += 1
                    break
            else:
                i += 1
                if i == len(d2y)-2:
                    break
        else:
            i += 1
    #print(d2yZeroRegions)
    for i in d2yZeroRegions:
        print("d2 zero region", d2y[i[0]:i[1]+1], dy[i[0]:i[1]+1], np.mean(dy[i[0]:i[1]+1]), tcpWindowAvoidCongestion[i[0]:i[1]+1], np.std(tcpWindowAvoidCongestion[i[0]:i[1]+1]))
        pass

    def isCubic():
        for i in d2yZeroRegions:
            #if round(np.std(tcpWindowAvoidCongestion[i[0]:i[1]+1]),0) <= 2 :
            if len(tcpWindowAvoidCongestion[i[0]:i[1]+1]) > 3:
                #print(d2y[:i[0]], len(d2y[:i[0]]))
                if len(d2y[:i[0]]) >= 3:
                    #print(round(len(list(filter(lambda x: x<0, d2y[:i[0]]))) / len(d2y[:i[0]]),1))
                    if round(len(list(filter(lambda x: x<0, d2y[:i[0]]))) / len(d2y[:i[0]]),1) >= 0.5:
                        if len(d2y[i[1]+1:]) >= 3:
                            if len(list(filter(lambda x:x>0, d2y[i[1]+1:]))) / len(d2y[i[1]+1:]) >= 0.5 and averageIncre > 1:
                                print("cubic")
                                #print(d2y[:i[0]], np.mean(dy[1:i[0]+1]))
                                #print(d2y[i[0]:i[1]+1], np.mean(dy[i[0]+1:i[1]+2]))
                                #print(d2y[i[1]+1:], np.mean(dy[i[1]+2:]))
                                return True
        return False
    
    def isBBR():
        if round(tcpBeta, 1) == 1:
            print("bbr")
            return True
        return False

    def isBIC():
        for i in d2yZeroRegions:
            #if round(np.std(tcpWindowAvoidCongestion[i[0]:i[1]+1]), 0) <= 2:
            if len(tcpWindowAvoidCongestion[i[0]:i[1]+1]) > 3:
                #print(d2y[:i[0]], len(d2y[:i[0]]))
                if len(d2y[:i[0]]) >= 3:
                    if len(list(filter(lambda x: x<0, d2y[:i[0]]))) / len(d2y[:i[0]]) >= 0.5 and len(list(filter(lambda x:x>0, d2y[i[1]+1:]))) / len(d2y[i[1]+1:]) < 0.5:
                        print("bic")
                        #print(d2y[:i[0]], np.mean(dy[1:i[0]+1]))
                        #print(d2y[i[0]:i[1]], np.mean(dy[i[0]+1:i[1]+1]))
                        return True
        return False
    
    def isHTCP():
        if len(list(filter(lambda x:x>0, d2y))) / len(d2y) > 0.6 and averageIncre > 3:
            print("htcp")
            return True
        """
        if len(d2yZeroRegions) == 0:
            if len(list(filter(lambda x:x>0, d2y))) / len(d2y) > 0.5 and averageIncre > 2:
                print("htcp")
                return True
        
        else:
            for i in d2yZeroRegions:
                if np.std(tcpWindowAvoidCongestion[i[0]:i[1]+1]) < 2:
                    if len(d2y[i[1]+1:]) >= 3:
                        if len(list(filter(lambda x:x>0, d2y[i[1]+1:]))) / len(d2y[i[1]+1:]) >= 0.5 and averageIncre > 1:
                            print("htcp with zero")
                            return True
                else:
                    if len(list(filter(lambda x:x>0, d2y))) / len(d2y) > 0.5 and averageIncre > 2:
                        print("htcp")
                        return True
        
        return False
        """

    def isScalable():
        if tcpBeta >= 0.8:
            if round(averageRate, 2) == 1.01 and round(averageIncre, 1) >= 1:
                print("scalable")
                return True
        return False
    
    def isYEAH():
        if tcpBeta >= 0.8:
            if averageIncre < 1:
                print("YEAH")
                return True
        return False

    def isIllinois():
        if tcpBeta > 0.5 and averageIncre > 0.5:
            print("illinois")
            return True
        return False

    def isVegas():
        if tcpBeta <= 0.5:
            if round(averageIncre, 1) < 1:
                print("Vegas")
                return True
        return False

    def isReno():
        if round(averageIncre, 1) == 1:
            print("Reno")
            return True
        return False
    
    def isRateBase():
        if round(tcpBeta, 1) >= 1:
            print("maybe rate base")
            return True
        return False

    if isBBR():
        return "bbr"
    #elif isRateBase():
    #    return "maybe rate base"
    else:
        if isCubic():
            return "cubic"
        elif isBIC():
            return "bic"
        elif isHTCP():
            return "htcp"
        elif isScalable():
            return "scalable"
        elif isYEAH():
            return "YEAH"
        elif isIllinois():
            return "illinois"
        elif isVegas():
            return "vegas"
        elif isReno():
            return "reno"
        else:
            print("unknown")
            return "unknown"

