# spark-schema-validator

Spark job for validating json schema against a RDD.

## Development

Install `pipenv` on your system and the project dependencies.

```bash
pip install pipenv
pipenv sync
```

You may run the following commands within a virtual environment (e.g `pipenv shell`)
or through the `pipenv run` prefix.

### Testing
```bash
python setup.py test
```

You can manually specify optione either through the `PYTEST_ADDOPTS` environment variable,
or by manually adding the module into context. For example, you may want to stop on the first
failure in the test and run the python debugging tool.

```bash
python -m pytest -x --pdb
```

### Packaging
```bash
python setup.py bdist_egg
```