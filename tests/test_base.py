import os
import shutil
import tempfile
from unittest import TestCase

from excelcy import ExcelCy


class BaseTestCase(TestCase):
    test_data_path = None  # type: str

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls.setup_class()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCase, cls).tearDownClass()
        cls.teardown_class()

    @classmethod
    def setup_class(cls):
        # set path
        current_path = os.path.dirname(os.path.abspath(__file__))
        cls.test_data_path = os.path.join(current_path, 'data')

    @classmethod
    def teardown_class(cls):
        pass

    @classmethod
    def get_test_data_path(cls, fs_path: str):
        return os.path.join(cls.test_data_path, fs_path)

    @classmethod
    def get_test_tmp_path(cls, fs_path: str):
        return os.path.join(tempfile.gettempdir(), fs_path)

    def assert_training(self, file_path: str, entity_tests: dict = None):
        excelcy = ExcelCy.execute(file_path=file_path)
        nlp = excelcy.nlp
        for idx, train in excelcy.storage.train.items.items():
            train_ents = set([(gold.subtext, gold.entity) for _, gold in train.items.items()])
            doc = nlp(train.text)
            ents = set([(ent.text, ent.label_) for ent in doc.ents])
            # verify based on data
            assert train_ents <= ents
            # verify if test given
            test = (entity_tests or {}).get(idx, set())
            assert test <= ents
