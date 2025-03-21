python-ssdeeper
===============

This is a straightforward Python wrapper for `ssdeep by Jesse Kornblum`_, which is a library for computing context
triggered piecewise hashes (CTPH). Also called fuzzy hashes, CTPH can match inputs that have homologies. Such inputs
have sequences of identical bytes in the same order, although bytes in between these sequences may be different in both
content and length.

The ssdeeper wrapper uses the ssdeep libraries as augmented by Fraunhofer FKIE.
The specific flavor used is `ssdeep-refactored-4b-djb2-nocommonsub`_.
Scientific papers and slides on Fraunhofer FKIE's `ssdeeper version 2.14.1`_
may be found on the `DFRWS publication`_ websites.

You can install ``python-ssdeeper`` with ``pip``:

.. code-block:: console

    $ python3 -m venv $HOME/venv && $HOME/venv/bin/pip3 install git+https://codeberg.org/DFIR/python-ssdeeper

See :doc:`Installation <installation>` for more information.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   faq
   contributing
   changelog

History
=======

* The initial version was published in 2010 by `Denis Bilenko on bitbucket`_.
* Since 2012 the source is maintained by PhiBo (`DinoTools`_) and has been published on `github`_.
* In 2014 the wrapper has been rewritten to use cffi.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _ssdeep by Jesse Kornblum: https://ssdeep-project.github.io/ssdeep/
.. _Denis Bilenko on bitbucket: https://bitbucket.org/denis/ssdeep
.. _github: https://github.com/DinoTools/python-ssdeep
.. _Dinotools: https://www.dinotools.org/
.. _ssdeeper version 2.14.1: https://github.com/fkie-cad/ssdeeper
.. _ssdeep-refactored-4b-djb2-nocommonsub: https://github.com/fkie-cad/ssdeeper/tree/ssdeep-refactored-4b-djb2-nocommonsub
.. _DFRWS publication: https://dfrws.org/presentation/ssdeeper-evaluating-and-improving-ssdeep/
