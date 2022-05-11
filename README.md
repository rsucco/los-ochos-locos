# doubleskunk

Terminal-based crazy eights card game

#### Setup:

##### Arch Linux:
    sudo pacman -S python python-colorama python-pyfiglet
##### Ubuntu:
    sudo apt update && sudo apt install python3 python3-pip -y
    sudo pip3 install colorama pyfiglet
##### Gentoo:
    sudo emerge dev-lang/python dev-python/pip
    sudo pip3 install --user colorama pyfiglet
##### FreeBSD:
    sudo pkg install python3 py38-pip
    pip install colorama pyfiglet
##### macOS:
Note: If you don't have [Homebrew](https://brew.sh/) installed already, you'll have to install it first.

    brew install python
    sudo -H pip3 install colorama pyfiglet
##### Windows:
Note: If you don't have [Chocolatey](https://chocolatey.org/) installed already, you'll have to install it first.
Python 3.6+ is required, but if you're using a different version than 3.8, replace 'Python38' with the correct directory
name below. Run these commands in an Administrator PowerShell terminal.

    choco install python pip
    C:\Python38\Scripts\pip3.exe install colorama pyfiglet

#### Play:
##### Linux/BSD/macOS

    ./los-ochos-locos.py

##### Windows
Note: If you have a version of Python 3 installed other than Python 3.8, change the path here accordingly.
If you followed the setup instructions above, this should work.

    C:\Python38\python.exe .\los-ochos-locos.py

You can use the `-p` flag to set 1-4 human players, or just launch the game with no flags and select your difficulty from the game's menu.

#### Release Notes:

##### 0.1 (10MAY202):
Crazy eights is such a simple game that this ended up not taking very long to make. I was able to reuse a lot of code from the doubleskunk project,
especially for rendering the UI. Overall, not a super in-depth game and not something I'm likely to return to, but I plan to re-use a lot of the UI
work for other non-cribbage terminal card games in the future.
