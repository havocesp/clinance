#!/usr/bin/env bash

if ! which git &> /dev/null
then
    echo " - [ERROR] git command could not be located please install it and try again."
fi

if ! which python3 &> /dev/null && ! which python &> /dev/null
then
    echo " - [ERROR] python3 could not be located please install it and try again."
fi

if ! which pip3 &> /dev/null && ! which pip &> /dev/null
then
    echo " - [ERROR] python3 could not be located please install it and try again."
fi

if [ -d './venv' ] && [ -f './venv/bin/activate' ]
then

    echo "Activating python virtual environment ... "
    source './venv/bin/activate'
fi

echo "Installing dependencies ... "
pip install -U git+https://github.com/havocesp/panance || pip3 install -U git+https://github.com/havocesp/panance
pip install -U git+https://github.com/havocesp/finta || pip3 install -U git+https://github.com/havocesp/finta
pip install -U tabulate || pip3 install -U tabulate
pip install -U defopt || pip3 install -U defopt
echo "DONE"

if declare | grep -iq -E  ^deactivate
then
    deactivate &> /dev/null
fi
