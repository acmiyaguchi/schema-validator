import shutil
import os

import pyspark
import pytest
from click.testing import CliRunner
from validator import app


@pytest.fixture(autouse=True)
def mock_spark_session(spark, monkeypatch):
    def _getOrCreate(self):
        return spark

    monkeypatch.setattr(
        pyspark.sql.session.SparkSession.Builder,
        "getOrCreate",
        _getOrCreate
    )


def test_request_success(spark, tmpdir):
    schema_name = "test.schema.json"
    data_name = "test.success.json.txt"

    input_dir = tmpdir.join("input")

    test_data = os.path.join(os.path.dirname(__file__), "data", "input")
    shutil.copytree(test_data, input_dir)

    output_dir = tmpdir.mkdir("output")

    # equivalent of spark-submit's `--files` option
    schema_path = str(input_dir.join(schema_name))
    spark.sparkContext.addFile(schema_path)

    runner = CliRunner()
    result = runner.invoke(app.main, [
        "--schema-name", schema_path,
        '--input-path',  str(input_dir.join(data_name)),
        "--output-path", str(output_dir),
        "--protocol", "file"
    ])

    assert result.exit_code == 0

    assert output_dir.join("validation", "_SUCCESS").check()
