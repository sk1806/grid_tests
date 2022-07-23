#!/bin/bash

echo ''
ls -lh
echo ''
echo ''

 ls -l /cvmfs/hyperk.egi.eu/hk
 ls -l /cvmfs/t2k.egi.eu/nd280_containers/
 ls -l /cvmfs/t2k.egi.eu/nd280_containers/nd280v11r31p57_sand/usr/local/t2k/current/nd280/setup.sh



  TRYCVMFSSINGULARITY=true
  
  export SINGULARITY_OPTS=''

  if [ "${TRYCVMFSSINGULARITY}" = true ] && [ -f "/cvmfs/oasis.opensciencegrid.org/mis/singularity/current/bin/singularity" ] && [ `sysctl -n user.max_user_namespaces` -gt 100 ]; then
      # Use CVMFS version of singularity
      'Attempting to setup singularity frrom cvmfs'
      export SINGULARITY="/cvmfs/oasis.opensciencegrid.org/mis/singularity/current/bin/singularity"
      export SINGULARTY_OPTS="--userns"
  fi



  $SINGULARITY exec ${SINGULARTY_OPTS} /cvmfs/hyperk.egi.eu/hk/hk_0.2.1_prod_sand  ls /opt/HyperK/ 
