"""
Spark job for processing validation errors.

Usage:
````
spark-submit \
    --master local[*] \
    --deploy-mode client \
    --py-files dist/*.egg \
    --files ${SCHEMA}.json
    driver.py SCHEMA INPUT_PATH OUTPUT_PATH
```
"""

import json

import click
from pyspark.sql import SparkSession

from . import validator


@click.command()
@click.option('--schema-path', required=True)
@click.option('--input-path', required=True)
@click.option('--output-path', required=True)
@click.option('--protocol', type=click.Choice(['file', 's3']), default='file')
def main(schema_path, input_path, output_path, protocol):
    spark = SparkSession.builder.appName("schema_validator").getOrCreate()

    # TODO: logging
    if protocol == "file":
        with open(schema_path) as f:
            schema = json.load(f)
    else:
        raise NotImplementedError

    spark_input_path = "{}://{}".format(protocol, input_path)
    spark_output_path = "{}://{}".format(protocol, output_path)

    print(input_path)
    print(output_path)

    ping_rdd = validator.extract(spark, spark_input_path)
    validation_df = validator.validate(ping_rdd, schema)
    summary_dict = validator.summarize(validation_df)

    validator.load(spark_output_path, "validation", validation_df)

    if protocol == "file":
        file_path = "{}/{}".format(output_path, "response.json")
        with open(file_path, "w") as f:
            json.dump(summary_dict, f)
    else:
        raise NotImplementedError


if __name__ == '__main__':
    main()
