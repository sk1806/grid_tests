#!/bin/bash

chmod +x job.sh
./job.sh  2>&1 | tee -a out.txt

