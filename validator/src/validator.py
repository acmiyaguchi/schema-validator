import itertools

import jsonschema
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType


class SchemaValidator:
    def __init__(self, spark):
        self.spark = spark

    def extract(self, submission_date, sample=1.0):
        return self.spark.createDataFrame([{}])


def validate_ping(ping, schema):
    errors = []

    validator = jsonschema.Draft4Validator(schema)
    err = validator.iter_errors(ping)
    for e in err:
        s = (
            e.validator,
            "/".join(map(str, e.path)),
            "/".join(map(str, e.schema_path)),
        )
        errors.append(s)

    if not errors:
        errors.append((None, None, None))

    return errors


def validate(rdd, schema):
    error_schema = StructType([
        StructField("document_id", StringType(), True),
        StructField("validator", StringType(), True),
        StructField("path", StringType(), True),
        StructField("schema_path", StringType(), True),
    ])

    return (
        rdd
        # associate each error with attribute data
        .flatMap(
            lambda x: list(
                zip(itertools.repeat((x["meta"]["documentId"])),
                    validate_ping(x, schema))
                )
        )
        .map(lambda x: x[0] + x[1])
        .toDF(schema=error_schema)
    )


def summarize(validation, top_n=10):

    success = (
        validation
        .where("validator is null")
        .select("document_id")
        .distinct()
        .count()
    )

    total = (
        validation
        .groupBy()
        .agg(F.countDistinct("document_id").alias("total_count"))
    )

    rollup = (
        validation
        .where("validator is not null")
        .groupBy("validator", "path", "schema_path")
        .agg(F.count("document_id").alias("num_error"))
        .orderBy(F.desc("num_error"))
        .limit(top_n)
        .collect()
    )

    summary = {
        "success": success,
        "total": total,
        "rollup": map(lambda x: x.asDict, rollup)
    }

    return summary
