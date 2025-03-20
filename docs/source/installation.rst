Installation
============

Requirements
------------

* Python

  * Python >= 3.8
  * PyPy >= 2.0

* ssdeeper/libfuzzy >= 2.10 (Some features might not be available with older versions. See :py:class:`ssdeep.Hash`)
* cffi
* pip
* six

Install on Debian
-----------------

**Use included ssdeep lib**

Since ssdeeper is an augmented version of ssdeep, the included lib must always be built.

Install required packages.

.. code-block:: console

    $ sudo apt-get install build-essential libffi-dev python3-full python3-dev python3-pip automake autoconf libtool

Build and install Python module.

.. code-block:: console

    $ python3 -m venv $HOME/venv && BUILD_LIB=1 $HOME/venv/bin/pip3 install git+https://codeberg.org/DFIR/python-ssdeeper

Install on Fedora
-----------------

**Use included ssdeep lib**

Since ssdeeper is an augmented version of ssdeep, the included lib must always be built.

Install required packages.

.. code-block:: console

    $ sudo dnf groupinstall "Development Tools"
    $ sudo dnf install libffi-devel python3-devel python3-pip ssdeep-devel

Build and install Python module.

.. code-block:: console

    $ python3 -m venv $HOME/venv && BUILD_LIB=1 $HOME/venv/bin/pip3 install git+https://codeberg.org/DFIR/python-ssdeeper
