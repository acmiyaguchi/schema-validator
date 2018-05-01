import logging
import subprocess
from . import celery

logger = logging.getLogger(__name__)


@celery.task()
def spark_submit(schema_id, dataset_id):
    """Submit a job to a remote spark cluster.

    :param schema_id: A unique identifier for the document schema
    :param dataset_id: A unique identifier of the dataset to validate
    :return:
    """

    # TODO: add logging
    # NOTE: assumes the current working directory is the root
    input_path = "/app/data/input"
    output_path = "/app/data/output"

    spark_submit_args = [
        "spark-submit",
        "--master", "spark://spark:7077",
        "--py-files", "validator/dist/validator-0.1.0-py3.6.egg",
    ]

    # TODO: add random suffix for run_id
    run_args = [
        "validator/bin/run.py",
        "--schema-path", "{}/{}".format(input_path, schema_id),
        "--input-path", "{}/{}".format(input_path, dataset_id),
        "--output-path", output_path
    ]
    command = spark_submit_args + run_args
    retval = subprocess.call(command)

    # result passing via the filesystem
    if retval == 0:
        with open("{}/{}".format(output_path, "response.json"), 'r') as f:
            return f.read()
    else:
        return None
