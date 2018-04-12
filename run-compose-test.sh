#!/bin/bash

set eou -pipefail

# make sure all running containers are down
make clean

pushd .
cd validator
pipenv run python setup.py bdist_egg
popd

# rebuild the current docker containers
make build
make up &

make_up_pid=$!

function cleanup {
    kill $make_up_pid
    make clean
}
trap cleanup EXIT

# wait until the services come online
timeout=1
web_container=""
while [[ -z $web_container ]]; do
    web_container=`docker ps | grep _web | awk '{print $1}'`
    sleep $timeout
    timeout=$(( $timeout * 2 ))
done

echo "test data directory is mounted on /mnt/data"

docker exec -it $web_container \
    spark-submit \
        --master spark://spark:7077 \
        --py-files validator/dist/mozschema_validator-0.0.1-py3.6.egg \
        --files /mnt/data/input/test.schema.json \
        validator/bin/run.py \
            --schema-name test.schema.json \
            --input-path /mnt/data/input/test.success.json.txt \
            --output-path /mnt/data/output

output=`docker exec -it $web_container \
    stat /mnt/data/output/validation/_SUCCESS > /dev/null && \
    echo $?`


# clean-up and then print results
function test_results {
    cleanup

    if [[ $output -eq 0 ]]; then
        echo "Test succeeded"
    else
        echo "Test failed"
        exit 1
    fi
}
trap test_results EXIT