FAQ
===

**If comparing two hashes the result is always 0**

The result depends on the algorithms in the ssdeep library. There are some issues if the length of provided data is too short or if the algorithm could not find enough patterns.

The following example must not return the expected value.

.. code-block:: pycon

    >>> hash1 = ssdeeper.hash('foo')
    >>> hash2 = ssdeeper.hash('foo')
    >>> ssdeeper.compare(hash1, hash2)
    0
