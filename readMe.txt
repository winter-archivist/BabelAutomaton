#-----------#
Project Description
#-----------#
A GNU GPL v3 Licensed Discord Bot made for a friend to be used as a language learning assistant for a college group learning American Sign Language.
This project will never use AI in any way shape or form.

You, or a group, can make a dictionary, or multiple dictionaries, of words that you can then get a random word from as well as assign definitions to said words

In most comments/description you'll see me using the word "Automaton" to describe the bot, this is purely because I like the word Automaton. :)
I am using this project as a way to teach/reteach myself some things, if you have any feedback please see the contact section of the README.

#-----------#
Contact
#-----------#
Discord : .w1ll0w3
Github  : winter-archivist
Email   : ashen_entropy@proton.me

#-----------#
SETUP GUIDE
#-----------#
The following provides guidance for both Debian or Arch. I have personally tested this on Ubuntu & EndeavourOS.

Update your system, this may take a while depending on your system & connection
Debian:    sudo apt update && sudo apt upgrade
Arch:      sudo pacman -Syu

Install python & pip for your distro
Debian:    sudo apt install python3 python3-pip
Arch:      sudo pacman -S python python-pip
Moving forward if a command says "python" and you're on Debian use "python3" instead.

cd into BabelAutomaton/
Run this once to make the virtual environment, I prefer .venv
    python -m venv .venv

To enter the venv run
    source .venv/bin/activate

Once in the virtual environment, run this once to install all requirements
    python -m pip install -r requirements.txt

Before running the automaton make sure to run configSetup.py
    python configSetup.py

Once the config is generated, ensure the automaton's token is in a file named ".client.secret" in the Automaton/ directory
The client's token is found under the Bot section of the discord dev portal. !DO NOT SHARE THIS TOKEN!

Once in the virtual environment, run this to run the actual Automaton
    python Automaton/main.py
#-----------#