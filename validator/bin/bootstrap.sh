#!/bin/bash
set -euo pipefail
set -x

MASTER=${MASTER:-spark://master:7077}

${SPARK_HOME}/sbin/start-master.sh
${SPARK_HOME}/sbin/start-slave.sh ${MASTER}

# prevent the script from exiting
while true; do sleep 3600; done