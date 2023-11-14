import yaml
from checkers import ssh_checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_negativ_step1(self, make_bad_arx):
        assert ssh_checkout_negative("0.0.0.0", "user2", "1111",
                                     "cd {}; 7z e bad_arx.{} -o{} -y".format(data["folder_out"], data["type"],
                                                                             data["folder_ext"]),
                                     "ERRORS"), "test2 fail"

    def test_negative_step2(self):
        assert ssh_checkout_negative("0.0.0.0", "user2", "1111",
                                     "cd {}; 7z t bad_arx.{}".format(data["folder_out"], data["type"]),
                                     "ERRORS"), "test3 fail"
