
import yaml
from checkers import checkout, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files):
        """
        архивирование файлов (а)
        """
        result1 = checkout("cd {}; 7z a -t{} {}/arx2".format( data["folder_in"], data["type"], data["folder_out"]), "Everything is Ok")
        result2 = checkout("ls {}".format(data["folder_out"]), "arx2.{}".format(data["type"]))
        assert result1 and result2, "test1 fail"


    def test_step2(self, clear_folders, make_files):
        """
        разархивирование (е)
        """
        res = []
        res.append(checkout("cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data["type"], data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res), "test2 fail"


    def test_step3(self):
        """
        целостность архива (t)
        """
        assert checkout("cd {}; 7z t arx2.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test3 fail"


    def test_step4(self):
        """
        обновление файлов в архиве (u)
        """
        assert checkout("cd {}; 7z u ../out/arx2.{}".format(data["folder_in"],data["type"]), "Everything is Ok"), "test4 fail"


    def test_step5(self, clear_folders, make_files):
        """
        список файлов (l)
        """
        res = []
        res.append(checkout("cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data["type"], data["folder_out"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arx2.{}".format(data["folder_out"], data["type"]), item))
        assert all(res), "test5 fail"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        """
        разархивирование с сохранением структуры (х)
        """
        res = []
        res.append(checkout("cd {}; 7z a -t{} {}/arx".format(data["folder_in"], data["type"], data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))

        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), item))

        res.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 fail"

    def test_step7(self):
        """
        удаление файлов из архива (d)
        """
        assert checkout("cd {}; 7z d arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"), "test7 fail"

    def test_step8(self, clear_folders, make_files):
        """
        хэш архива (h)
        """
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), hash))
        assert all(res), "test8 fail"



