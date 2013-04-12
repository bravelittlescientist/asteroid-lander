Asteroid Lander
================

Multiplayer, asteroid-mining themed game inspired by the classic Lunar Lander video game.

There isn't as much in-game documentation of the controls as we would have liked, due to a tight time-schedule. 
This may be added as a feature later. 
If you're interested in learning about the design and architecture of the game, we've included our course reports in the reports/ directory.

## Getting Started: Environment

Step 1: To Install PodSixNet

    $ cd your/path/to/asteroid-lander/PodSixNet-78

    $ sudo python setup.py install

Step 2: Make sure the top-level project directory is on the Python Path. Some IDEs (Eclipse) will do this for you, but in Ubuntu you may need the following command:

    $ export PYTHONPATH=$PYTHONPATH:/path/to/asteroid-lander/

Step 3: Install Python dependencies

    $ [pip,easy_install] jsonpickle
    $ [pip,easy_install] pygame # You need to install a bunch of headers for this to work, see the pygame site.

Step 4: Make starting scripts executable

    $ cd /path/to/asteroid-lander/game

    $ chmod +x startClientHelperScript.sh

    $ chmod +x startServerHelperScript.sh

## Getting Started: Run Server and Clients!

To run a server:
    
    $ cd path/to/asteroid-lander/game

    $ ./startServerHelperScript.sh localhost:12345

Open a new tab to run two clients, each using startClientHelperScript.sh, using the same host and port!

    $ cd path/to/steroid-lander/game

    $ ./startClientHelperScript.sh localhost:12345

Each window will open a tab! Use space to start the game, click a mineral button in the bottom right, and use arrow-keys to control your ship! 

## Known Issues

### Issue 1: Python Path (Seen on Ubuntu)

If you try to run the game and it is not on your PythonPath, it will report an error like this:

    ImportError: No module named game.Constants

The solution is to add the asteroid-lander top-level project directory to your Python Path. 

    $ export PYTHONPATH=$PYTHONPATH:/path/to/asteroid-lander/

## Image Credit

Image contents obtained from opengameart.
