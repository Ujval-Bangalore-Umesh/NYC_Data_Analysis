import csv

class Patient:

    def __init__(self):
        self.patid = ""
        self.gender = ""
        self.age = 0
        self.state = ""
        self.listMed = []
        self.listRes = []
        self.listRx = []
        self.listRxCodes = []
        self.listConf = []
        self.t = []
        self.c = []
        self.earliestDay = 10000
        self.latestDay = -10000
        self.binSums = [0]*6
        self.diagCounts = [[0]*10 for i in range(6)]
        self.rxCounts = [[0]*5 for i in range(6)]


#LAB results       
class Results:

    def __init__(self):
        self.abnl_cd = ""
        self.anylseq = ""
        self.hi_nrml = 0
        self.labclid = ""
        self.loinc_id = ""
        self.low_nrml = 0
        self.proc_cd = ""
        self.rslt_nbr = 0
        self.rslt_txt = ""
        self.rslt_unit_nm = ''
        self.days_from_diag = 0

#RX FILE    
class RxClaim:

    def __init__(self):
        self.clmid = ""
        self.ahfsclss = ""
        self.days_sup = 0
        self.quantity = 0
        self.std_cost = 0
        self.days_from_diag = 0

    #services = []

#medical file
class MedClaim:

    def __init__(self):
        self.clmid = ""
        self.conf_id = ""
        self.std_cost = 0
        self.pos = ""
        self.drg = ""
        self.provcat = ""
        self.rvnu_cd = ""
        self.proc_cd = ""
        self.diag = []
        self.proc = []
        self.days_from_diag = 0

##Helper class for claims    
#class service:
#    confinements = []

class ConfClaim:
    
    def __init__(self):
        self.clmid = ""      
        self.conf_id = ""
        self.std_cost = 0
        self.drg = ""
        self.pos = ""
        self.diag = []
        self.proc = []
        self.days_from_diag = 0
        self.discharge_days_from_diag = 0

def removeClaim(row):
    for i in range (5):
        try:
            code = row[9+i]
        except IndexError:
            continue
        if code[0] in ["E","8"]:
            return True
        if code[0:1] in ["63","64","65","66","67","V3","90","91","92","93","94","95"]:
            return True
        if code[0:2] in ["V22","V23","V24","V27","V28","V91"]:
            return True
        if code[0:3] == "3392":
            return True
    return False

def ReadIn():
    
    count = 0
    memberReader = csv.reader(open('member_information.csv'))
    members = []
    next(memberReader)
    for row in memberReader:
        count = count + 1
        if count > 100:
            break
        pat = Patient()
        pat.patid = row[0]
        if row[1] == "F":
            pat.gender = "1"
        elif row[1] == "M":
            pat.gender = "0"
        else:
            pat.gender = ".5"
        pat.age = str(2017-int(row[2]))
        if row[3] in ["AK","MA","DE","VT","CT","ND","NY","NH","RI","ME"]:
            pat.state = "4";
        elif row[3] in ["WV","PA","SD","MN","NJ","OH","WI","MD","NE","WY"]:
            pat.state = "3";
        elif row[3] in ["IN","IL","MT","FL","IA","MI","OR","KY","WA","MO"]:
            pat.state = "2";
        elif row[3] in ["LA","KS","MS","OK","VA","CA","AR","TN","SC","HI"]:
            pat.state = "1";
        else:
            pat.state = "0";
        
        members.append(pat)

    count = 0
    mInd = 0
    medicalReader = csv.reader(open('medical_target.csv'))
    next(medicalReader)
    for row in medicalReader:
        count = count + 1
        if removeClaim(row):
            continue
        if row[0] != members[mInd].patid:
            for i in range(mInd+1, len(members)):
                if members[i].patid == row[0]:
                    mInd = i;
        if row[0] != members[mInd].patid:
            for i in range(0, mInd+1):
                if members[i].patid == row[0]:
                    mInd = i;   
        if row[0] != members[mInd].patid or len(row) < 20:
            continue
        med = MedClaim()
        med.clmid = row[1]
        if row[2] != "None":
            med.conf_id = row[2]
        if row[3] != "None":
            med.std_cost = float(row[3])
        if row[4] != "None":
            med.pos = row[4]
        if row[5] != "None":
            med.drg = row[5]
        if row[6] != "None":
            med.provcat = row[6]
        if row[7] != "None":
            med.rvnu_cd = row[7]
        med.proc_cd = row[8]
        for i in range (0,5):
            if (row[9+i] != "None") and (row[9+i] != "0"):
                med.diag.append(row[9+i])
            if (row[14+i] != "None") and (row[14+i] != "0"):
                med.proc.append(row[14+i])
        if row[19] != "None":        
            med.days_from_diag = int(row[19])
        if med.days_from_diag > pat.latestDay:
            pat.latestDay = med.days_from_diag
        members[mInd].listMed.append(med)
        
#                if row[3] != "None" and row[19] != "None":
#                    try:
#                        ind = pat.t.index(int(row[19]))
#                        pat.c[ind] = pat.c[ind] + float(row[3])
#                    except ValueError:
#                        pat.t.append(int(row[19]))
#                        pat.c.append(float(row[3]))
                
    count = 0         
    rxReader = csv.reader(open('rx_target.csv'))
    next(rxReader)
    for row in rxReader:
        count = count + 1
        if row[0] != members[mInd].patid:
            for i in range(mInd+1, len(members)):
                if members[i].patid == row[0]:
                    mInd = i;
        if row[0] != members[mInd].patid:
            for i in range(0, mInd+1):
                if members[i].patid == row[0]:
                    mInd = i;    
        if row[0] != members[mInd].patid or len(row) < 7:
            continue
        rx = RxClaim()
        rx.clmid = row[1]
        rx.ahfsclss = row[2]
        rx.days_sup = int(row[3])
        rx.quantity = row[4]
        if row[5] != "None":
            rx.std_cost = float(row[5])
        rx.days_from_diag = int(row[6])
        if med.days_from_diag > pat.latestDay:
            pat.latestDay = med.days_from_diag
        members[mInd].listRx.append(rx)
        if rx.ahfsclss not in members[mInd].listRxCodes:
            members[mInd].listRxCodes.append(rx.ahfsclss)
#        if rx.days_from_diag < members[mInd].earliestDay:
#            members[mInd].earliestDay = rx.days_from_diag
#            print(rx.days_from_diag)
#        if rx.days_from_diag > members[mInd].latestDay:
#            members[mInd].latestDay = rx.days_from_diag
#            print(rx.days_from_diag)
        #if row[6] != "None" and row[5] != "None":
#                    try:
#                        ind = pat.t.index(int(row[6]))
#                        pat.c[ind] = pat.c[ind] + float(row[5])
#                    except ValueError:
#                        pat.t.append(int(row[6]))
#                        pat.c.append(float(row[5]))
    '''        
    confReader = csv.reader(open('confinement_target.csv')) 
    next(confReader)
    for row in confReader:
        confPatID = row[0]
        for pat in members:
            if pat.patid == confPatID:
                conf = ConfClaim()
                conf.clmid = row[1]
                if row[2] != "None":
                    conf.conf_id = row[2]
                conf.std_cost = row[3]
                if row[4] != "None":
                    conf.drg = row[4]
                if row[5] != "None":
                    conf.pos = row[5]
                for i in range (0,5):
                    if (row[6+i] != "None") and (row[6+i] != "0"):
                        conf.diag.append(row[6+i])
                    if (row[11+i] != "None") and (row[11+i] != "0"):
                        conf.proc.append(row[11+i])
                conf.days_from_diag = row[16]
                pat.listConf.append(conf) 


    resultsReader = csv.reader(open('labresults_target.csv'))
    next(resultsReader)
    for row in resultsReader:
        resPatID = row[0]
        for pat in members:
            if pat.patid == resPatID:
                res = Results()
                res.abnl_cd = row[1]
                res.anylseq = row[2]
                res.hi_nrml = float(row[3])
                res.labclid = row[4]
                res.loinc_id = row[5]
                res.low_nrml = float(row[6])
                res.proc_cd = row[7]
                res.rslt_nbr = float(row[8])
                res.rslt_txt = row[9]
                res.rslt_unit_nm = row[10]
                res.days_from_diag = int(row[11])
                pat.listResults.append(res) 
    '''
    '''
    for pat in members:
        together = zip(pat.t,pat.c)
        sortedTogether = sorted(together)
        pat.t = [x[0] for x in sortedTogether]
        pat.c = [x[1] for x in sortedTogether]
    '''
    return members

def yearSums(members):
    for pat in members:
        for med in pat.listMed:
            if med.days_from_diag < pat.earliestDay:
                pat.earliestDay = med.days_from_diag
            if med.days_from_diag > pat.latestDay:
                pat.latestDay = med.days_from_diag
        for rx in pat.listRx:
            if rx.days_from_diag < pat.earliestDay:
                pat.earliestDay = rx.days_from_diag
            if rx.days_from_diag > pat.latestDay:
                pat.latestDay = rx.days_from_diag
        for med in pat.listMed:
            b = int((med.days_from_diag - pat.latestDay + 3*365)/(3*365)*6)
            if b >= 0 and b <= 5 and med.std_cost < 50000:
                pat.binSums[b] += med.std_cost
#            if med.days_from_diag <= pat.latestDay and med.days_from_diag > pat.latestDay-365:
#                pat.yearSums[2] += med.std_cost
#            elif med.days_from_diag <= pat.latestDay - 365 and med.days_from_diag > pat.latestDay-2*365:
#                pat.yearSums[1] += med.std_cost
#            elif med.days_from_diag <= pat.latestDay - 2*365 and med.days_from_diag > pat.latestDay-3*365:
#                pat.yearSums[0] += med.std_cost
        for rx in pat.listRx:
            b = int((rx.days_from_diag - pat.latestDay + 3*365)/(3*365)*6)
            if b >= 0 and b <= 5:
                pat.binSums[b] += rx.std_cost
#            if rx.days_from_diag <= pat.latestDay and rx.days_from_diag > pat.latestDay-365:
#                pat.yearSums[2] += rx.std_cost
#            elif rx.days_from_diag <= pat.latestDay - 365 and rx.days_from_diag > pat.latestDay-2*365:
#                pat.yearSums[1] += rx.std_cost
#            elif rx.days_from_diag <= pat.latestDay - 2*365 and rx.days_from_diag > pat.latestDay-3*365:
#                pat.yearSums[0] += rx.std_cost
    return members

def countDiags(members):
    from collections import defaultdict
    d3diag = defaultdict(int)
    d2rx = defaultdict(int)
    for pat in members:
        for med in pat.listMed:
            for diag in med.diag:
                d3diag[diag[0:3]] += 1
        for rx in pat.listRx:
            d2rx[rx.ahfsclss[0:2]] += int(rx.days_sup)
    diags = sorted(d3diag, key = lambda x: d3diag[x], reverse = True)
    rxs = sorted(d2rx, key = lambda x: d2rx[x], reverse = True)
    for pat in members:
        for med in pat.listMed:
            for patDiag in med.diag:
                for d in range(10):
                    if patDiag[0:3] == diags[d]:
                        b = int((med.days_from_diag - pat.latestDay + 3*365)/(3*365)*6)
                        if b >= 0 and b <= 5:
                            pat.diagCounts[b][d] += 1
        for rx in pat.listRx:
            for d in range(5):
                if rx.ahfsclss[0:2] == rxs[d]:
                     b = int((rx.days_from_diag - pat.latestDay + 3*365)/(3*365)*6)
                     print(b)
                     if b >= 0 and b <= 5:
                         pat.rxCounts[b][d] += int(rx.days_sup)
                         print(pat.rxCounts)
#        for code in pat.listRxCodes:
#            rxs = []
#            for rx in pat.listRx:
#                if rx.ahfsclss == code:
#                    rxs.append(rx)
#            if len(rxs) > 1:
#                times = dict()
#                for rx in rxs:
#                    times[rx.days_from_diag] = rx.days_sup
#                it = iter(sorted(times.iteritems()))
#                
                    
    return members
      
        
                 

def readOut(members):
    import math
    with open("MUDAC_Xtrain.csv", "w") as Xtrain, open("MUDAC_ytrain.csv", "w") as ytrain, open("MUDAC_Xtest.csv", "w") as Xtest:
        for pat in members:  
            if pat.latestDay == -10000:
                pat.latestDay = 0      
            if pat.binSums[4]+pat.binSums[5] < 100000:
                Xtrain.write(pat.gender + ",")
                Xtrain.write(pat.age + ",")
                Xtrain.write(pat.state + ",")
                Xtrain.write(str(pat.latestDay-365) + ",")
                for b in range(2,4):
                    Xtrain.write(str(math.log(pat.binSums[b]+1)) + ",")
                    for d in range(10):
                        Xtrain.write(str(pat.diagCounts[b][d]) + ",")
                    for d in range(5):
                        Xtrain.write(str(pat.rxCounts[b][d]) + ",")   
                        Xtrain.write("\n")
            
                ytrain.write(str(math.log(pat.binSums[4]+pat.binSums[5]+1))+"\n")
            
            Xtest.write(pat.gender + ",")
            Xtest.write(pat.age + ",")
            Xtest.write(pat.state + ",")
            Xtest.write(str(pat.latestDay) + ",")
            for b in range(2,4):
                Xtest.write(str(math.log(pat.binSums[b+2]+1)) + ",")
                for d in range(10):
                    Xtest.write(str(pat.diagCounts[b+2][d]) + ",")
                for d in range(5):
                    Xtest.write(str(pat.rxCounts[b+2][d]) + ",") 
            Xtest.write("\n")
    Xtrain.close()
    Xtest.close()
    ytrain.close()
    
#def averageCosts(members):
#    aveCostsT = []
#    aveCostsC = []
#    aveCostsCount = []
#    for pat in members:
#        for i in range(len(pat.t)):
#            try:
#                ind = aveCostsT.index(pat.t(i))
#                aveCostsC[ind] = aveCostsC[ind] + pat.c[i] 
#                aveCostsCount[ind] = aveCostsCount[ind] + 1
#            except ValueError: 
#                
        
 
#import pylab as plt    
memList = ReadIn()
memList = yearSums(memList)
memList = countDiags(memList)
readOut(memList)
#plt.figure(0)
#for i in range(0,100):
#    plt.plot(memList[i].t,memList[i].c)
#plt.axis([-10,10,-1000,10000])
#plt.show()



