#!/bin/bash

set -eu -o pipefail

# make sure this script is running at the root of the directory
cd `dirname $0` && cd ..

make build

docker-compose up &
make_up_pid=$!

function cleanup {
    kill $make_up_pid
    make clean
}
trap cleanup EXIT

# wait until the services come online
timeout=1
worker_container=""
while [[ -z $worker_container ]]; do
    worker_container=`docker ps | grep _worker | head -n1 | awk '{print $1}'`
    sleep $timeout
    timeout=$(( $timeout * 2 ))
done

echo "test data directory is mounted on /mnt/data"

docker exec -it $worker_container \
    spark-submit \
        --master spark://spark:7077 \
        --py-files /app/validator/dist/*.egg \
        validator/bin/run.py \
            --schema-path /app/data/input/test.schema.json \
            --input-path /app/data/input/test.success.json.txt \
            --output-path /app/data/output

validation=`docker exec -it $worker_container \
    stat /mnt/data/output/validation/_SUCCESS > /dev/null && \
    echo $?`
response=`docker exec -it $worker_container \
    stat /mnt/data/output/response.json > /dev/null && \
    echo $?`

# TODO: clear output and test json

# clean-up and then print results
function test_results {
    cleanup

    if [[ $output -eq 0 && $response -eq 0 ]]; then
        echo "Test succeeded"
    else
        echo "Test failed"
        exit 1
    fi
}
trap test_results EXIT
