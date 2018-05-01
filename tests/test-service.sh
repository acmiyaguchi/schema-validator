#!/usr/bin/env bash

max_retries=5
base_uri="localhost:8000"
schema_id=test.schema.json
dataset_id=test.success.json.txt

# run at the root of the project
cd `dirname $0` && cd ..

# if the setup is run, then also run the cleanup
function setup {
    make clean && make build
    make up &
    export make_up_pid=$!

    function cleanup {
        kill $make_up_pid
        make clean
    }
    trap cleanup EXIT
}


resp=`curl --silent "${base_uri}/__heartbeat__"`
if [[ ${resp} != "OK" ]]; then
    setup

    timeout=6
    retries=0
    while [[ `curl --silent "${base_uri}/__heartbeat__"` != "OK" && ${retries} -lt ${max_retries} ]]; do
        sleep ${timeout}
        retries=$(( $retries + 1 ))
    done

fi

resp=`curl --silent -X POST "${base_uri}/submit?schema_id=${schema_id}&dataset_id=${dataset_id}"`
task_id=`echo ${resp} | jq -r .task_id`

echo "polling state for ${task_id}"

timeout=15
state="{\"state\": \"PENDING\"}"
retries=0
while [[ `echo "${state}" | jq -r .state` == "PENDING" && ${retries} -lt ${max_retries} ]]; do
    state=`curl --silent "${base_uri}/status/${task_id}"`
    echo "polled state:" ${state}
    sleep ${timeout}
    retries=$(( $retries + 1 ))
done


function test_results {
    if [[ `type -t cleanup` == "function" ]]; then
        cleanup
    fi

    if [[ `echo "$state" | jq -r .result.success` -eq 3 ]]; then
        echo "Test succeeded"
    else
        echo "Test failed"
        exit 1
    fi
}
trap test_results EXIT