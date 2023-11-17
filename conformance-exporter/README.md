## Local Development

### Configuration

The `dev-config` file stores environment variables that may be required by the script.
Note the format of the file must me valid shell expressions e.g. `export MY_VAR=123`

### Python setup

Create and activate a python3 virtual environment in the current folder.

```shell
python3 -m venv venv
```

activate the environment

```shell
source ./venv/bin/activate
```

upgrade pip

```shell
python3 -m pip install --upgrade pip
```

install dependencies

```shell
 pip3 install -r requirements.txt
```

### Start the service locally

You can use the provided makefile to start the service

```shell
make dev
```

### Linting

You can lint the python source code using the black formatter

```shell
make lint
```
