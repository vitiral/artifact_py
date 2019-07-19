import os
import yaml
import unittest

from artifact_py import load

SCRIPT_PATH = os.path.realpath(__file__)
TEST_DIR = os.path.dirname(SCRIPT_PATH)


def read(path):
    with open(path) as f:
        return f.read()


def read_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


class TestArtifactsOnly:
    DIR = os.path.join(TEST_DIR, "artifacts_only")

    def run_test(self, name):
        test_name = "TEST_NAME={}.test_{}".format(self.__class__.__name__,
                                                  name)
        expected = read_yaml(os.path.join(self.DIR, name + '.yml'))
        md = os.path.join(self.DIR, name + '.md')
        project = load.from_root_file(md)
        result = project.serialize()
        root_dir = result['settings'].pop('root_dir')
        assert expected == result, test_name
        assert self.DIR == root_dir

    def test_settings(self):
        self.run_test('simple')
