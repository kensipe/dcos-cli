#!/bin/bash -e

BASEDIR=`dirname $0`/..

if [ ! -d "$BASEDIR/env" ]; then

    if [ ! "$(command -v pyvenv-3.5)" ]; then
      echo "Cannot find supported python version 3.5. Exiting..."
      exit 1
    fi

    pyvenv-3.5 $BASEDIR/env
    echo "Virtualenv created."

    if [ -f "$BASEDIR/env/bin/activate" ]; then
	    source $BASEDIR/env/bin/activate
    else
	    $BASEDIR/env/Scripts/activate
    fi
    echo "Virtualenv activated."

    pip install -r $BASEDIR/requirements.txt
    pip install -e $BASEDIR
    echo "Requirements installed."

elif [ ! -f "$BASEDIR/env/bin/activate" -o "$BASEDIR/setup.py" -nt "$BASEDIR/env/bin/activate" ]; then

    source $BASEDIR/env/bin/activate
    echo "Virtualenv activated."

    pip install -r $BASEDIR/requirements.txt
    pip install -e $BASEDIR
    echo "Requirements installed."

fi
