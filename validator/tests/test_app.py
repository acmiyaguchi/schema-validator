import json

import pyspark
import pytest
from click.testing import CliRunner
from mozvalidator import app


@pytest.fixture(autouse=True)
def mock_spark_session(spark, monkeypatch):
    def _getOrCreate(self):
        return spark

    monkeypatch.setattr(
        pyspark.sql.session.SparkSession.Builder,
        "getOrCreate",
        _getOrCreate
    )


@pytest.fixture
def schema():
    return json.dumps({
        "type": "object",
        "properties": {
            "foo": {"type": "integer"},
            "bar": {"type": "boolean"},
        },
        "required": ["foo", "bar"]
    })


def append_meta(data):
    def doc_id(i): return {"meta": {"documentId": "{:03}".format(i)}}
    return [{**x, **doc_id(i)} for i, x in enumerate(data)]


def text_data(data, delim="\n"):
    data = append_meta(data)
    return delim.join([json.dumps(point) for point in data])


@pytest.fixture
def success_data():
    return text_data([
        {"foo": 1, "bar": True},
        {"foo": 2, "bar": False},
        {"foo": 3, "bar": True},
    ])


@pytest.fixture
def error_data():
    return text_data([
        {"foo": 1, "bar": True},
        {"foo": 2, "bar": False},
        {"foo": 3, "bar": True},
    ])


def test_request_success(spark, schema, success_data, tmpdir):
    schema_name = "test.schema.json"
    input_data_name = "data"

    # TODO: refactor into a tmpdir factory
    input_dir = tmpdir.mkdir("input")
    output_dir = tmpdir.mkdir("output")

    input_dir.join(schema_name).write(schema)
    input_dir.join(input_data_name).write(success_data)

    # equivalent of spark-submit's `--files` option
    spark.sparkContext.addFile(str(input_dir.join(schema_name)))

    runner = CliRunner()
    result = runner.invoke(app.main, [
        "--schema-name", schema_name,
        '--input-path',  str(input_dir.join(input_data_name)),
        "--output-path", str(output_dir),
        "--protocol", "file"
    ])

    assert result.exit_code == 0

    assert output_dir.join("validation", "_SUCCESS").check()
