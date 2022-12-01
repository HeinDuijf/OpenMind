## Help for setting up PyCharm configuration
This chapter does not belong in this code repository, since it is
independent of the code.<br>
However, for now, it is included as a small reference, until we find a better place for it.

## Choosing python interpreter
To choose your python environment in PyCharm, first create it:

```bash
cd [some directory you want env to be in, usually project folder]
python3 -m venv .venv  # These commands work for linux, don't know windows
source .venv/bin/activate
pip install -r requirements.txt
```
Then, select it for PyCharm via: `preferences` --> `project` --> `python interpreter`.

## Setting up black
To use black as an auto-formatter (which is very nice), go to `preferences`-`tools`-`file watchers`-`[add]`-`custom`.
```
name: whatever
file type: select “Python”
Program: $PyInterpreterDirectory$/black
Arguments: $FilePath$
Output paths to refresh: $FilePath$
Working directory: $ProjectFileDir$
```

## Setting up isort
This is similar to the black setup. <br>
Go to `preferences`-`tools`-`file watchers`-`[add]`-`custom`.
```
name: whatever
file type: select “Python”
Program: $PyInterpreterDirectory$/isort
Arguments: $FilePath$
Output paths to refresh: $FilePath$
Working directory: $ProjectFileDir$
```

## Setting up flake8
Is similar again. The program (~terminal command) is flake8 instead of black or isort.