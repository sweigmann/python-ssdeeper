#!/usr/bin/env python3
import pytest
import ssdeeper


class TestFunctionsFail(object):
    def test_compare(self):
        with pytest.raises(TypeError):
            ssdeeper.compare(
                "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL",
                None
            )

        with pytest.raises(TypeError):
            ssdeeper.compare(
                None,
                "3:AXGBicFlIHBGcL6wCrFQEv:AXGH6xLsr2C"
            )

        with pytest.raises(ssdeeper.InternalError):
            ssdeeper.compare(
                "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL",
                ""
            )

    def test_hash(self):
        with pytest.raises(TypeError):
            ssdeeper.hash(None)

        with pytest.raises(TypeError):
            ssdeeper.hash(1234)


class TestFunctions(object):
    def test_compare(self):
        res = ssdeeper.compare(
            "3:AXGBicFlgVNhBGcL6wCrFQEv:AXGHsNhxLsr2C",
            "3:AXGBicFlIHBGcL6wCrFQEv:AXGH6xLsr2C"
        )
        assert res == 44

        res = ssdeeper.compare(
            b"3:AXGBicFlIHBGcL6wCrFQEv:AXGH6xLsr2C",
            b"3:AXGBicFlgVNhBGcL6wCrFQEv:AXGHsNhxLsr2C"
        )
        assert res == 44

    def test_hash_1(self):
        res = ssdeeper.hash("Also called fuzzy hashes, Ctph can match inputs that have homologies.")
        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"

    def test_hash_2(self):
        res = ssdeeper.hash("Also called fuzzy hashes, CTPH can match inputs that have homologies.")
        assert res == "3:AN8gu5QklJuXgcGwFEBQJaL:VglxFkL"

    def test_hash_3(self):
        res = ssdeeper.hash(b"Also called fuzzy hashes, CTPH can match inputs that have homologies.")
        assert res == "3:AN8gu5QklJuXgcGwFEBQJaL:VglxFkL"

    def test_hash_from_file(self):
        with pytest.raises(IOError):
            ssdeeper.hash_from_file("tests/files/")

        with pytest.raises(IOError):
            ssdeeper.hash_from_file("tests/files/file-does-not-exist.txt")

        res = ssdeeper.hash_from_file("tests/files/file.txt")
        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJab:VgDhxFkb"


class TestHashClass(object):
    def test_copy(self):
        obj = ssdeeper.Hash()
        obj.update("Also called fuzzy hashes, ")
        new_obj = obj.copy()
        assert isinstance(new_obj, ssdeeper.Hash)

        res = obj.digest()
        new_res = new_obj.digest()
        assert res == "3:AN8gu5QklJF:Vg6"
        assert new_res == "3:AN8gu5QklJF:Vg6"

        # Update only original object
        obj.update("Ctph can match inputs that have homologies.")

        res = obj.digest()
        new_res = new_obj.digest()
        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"
        assert new_res == "3:AN8gu5QklJF:Vg6"

        # Update only new object
        new_obj.update("Ctph can match inputs that have homologies.")
        res = obj.digest()
        new_res = new_obj.digest()
        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"
        assert new_res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"

    def test_hashlib(self):
        obj = ssdeeper.Hash()
        assert obj.name == "ssdeeper"

        obj.update("Ctph can match inputs that have homologies.")
        assert obj.block_size == 3

    def test_update(self):
        obj = ssdeeper.Hash()
        obj.update("Also called fuzzy hashes, Ctph can match inputs that have homologies.")
        res = obj.digest()

        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"


class TestPseudoHashClass(object):
    def test_copy(self):
        obj = ssdeeper.PseudoHash()
        obj.update("Also called fuzzy hashes, ")
        new_obj = obj.copy()
        assert isinstance(new_obj, ssdeeper.PseudoHash)

        res = obj.digest()
        new_res = new_obj.digest()
        assert res == "3:AN8gu5QklJF:Vg6"
        assert new_res == "3:AN8gu5QklJF:Vg6"

        # Update only original object
        obj.update("Ctph can match inputs that have homologies.")

        res = obj.digest()
        new_res = new_obj.digest()
        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"
        assert new_res == "3:AN8gu5QklJF:Vg6"

        # Update only new object
        new_obj.update("Ctph can match inputs that have homologies.")
        res = obj.digest()
        new_res = new_obj.digest()
        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"
        assert new_res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"

    def test_hashlib(self):
        obj = ssdeeper.PseudoHash()
        assert obj.name == "ssdeeper"

        obj.update("Ctph can match inputs that have homologies.")
        assert obj.block_size == 3

    def test_update(self):
        obj = ssdeeper.PseudoHash()
        obj.update("Also called fuzzy hashes, ")
        obj.update("Ctph can match inputs that have homologies.")
        res = obj.digest()

        assert res == "3:AN8gu5QklJgVNhyEgcGwFEBQJaL:VgDhxFkL"


class TestHashClassFail(object):
    def test_update_01(self):
        obj = ssdeeper.Hash()
        with pytest.raises(TypeError):
            obj.update(None)

    def test_update_02(self):
        obj = ssdeeper.Hash()
        with pytest.raises(TypeError):
            obj.update(1234)


class TestPseudoHashClassFail(object):
    def test_update_01(self):
        obj = ssdeeper.PseudoHash()
        with pytest.raises(TypeError):
            obj.update(None)

    def test_update_02(self):
        obj = ssdeeper.PseudoHash()
        with pytest.raises(TypeError):
            obj.update(1234)
