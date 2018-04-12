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
from mozvalidator import validator
from pyspark.files import SparkFiles
from pyspark.sql import SparkSession


@click.command()
@click.option('--schema-name', required=True)
@click.option('--input-path', required=True)
@click.option('--output-path', required=True)
@click.option('--protocol', type=click.Choice(['file', 's3']), default='file')
def main(schema_name, input_path, output_path, protocol):
    spark = SparkSession.builder.appName("schema_validator").getOrCreate()

    # TODO: logging
    with open(SparkFiles.get(schema_name), 'r') as f:
        schema = json.load(f)

    input_path = "{}://{}".format(protocol, input_path)
    output_path = "{}://{}".format(protocol, output_path)

    print(input_path)
    print(output_path)

    ping_rdd = validator.extract(spark, input_path)
    validation_df = validator.validate(ping_rdd, schema)
    summary_dict = validator.summarize(validation_df)

    validator.load(output_path, "validation", validation_df)

    # TODO: Add response using the summary_dict as a base
    print(summary_dict)


if __name__ == '__main__':
    main()
