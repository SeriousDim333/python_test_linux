
import yaml
from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_bad_arx):
        assert checkout_negative("cd {}; 7z e bad_arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "ERRORS"), "test2 fail"


    def test_step2(self):
        assert checkout_negative("cd {}; 7z t bad_arx.{}".format(data["folder_out"], data["type"]), "ERRORS"), "test3 fail"

