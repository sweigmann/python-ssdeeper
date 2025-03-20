Usage
=====

Import the required module.

.. code-block:: pycon

    >>> import ssdeeper

Use the :py:func:`ssdeeper.hash` function to compute a fuzzy hash.

.. code-block:: pycon

    >>> hash1 = ssdeeper.hash('Also called fuzzy hashes, Ctph can match inputs that have homologies.')
    >>> hash1
    '3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL'
    >>> hash2 = ssdeeper.hash('Also called fuzzy hashes, CTPH can match inputs that have homologies.')
    >>> hash2
    '3:AN8gu5QklJuXgcGwFEBQJaL:VglxFkL'


The :py:func:`ssdeeper.compare` function returns the match score of two hashes. The score is an integer value from 0 (no match) to 100.

.. code-block:: pycon

    >>> ssdeeper.compare(hash1, hash2)
    22

The :py:func:`ssdeeper.hash_from_file` function accepts a filename as argument and calculates the hash of the contents of the file.

.. code-block:: pycon

    >>> ssdeeper.hash_from_file('/etc/resolv.conf')
    '3:S3yE29cFrrMOoiECAaHJgvn:S3m+COoiUCuvn'

The :py:class:`ssdeeper.Hash` class provides a hashlib like interface.

.. code-block:: pycon

    >>> h = ssdeeper.Hash()
    >>> h.update('Also called fuzzy hashes, ')
    >>> h.digest()
    '3:AN8gu5QklJF:Vg6'
    >>> h.update('Ctph can match inputs that have homologies.')
    >>> h.digest()
    '3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL'
