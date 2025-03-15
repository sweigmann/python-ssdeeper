ssdeeper Python Wrapper
=======================

Forked from: https://github.com/DinoTools/python-ssdeep

This is a straightforward Python wrapper for `ssdeep by Jesse Kornblum`_, which is a library for computing context
triggered piecewise hashes (CTPH). Also called fuzzy hashes, CTPH can match inputs that have homologies. Such inputs
have sequences of identical bytes in the same order, although bytes in between these sequences may be different in both
content and length.

The ssdeeper wrapper uses the ssdeep libraries as augmented by Fraunhofer FKIE. 
The specific flavor used is `ssdeep-refactored-4b-djb2-nocommonsub`_. 
Scientific papers and slides on Fraunhofer FKIE's `ssdeeper version 2.14.1`_ 
may be found on the `DFRWS publication`_ websites. 
 
How to use it
=============

To compute a fuzzy hash, use ``hash`` function:

.. code-block:: pycon

    >>> import ssdeeper
    >>> hash1 = ssdeeper.hash('Also called fuzzy hashes, Ctph can match inputs that have homologies.')
    >>> hash1
    '3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL'
    >>> hash2 = ssdeeper.hash('Also called fuzzy hashes, CTPH can match inputs that have homologies.')
    >>> hash2
    '3:AN8gu5QklJuXgcGwFEBQJaL:VglxFkL'

The ``compare`` function returns the match between 2 hashes, an integer value from 0 (no match) to 100.

.. code-block:: pycon

    >>> ssdeeper.compare(hash1, hash2)
    28


More examples are available in the `python-ssdeep documentation`_.

Install
=======

If all requirements are met it is possible to install the wrapper by using pip or easy_install.

.. code-block:: console

    $ pip install git+https://codeberg.org/DFIR/python-ssdeeper

The build will always use the included version of the ssdeep library.

For more information have a look at the `python-ssdeep documentation`_.

Tested on ...
=============

* CentOS 7
* Debian 8, 9, 13
* Ubuntu 14.04, 16.04, 18.04

Documentation
=============

Feel free to use the prebuild `python-ssdeep documentation`_ or use the steps below to build the documentation.

.. code-block:: console

    $ cd docs
    $ pip install -r requirements.txt
    $ make html

Licensing
=========

The code is licensed under the terms of the LGPLv3+.

This wrapper includes the unchanged source distribution of `ssdeep version 2.14.1`_. It is licensed under the GPLv2.

.. _ssdeep by Jesse Kornblum: https://ssdeep-project.github.io/ssdeep/
.. _ssdeep version 2.14.1: https://github.com/ssdeep-project/ssdeep/releases/tag/release-2.14.1
.. _python-ssdeep documentation: https://python-ssdeep.readthedocs.io
.. _ssdeeper version 2.14.1: https://github.com/fkie-cad/ssdeeper
.. _ssdeep-refactored-4b-djb2-nocommonsub: https://github.com/fkie-cad/ssdeeper/tree/ssdeep-refactored-4b-djb2-nocommonsub
.. _DFRWS publication: https://dfrws.org/presentation/ssdeeper-evaluating-and-improving-ssdeep/