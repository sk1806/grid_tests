#!/usr/bin/env python

import os

from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)

from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac


#JobName    = "test2";
#Executable = "loop_jobs.sh";
#StdOutput = "StdOut";
#StdError = "StdErr";
#InputSandbox = {"job.sh", "loop_jobs.sh"};
#OutputSandbox = {"StdOut","StdErr", "out.txt"};

j = Job()
j.setName('test2')
j.setPlatform("EL7")
j.setInputSandbox(["job.sh", "loop_jobs.sh"])
j.setOutputSandbox([ "StdErr" , "StdOut" ])
j.setExecutable("./loop_jobs.sh", arguments=" 2>&1 job.log", logFile="job.log")
print(Dirac().submitJob(j))


