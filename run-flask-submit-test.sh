#!/usr/bin/env bash

# assumes that the service is running on localhost:8000
schema_id=test.schema.json
dataset_id=test.success.json.txt

resp=`curl --silent -X POST "localhost:8000/submit?schema_id=${schema_id}&dataset_id=${dataset_id}"`
task_id=`echo $resp | jq -r .task_id`

echo "polling state for $task_id"

#TODO: max retries
timeout=15
state="{\"state\": \"PENDING\"}"
while [[ `echo "$state" | jq -r .state` == "PENDING" ]]; do
    state=`curl --silent "localhost:8000/status/${task_id}"`
    echo "polled state:" $state
    sleep $timeout
done

if [[ `echo "$state" | jq -r .result.success` -eq 3 ]]; then
    echo "Test succeeded"
else
    echo "Test failed"
    exit 1
fi
