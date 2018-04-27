import json
import os
import shutil
import traceback

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

    runner = CliRunner()
    result = runner.invoke(app.main, [
        "--schema-path", str(input_dir.join(schema_name)),
        '--input-path',  str(input_dir.join(data_name)),
        "--output-path", str(output_dir),
        "--protocol", "file"
    ])

    if result.exit_code != 0:
        traceback.print_tb(result.exc_info[2])
        assert False

    assert output_dir.join("validation", "_SUCCESS").check()

    with open(output_dir.join("response.json"), 'r') as f:
        result = json.load(f)
    assert result['success'] == 3
