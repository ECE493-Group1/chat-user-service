# user-service
User Service for Context-Aware Thread-based Chat App



## Installing the app
It is recommended to use a virtual environment for installing the app.
### Install
```
pip3 install -e .
```
### Run
```
flask run --port 3000
```

## Running the tests

### Install the testing libraries
```
pip3 install -e '.[test]'
```

### Run the tests
```
pytest
```

### Check code coverage
```
coverage run -m pytest

coverage report
```
