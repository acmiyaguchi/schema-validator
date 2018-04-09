from pyspark.sql import SparkSession
import click
from validator import SchemaValidator


@click.command()
def main():
    spark = SparkSession.builder.appName("schema_validator").getOrCreate()
    validator = SchemaValidator(spark)
    validator.extract("20180401")


if __name__ == '__main__':
    main()
