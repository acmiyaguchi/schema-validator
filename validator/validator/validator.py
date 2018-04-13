import itertools
import json

import jsonschema
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType


def extract(spark, source):
    """Return an RDD[String]."""
    rdd = spark.sparkContext.textFile(source)
    return rdd.map(lambda x: json.loads(x))


def load(bucket, tablename, dataframe):
    path = "{}/{}".format(bucket, tablename)
    dataframe.write.parquet(path, mode="overwrite")


def _validate_ping(ping, schema):
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
                zip(itertools.repeat((x["meta"]["documentId"],)),
                    _validate_ping(x, schema))
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
        .select("document_id")
        .distinct()
        .count()
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
        "rollup": [row.asDict() for row in rollup]
    }

    return summary
