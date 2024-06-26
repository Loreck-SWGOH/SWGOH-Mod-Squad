# SWGOH Mod Squad

This web application is used to help players of Star Wars Galaxy of Heros (SWGOH) apply and manage mods on teams of characters. Players who are only interested in applying mods to their characters can use the static web site located [here](https://loreck-swgoh.github.io/SWGOH-Mod-Squad/). If you are interested in doing more you install the web app using the below instructions.

This application uses the Flask framework coded in Python to track the typical mods applied to characters in SWGOH. SWGOH is divided into groups of events. Some of these events are always present, some events are guild driven, and other events are started by the game. Within each event category, there are specific events that allow players to interact with other players or the game. Players interact via teams.

Teams in SWGOH are comprised of different characters which can be obtained via shards earned via game play. Characters gain attributes such as speed and health by increasing the type of gear they own.

Along with the gear, characters can increase their attributes via mods. Unlike gear, mods can be added or removed from characters at will. Hence, the use of mods allow players to fine-tune the strengths of their characters.

Unfortunately, there many sources of mod suggestions. Players are often overwhelmed by these choices and this application will try to tabulate some of the more common mod suggestions.

The original code base was created by [Rickard Stureborg](http://www.rickard.stureborg.com) and [Yihao Hu](https://www.linkedin.com/in/yihaoh/) for Duke CPS 316 Fall 2021 projects.  Amended by various teaching staff in subsequent years. Amended for this project by George Hugh.

## Create Developmental/Run-time Environments

The environments for this web application are contained in Docker instances. Docker instances are computer processes that run on your PC. These processes are 'images' that are pre-loaded with the software needed to run the app's Python code and interact with the app's databases. The other method would be to load database servers and clients on your PC. Using the Docker instance(s) obviates the need for software bloat on your PC.

All instructions and files needed to create the Docker instances are contained in the docker directory of this repository. Follow the [instructions](docker/README.md) in that repository directory to install and set up your Docker instance.

## Code Development

Visual Studio Code (VS Code) is the recommended IDE for this project, though you are free to use the IDE of your choice. If you choose another IDE you'll want the capabilities of remote development, Linux shell exectution, and Python code development.

Follow these [instructions](https://code.visualstudio.com/) to install VS Code. Start VS Code and install the following extensions (from the left side menus):

* Remote Development (Microsoft)
* Python (Microsoft)

### Connecting to Docker Container

With the `Remote Development` extension installed in VS Code you can continue development of this application within the Docker container.

Make sure that your Docker containers are running and select the `Open a Remote Window` icon in the bottom left corner of the VS Code window. Select `Attach to Running Container ...` from the dropdown menu of the search box. Select the Ubuntu container.

At this point you can open the git folder located in your `shared` directory. Changes can be committed then synced with your GitHub repository.

### Creating the Application Environment

This web app uses `poetry` for dependency management. Use of `poetry` ensures that all Python dependencies are installed in the system. In your container shell, change into the repository directory and
run ./install.sh.  This will install the application's dependecies, create the all-important .env file, and creates a simple
PostgreSQL database named `mod_squad`.

Since the Docker container is essentially a separate machine from your PC, you'll want to install the following VS Code extensions (from the left side menus):

* Python (Microsoft)

This may require that you select a Python interpreter.


## Running/Stopping the Website

To run the web application you will need to be in the `poetry` environment. Issue the following commands to run the application:
```
poetry shell
flask run
```

The first command ensures that you are running within the `poetry` environment while the second command runs the web server (Flask). Do NOT run Flask outside the `poetry` environment; you will get errors.

You can now use your laptop's browser to explore the website. Depending on your setup, the URL will be different:

* If you use containers on your own laptop, point your browser to http://localhost:8080/

* To stop your app, type <kbd>CTRL</kbd>-<kbd>C</kbd> in the container shell; that will take you back to the command-line prompt, still inside the `poetry` environment. If you are all done with this app for
now, you can type `exit` to leave the `poetry` environment and return to the normal container shell.

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `mod_squad`
behind the scene.  As part of the installation procedure above, this
database has been created automatically for you.  You can access the
database directly by running the command `psql mod_squae` in your VM.

For debugging, you can access the database while the Flask server is
running.  We recommend you open a second container shell to run `psql
amazon`.  After you perform some action on the website, you run a
query inside `psql` to see the action has the intended effect on the
database.

The `db/` subdirectory of this repository contains files useful for
(re-)initializing the database if needed.  To (re-)initialize the
database, first make sure that you are NOT running your Flask server
or any `psql` sessions; then, from your repository directory, run
`db/setup.sh`.

* You will see lots of text flying by --- make sure you go through
  them carefully and verify there was no errors.  Any error in
  (re-)initializing the database will cause your Flask server to fail,
  so make sure you fix them.

* If you get `ERROR: database "mod_squad" is being accessed by other
  users`, that means you likely have Flask or another `psql` still
  running; terminate them and re-run `db/setup.sh`.  If you cannot
  seem to find where you are running them, a sure way to get rid of
  them is to stop/start your container.

To change the database schema, modify `db/create.sql` and
`db/load.sql` as needed.  Make sure you run `db/setup.sh` to reflect
the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to
initialize the database contents when you run `db/setup.sh`.  Under
`db/generated/`, you will find alternate CSV files that will be used
to initialize a bigger database instance when you run `db/setup.sh
generated`; these files are automatically generated by running a
script (which you can re-run by going inside `db/data/generated/` and
running `python gen.py`.

* Note that PostgreSQL does NOT store data inside these CSV files; it
  store data on disk files using an efficient, binary format.  In
  other words, if you change your database contents through your
  website or through `psql`, you will NOT see these changes reflected
  in these CSV files (but you can see them through `psql mod_squad`).

* For safety, a database should never store password in plain text;
  instead it stores one-way hash of the password.  This rule applies
  to the password value in the CSV files too.  To see what hashed
  password value you should put in a CSV file, see `db/data/gen.py`
  for example of how to compute the hashed value.


## Note on Hiding Credentials

Use the file `.flaskenv` for passwords/secret keys --- we are talking about passwords used to access your database server, for example (not user passwords for your website in CSV files for loading sample database).  This file is NOT tracked by `git` and it was automatically generated when you first ran `./install.sh`.  Don't check it into `git` because your credentials would be exposed to everybody on GitHub if you are not careful.
