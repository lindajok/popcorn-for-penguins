## Flask commands

And a virtual environment `demoenv`:

```
python3 -m venv demoenv
```

Activate the environment:

```
. demoenv/bin/activate
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
export FLASK_APP=search_engine.py
```

Enable development environment to activate interactive debugger and reloader:

```
export FLASK_ENV=development
```

Set the port in which to run the application, e.g.:

```
export FLASK_RUN_PORT=8000
```

Run the app:

```
flask run
```

Go to `localhost:8000/search` in your browser to see the website.
