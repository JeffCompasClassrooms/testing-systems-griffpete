import os
import pytest
from pytest import fixture
from mydb import MyDB


def describe_MyDB():
    @fixture
    def test_db_file(tmp_path):
        db_file = tmp_path / "test_db.pkl"
        yield str(db_file)
        if os.path.exists(str(db_file)):
            os.remove(str(db_file))

    def describe_init():
        def store_filename(test_db_file):
            db = MyDB(test_db_file)
            assert db.fname == test_db_file

        def do_not_overite_existing_file(test_db_file):
            db1 = MyDB(test_db_file)
            db1.saveStrings(["existing_data"])
            db2 = MyDB(test_db_file)
            data = db2.loadStrings()
            assert data == ["existing_data"]

        def make_list_for_new_db(test_db_file):
            db = MyDB(test_db_file)
            data = db.loadStrings()
            assert data == []
            assert isinstance(data, list)


    def describe_loadStrings():
        def load_empty_list(test_db_file):
            db = MyDB(test_db_file)
            result = db.loadStrings()
            assert result == []

        def loads_single_string(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["hello"])
            result = db.loadStrings()
            assert result == ["hello"]

        def loads_multiple_strings(test_db_file):
            db = MyDB(test_db_file)
            test_data = ["first", "second", "third"]
            db.saveStrings(test_data)
            result = db.loadStrings()
            assert result == test_data


    def describe_saveStrings():
        def saves_empty_array(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings([])
            result = db.loadStrings()
            assert result == []

        def saves_multiple_strings(test_db_file):
            db = MyDB(test_db_file)
            test_data = ["one", "two", "three"]
            db.saveStrings(test_data)
            result = db.loadStrings()
            assert result == test_data

        def overwrites_existing_data(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["old_data"])
            db.saveStrings(["new_data"])
            result = db.loadStrings()
            assert result == ["new_data"]
            assert "old_data" not in result


    def describe_saveString():
        def appends_string_new(test_db_file):
            db = MyDB(test_db_file)
            db.saveString("first")
            result = db.loadStrings()
            assert result == ["first"]

        def appends_string_to_existing(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["existing"])
            db.saveString("new")
            result = db.loadStrings()
            assert result == ["existing", "new"]

        def appends_empty_string(test_db_file):
            db = MyDB(test_db_file)
            db.saveStrings(["existing"])
            db.saveString("")
            result = db.loadStrings()
            assert result == ["existing", ""]
