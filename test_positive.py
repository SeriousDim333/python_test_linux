import subprocess

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    """
    архивирование файлов (а)
    """
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "test1 fail"


def test_step6():
    """
    список файлов (l)
    """
    result1 = checkout("cd {}; 7z l arx2.7z".format(out), "qwer")
    result2 = checkout("cd {}; 7z l arx2.7z".format(out), "asdf")
    assert result1 and result2, "test6 fail"


def test_step8():
    """
    хэш архива (h)
    """
    result = subprocess.run("cd {}; 7z h arx2.7z".format(out), shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    text = result.stdout.split()
    result2 = checkout("cd {}; crc32 arx2.7z".format(out), text[-4].lower())
    assert result2, "test8 fail"


def test_step2():
    """
    разархивирование (е)
    """
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "qwer")
    result3 = checkout("cd {}; ls".format(folder1), "asdf")
    assert result1 and result2 and result3, "test2 fail"


def test_step7():
    """
    разархивирование с сохранением структуры (х)
    """
    result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(out, folder2), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder2), "qwer")
    result3 = checkout("cd {}/q; ls".format(folder2), "asdf")
    assert result1 and result2 and result3, "test7 fail"


def test_step3():
    """
    целостность архива (t)
    """
    assert checkout("cd {}; 7z t arx2.7z".format(out), "Everything is Ok"), "test3 fail"


def test_step4():
    """
    обновление файлов в архиве (u)
    """
    assert checkout("cd {}; 7z u ../out/arx2.7z".format(tst), "Everything is Ok"), "test4 fail"


def test_step5():
    """
    удаление файлов из архива (d)
    """
    assert checkout("cd {}; 7z d arx2.7z".format(out), "Everything is Ok"), "test3 fail"
