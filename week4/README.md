## Flask commands

And a virtual environment `demoenv`:

```
python3 -m venv demoenv
```

On Windows:

```
py -3 -m venv demoenv
```

Activate the environment:

```
. demoenv/bin/activate
```

On Windows:

```
demoenv/Scripts/activate
```

Install Flask:

```
pip install Flask
```

You might also have to install:
```
pip install -U scikit-learn
pip install nltk
pip install beautifulsoup4
```

Set the following environment variables:

Show flask which file to run:

```
export FLASK_APP=flaskdemo.py
```

Enable development environment to activate interactive debugger and reloader:

```
export FLASK_ENV=development
```

Set the port in which to run the application, e.g.:

```
export FLASK_RUN_PORT=8000
```

On Windows command line, you can the environment variables with:

```
set FLASK_APP=flaskdemo.py
set FLASK_ENV=development
set FLASK_RUN_PORT=8000
```

And on Windows PowerShell:

```
$env:FLASK_APP = "flaskdemo.py"
$env:FLASK_ENV = "development"
$env:FLASK_RUN_PORT = "8000"
```

Run the app:

```
flask run
```

Go to `localhost:8000/search` in your browser to see the website.

