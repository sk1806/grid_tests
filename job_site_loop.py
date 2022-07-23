#!/usr/bin/env python

from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)

from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac

sites=["LCG.UKI-SOUTHGRID-RALPP.uk", \
       "LCG.RAL-LCG2.uk", \
       "LCG.IN2P3-CC.fr", \
       "LCG.UKI-LT2-QMUL.uk", \
       "LCG.UKI-NORTHGRID-LIV-HEP.uk", \
       "LCG.UKI-LT2-IC-HEP.uk", \
       "LCG.UKI-NORTHGRID-MAN-HEP.uk", \
       "LCG.UKI-LT2-Brunel.uk", \
       "LCG.UKI-NORTHGRID-LANCS-HEP.uk", \
       "LCG.UKI-SCOTGRID-GLASGOW.uk", \
       "LCG-UKI-NORTHGRID-SHEF-HEP.uk", \
       "LCG.UKI-SOUTHGRID-OX-HEP.uk", \
       "LCG.CA-SFU-T2.ca", \
       "LCG.CERN-PROD.ch", \
       "LCG.INFN-T1.it", \
       "CLOUD.GRIF.fr", \
       "CLOUD.RECAS-NAPOLI.it" ]



j = Job()
j.setName("test")
j.setJobGroup("test")
j.setPlatform("EL7")
j.setCPUTime(3600)
j.setInputSandbox(['job.sh'])
j.setOutputSandbox([ "StdErr" , "StdOut"])
j.setExecutable("job.sh", arguments="", logFile="job.log")

dirac = Dirac()
j.setDestination("LCG.RAL-LCG2.uk")
res = dirac.submitJob(j)
print('')
#print(res['JobID'])
t4 = res['rpcStub'][2][0]
t5 = t4.split('Site = ')
t6 = t5[1].split(';')
t7 = t6[0]
print(t7 + '   JobID: ' + str(res['JobID']) )
print('')


#for site in sites:
#    j.setDestination(site)
#    res = Dirac().submitJob(j)
#
#    print('')
#    print(res['JobID'])
#    t4 = res['rpcStub'][2][0]
#    t5 = t4.split('Site = ')
#    t6 = t5[1].split(';')
#    t7 = t6[0]
#    print(t7)
#    print('')





# wildcard
#j.setOutputSandbox(['*.log

# j.setBannedSites(['site1'. 'site2'])

# env
# j.setExecutionEnv({'MYVARIABLE':'TOTO'})

# parametric
#j.setParameterSequence("args", ['one', 'two', 'three'])
#j.setParameterSequence("iargs", [1, 2, 3])


