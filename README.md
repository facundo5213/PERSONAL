# Kronos Project

Kronos project using FastAPI with MongoDB

## Requirements

To run the app on your pc, be sure to accomplish the next checklist:

- [ ] Be sure you have installed Git (https://git-scm.com/downloads)
- [ ] Have installed Python (https://www.python.org/downloads/)
- [ ] Already installed Mongodb (https://www.mongodb.com/try/download/community)
- [ ] Do not forget to ask the staff for the environment variables file

## Insallation

First clone our repo and be sure to be in develop branch, with:
```bash
git clone git@github.com:DevoCampTuc/Back-Kronos.git
```

Or:

```bash
git clone https://github.com/DevoCampTuc/Back-Kronos.git
```

Then change into the `Back-Kronos` folder:

```bash
cd Back-Kronos
```

Now, we will need to create a virtual environment and install all the dependencies:

```bash
python3 -m venv venv  # on Windows, use "python -m venv venv" instead
. venv/bin/activate   # on Windows, use "venv\Scripts\activate" instead
pip install -r requirements.txt
```

Finally run the app:

```bash
python3 main.py  # on Windows, use "python main.py" instead
```

## Updating

Go to the path where you have cloned the repo and as usual be sure to be in the develop branch, with:
```bash
git checkout develop
```

Pull the last commits pushed:

```bash
git pull
```

Activate the virtual environment and install new dependencies:
```bash
. venv/bin/activate   # on Windows, use "venv\Scripts\activate" instead
pip install -r requirements.txt
```
Now you are ready to re run the app:
```bash
python3 main.py  # on Windows, use "python main.py" instead
```