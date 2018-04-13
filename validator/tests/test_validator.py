import pytest
from validator import validator


@pytest.fixture
def schema():
    return {
        "type": "object",
        "properties": {
            "meta": {
                "type": "object",
                "properties": {
                    "documentId": {"type": "string"}
                }
            },
            "atomic": {"type": "integer"},
            "maybe_atomic": {"type": ["integer", "null"]},
            "complex": {
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "field_a": {"type": "integer"}
                        },
                        "required": ["field_a"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "field_b": {"type": "integer"}
                        },
                        "required": ["field_b"]
                    },
                ]
            }
        },
        "required": ["meta", "maybe_atomic", "complex"]
    }


@pytest.fixture
def rdd(spark):
    valid = [
        # normal
        {"atomic": 1, "maybe_atomic": 2,
         "complex": {"field_a": 3, "field_b": 4}},
        # nulled maybe
        {"atomic": 1, "maybe_atomic": None,
         "complex": {"field_a": 3, "field_b": 4}},
        # missing atomic, nulled maybe, extra field in complex
        {"maybe_atomic": None,
         "complex": {"field_a": 3, "field_b": 4, "extra": True}},
    ]

    invalid = [
        # 2x type, 1x required
        {"atomic": None,
         "complex": {"field_a": 3, "field_b": False}},
        # 2x required
        {"atomic": 1,
         "complex": {"field_a": 3}},
    ]

    def doc_id(i): return {"meta": {"documentId": "{:03}".format(i)}}
    data = [{**x, **doc_id(i)} for i, x in enumerate(valid + invalid)]

    return spark.sparkContext.parallelize(data)


@pytest.fixture
def dataframe(rdd, schema):
    return validator.validate(rdd, schema)


def test_validation_counts_all_errors(rdd, schema):
    validation = validator.validate(rdd, schema)
    assert validation.count() == 8
    assert validation.where('validator = "type"').count() == 2
    assert validation.where('validator = "required"').count() == 3


def test_summary_success(dataframe):
    summary = validator.summarize(dataframe)
    assert summary["success"] == 3


def test_summary_total(dataframe):
    summary = validator.summarize(dataframe)
    assert summary["total"] == 5


# TODO: a more robust set of rollup tests once the metric has been specified
def test_summary_rollup(dataframe):
    summary = validator.summarize(dataframe)
    assert summary["rollup"][0] == {
        "validator": "required",
        "path": "",
        "schema_path": "required",
        "num_error": 2
    }
