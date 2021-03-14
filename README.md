# Popcorn for Penguins

This repository was created for KIK-211 Building NLP Applications course at the University of Helsinki. It contains weekly tasks which can be found in week_*number* folders, and a final project in tomato_engine folder.

To read more about the code, go to our [Wiki](https://github.com/lindajok/popcorn-for-penguins/wiki)

## Tomato Engine 

### What is Tomato Engine?

Tomato Engine is a simple search engine which allows you to browse through nearly 1000 (yes, there are 3 zeros!) recipes. You can search for the simplest word such as *'tomato'*, or use Boolean search to find *'tomato AND NOT ladle'* if you lack kitchen utensils!

Tomato Engine is easy to use! We did all the dirty work with virtual environments, libraries, and dependencies ourselves, so the only thing you need is to clone this repo and you're ready to cook. 

Nice bonus: we're OS friendly which means you can enjoy the art of food making using either Linux, Mac, or Windows.

Side note: Tomato Engine speaks British English

### How to use it?

1. Clone this repository using `git clone`
2. Be sure to have Python3 installed
3. Go to tomato_engine folder by `cd tomato_engine`
4. Activate the tomato virtual environment with `. tomato/bin/activate`
5. Set the environment variables:

   __Linux & Mac:__

   `export FLASK_APP=search_engine.py`
   
   `export FLASK_RUN_PORT=8000`
   
   __Windows:__
   
   `set FLASK_APP=search_engine.py`
   
   `set FLASK_RUN_PORT=8000`
   
   __Windows PowerShell:__
   
   `$env:FLASK_APP = 'search_engine.py'`
   
   `$env:FLASK_RUN_PORT = '8000'`
   
   Make sure to set these every time you run a new Tomato Engine session. The virtual environment doesn't remember them.
   
6. Run Tomato Engine `flask run`
7. Go to `localhost:8000/search` in your browser to search the recipes
8. Choose ` Search exact` to search for exact match, or `Show all` to show all recipes containing searched items
9. In the search bar, type one word such as *tomato*, or connect several words using boolean values such as *tomato AND pasta*

   __NB: Be sure to type the boolean operator in UPPERCASE, otherwise the search won't work!__

10. To see the whole recipe, click on the recipe's name. You will be redirected and able to see the whole recipe
11. Check few interesting plots under *Get to know your recipes* bookmark
12. To leave Tomato Engine, simply close your browser and stop the program (`Ctrl+C` or whatever you're using). To leave the virtual environment, simply type `deactivate`

### Resources

Illustration by [Anna-Erika](https://github.com/annaerika)

Recipes from [BBC Good Food](https://www.bbcgoodfood.com/) scraped using [Webscraper](https://webscraper.io/)

Few code snippets used from [Mathias Creutz's NLP Tutorials](https://github.com/mathiascreutz/nlp-tutorials)

### Contributors

Project by Linda, Mája, and Anna-Erika

![This is fine](https://media2.giphy.com/media/QMHoU66sBXqqLqYvGO/giphy.gif)

DO JUDGE THE BOOK BY ITS COVER!!!

AT LEAST WE HAVE A VISION

<3
