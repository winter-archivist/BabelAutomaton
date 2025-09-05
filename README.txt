#-----------#
Project Description
#-----------#
A GNU GPL v3 Licensed Discord Bot made for a friend to be used as a language learning assistant for a college group learning American Sign Language.
You, or a group, can make a dictionary, or multiple dictionaries, of words that you can then get a random word from.

In most comments/description you'll see me using the word "Automaton" to describe the bot, this is purely because I like the word Automaton. :)
I am using this project as a way to teach/reteach myself some things, if you have any feedback please see the contact section of the README.

#-----------#
Project Goals
#-----------#
Individual & Group ID Based Dictionaries
Dictionary Selection so you can do this for multiple languages

#-----------#
Contact
#-----------#
Discord : .w1ll0w3
Github  : winter-archivist
Email   : ashen_entropy@proton.me

#-----------#
SETUP GUIDE
#-----------#
The following package assumes that you're running on Ubuntu, or its derivatives like Kubuntu, Xubuntu, Mint, etc.

Update your system, this may take a while depending on your system & connection
    sudo apt update && sudo apt upgrade

Install python3
    sudo apt install python3

cd into Babel_Automaton
Run this once to make the virtual environment, I prefer .venv
    python3 -m venv .venv

To enter the venv run
    source .venv/bin/activate

Once in the venv, run this once to install all requirements
    python3 -m pip install -r requirements.txt

Before running the automaton make sure to setup its config
    python3 config_setup.py

Once in venv, run this to run the actual Automaton
    python3 main.py
#-----------#