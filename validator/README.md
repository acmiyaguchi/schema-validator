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

### Packaging
```bash
python setup.py bdist_egg
```