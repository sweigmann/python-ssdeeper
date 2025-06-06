"""
This is a straightforward Python wrapper for ssdeep by Jesse Kornblum,
which is a library for computing Context Triggered Piecewise Hashes (CTPH).
"""

import os
from typing import Union

# Ignore flake8 F401 warning for unused vars
from ssdeeper.__about__ import (  # noqa: F401
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)
from ssdeeper._libfuzzy import ffi, lib


class BaseError(Exception):
    """The base for all other Exceptions"""
    pass


class InternalError(BaseError):
    """Raised if lib returns internal error"""
    pass


class BaseHash(object):
    """
    Base class used to implement some general functions for the Hash and
    PseudoHash class.
    """
    @property
    def block_size(self) -> int:
        """
        The block size used to calculate the hash.
        This depends on the length of the source string.

        :return: block size
        """
        size, _, _ = self.digest().partition(":")
        return int(size)

    @property
    def name(self) -> str:
        """
        The canonical name of this hash

        :return: ssdeeper
        """
        return "ssdeeper"

    def digest(self, elimseq: bool = False, notrunc: bool = False):
        raise NotImplementedError


class Hash(BaseHash):
    """
    Hashlib like object. It is only supported with ssdeeper/libfuzzy >= 2.10.

    :raises InternalError: If lib returns internal error
    :raises NotImplementedError: Required functions are not available
    """
    def __init__(self):
        self._state = ffi.NULL

        if not hasattr(lib, "fuzzy_new"):
            raise NotImplementedError("Only supported with ssdeeper >= 2.10")

        self._state = lib.fuzzy_new()
        if self._state == ffi.NULL:
            raise InternalError("Unable to create state object")

    def copy(self) -> "Hash":
        """
        Create a copy of this hash object.

        :return: Return a copy of the hash object.
        :rtype: Hash
        :raises InternalError: If the lib returns an internal error
        """
        if self._state == ffi.NULL:
            raise InternalError("State object is NULL")

        newstate = lib.fuzzy_clone(self._state)
        if newstate == ffi.NULL:
            raise InternalError("cloning of fuzzy state object failed")

        new = Hash.__new__(Hash)
        new._state = newstate
        return new

    def update(self, buf: Union[bytes, str], encoding="utf-8") -> None:
        """
         Feed the data contained in the given buffer to the state.

        :param String|Byte buf: The data to be hashed
        :param String encoding: Encoding is used if buf is String
        :raises InternalError: If lib returns an internal error
        :raises TypeError: If buf is not Bytes, String or Unicode

        """

        if self._state == ffi.NULL:
            raise InternalError("State object is NULL")

        if isinstance(buf, str):
            buf = buf.encode(encoding)

        if not isinstance(buf, bytes):
            raise TypeError(
                "Argument must be of string, unicode or bytes type not "
                "'%r'" % type(buf)
            )

        if lib.fuzzy_update(self._state, buf, len(buf)) != 0:
            lib.fuzzy_free(self._state)
            raise InternalError("Invalid state object")

    def digest(self, elimseq: bool = False, notrunc: bool = False) -> str:
        """
        Obtain the fuzzy hash.

        This operation does not change the state at all. It reports the hash
        for the concatenation of the data previously fed using update().

        :return: The fuzzy hash
        :rtype: String
        :raises InternalError: If lib returns an internal error

        """

        if self._state == ffi.NULL:
            raise InternalError("State object is NULL")

        flags = (lib.FUZZY_FLAG_ELIMSEQ if elimseq else 0) | \
                (lib.FUZZY_FLAG_NOTRUNC if notrunc else 0)

        result = ffi.new("char[]", lib.FUZZY_MAX_RESULT)
        if lib.fuzzy_digest(self._state, result, flags) != 0:
            raise InternalError("Function returned an unexpected error code")

        return ffi.string(result).decode("ascii")

    def __del__(self):
        if self._state != ffi.NULL:
            lib.fuzzy_free(self._state)


class PseudoHash(BaseHash):
    """
    Hashlib like object. Use this class only if Hash() isn't supported by your
    ssdeeper/libfuzzy library. This class stores the provided data in memory, so
    be careful when hashing large files.

    """
    def __init__(self):
        self._data = b""

    def copy(self) -> "PseudoHash":
        """
        Create a copy of this hash object.

        :return: Return a copy of the hash object.
        :rtype: PseudoHash
        :raises InternalError: If the lib returns an internal error
        """
        new = PseudoHash()
        new.update(self._data)
        return new

    def update(self, buf: Union[bytes, str], encoding: str = "utf-8") -> None:
        """
         Feed the data contained in the given buffer to the state.

        :param String|Byte buf: The data to be hashed
        :param String encoding: Encoding is used if buf is String
        :raises TypeError: If buf is not Bytes, String or Unicode

        """

        if isinstance(buf, str):
            buf = buf.encode(encoding)

        if not isinstance(buf, bytes):
            raise TypeError(
                "Argument must be of string, unicode or bytes type not "
                "'%r'" % type(buf)
            )

        self._data = self._data + buf

    def digest(self, elimseq: bool = False, notrunc: bool = False) -> str:
        """
        Obtain the fuzzy hash.

        This operation does not change the state at all. It reports the hash
        for the concatenation of the data previously fed using update().

        :return: The fuzzy hash
        :rtype: String

        """

        return hash(self._data)


def compare(sig1: Union[bytes, str], sig2: Union[bytes, str]) -> int:
    """
    Computes the match score between two fuzzy hash signatures.

    Returns a value from zero to 100 indicating the match score of the
    two signatures. A match score of zero indicates the signatures
    did not match.

    :param Bytes|String sig1: First fuzzy hash signature
    :param Bytes|String sig2: Second fuzzy hash signature
    :return: Match score (0-100)
    :rtype: Integer
    :raises InternalError: If lib returns an internal error
    :raises TypeError: If sig is not String, Unicode or Bytes

    """

    if isinstance(sig1, str):
        sig1 = sig1.encode("ascii")
    if isinstance(sig2, str):
        sig2 = sig2.encode("ascii")

    if not isinstance(sig1, bytes):
        raise TypeError(
            "First argument must be of string, unicode or bytes type not "
            "'%s'" % type(sig1)
        )

    if not isinstance(sig2, bytes):
        raise TypeError(
            "Second argument must be of string, unicode or bytes type not "
            "'%r'" % type(sig2)
        )

    res = lib.fuzzy_compare(sig1, sig2)
    if res < 0:
        raise InternalError("Function returned an unexpected error code")

    return res


def hash(buf: Union[bytes, str], encoding: str = "utf-8") -> str:
    """
    Compute the fuzzy hash of a buffer

    :param String|Bytes buf: The data to be fuzzy hashed
    :param encoding: Encoding is used if buf is String
    :return: The fuzzy hash
    :rtype: String
    :raises InternalError: If lib returns an internal error
    :raises TypeError: If buf is not String or Bytes

    """

    if isinstance(buf, str):
        buf = buf.encode(encoding)

    if not isinstance(buf, bytes):
        raise TypeError(
            "Argument must be of string, unicode or bytes type not "
            "'%r'" % type(buf)
        )

    # allocate memory for result
    result = ffi.new("char[]", lib.FUZZY_MAX_RESULT)
    if lib.fuzzy_hash_buf(buf, len(buf), result) != 0:
        raise InternalError("Function returned an unexpected error code")

    return ffi.string(result).decode("ascii")


def hash_from_file(filename: str) -> str:
    """
    Compute the fuzzy hash of a file.

    Opens, reads, and hashes the contents of the file 'filename'

    :param filename: The name of the file to be hashed
    :return: The fuzzy hash of the file
    :rtype: String
    :raises IOError: If Python is unable to read the file
    :raises InternalError: If lib returns an internal error

    """

    if not os.path.exists(filename):
        raise IOError("Path not found")
    if not os.path.isfile(filename):
        raise IOError("File not found")
    if not os.access(filename, os.R_OK):
        raise IOError("File is not readable")

    result = ffi.new("char[]", lib.FUZZY_MAX_RESULT)
    if lib.fuzzy_hash_filename(filename.encode("utf-8"), result) != 0:
        raise InternalError("Function returned an unexpected error code")

    return ffi.string(result).decode("ascii")
