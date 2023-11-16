from files import upload_files
import pytest
from checkers import checkout, ssh_checkout, ssh_get, getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "1111",
                        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                      data["folder_ext2"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "1111",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                            data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "1111",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename, data["bs"]),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("0.0.0.0", "user2", "1111", "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout("0.0.0.0", "user2", "1111",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "1111",
                 "cd {}; 7z a -t{} {}/bad_arx".format(data["folder_in"], data["type"], data["folder_out"]),
                 "Everthing is Ok")
    ssh_checkout("0.0.0.0", "user2", "1111",
                 "truncate -s 1 {}/bad_arx.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True)
def stat(request):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = request.node.name
    # out = ssh_get("0.0.0.0", "user2", "1111", "echo '1111' | sudo -S journalctl --since '{}'".format(time))
    out = getout("echo '1111' | sudo -S journalctl --since '{}'".format(time))
    with open("stat.txt", "a", encoding="utf-8") as f, open("/proc/loadavg", "r", encoding="utf-8") as fr:
        f.write(f'{name}\ntime start: {time}\ncount = {data["count"]}, size = {data["bs"]}\nCPU load: {fr.readlines()[-1]} \nOUT:{out} \n')


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "1111", "/home/user/p7zip-full.deb",
                 "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "1111",
                            "echo '1111' | sudo -S dpkg -i /home/user2/p7zip-full.deb", "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "1111",
                            "echo '1111' | sudo -S dpkg -s p7zip-full", "Status: install ok installed"))
    res.append(ssh_checkout("0.0.0.0", "user2", "1111",
                            "echo '1111' | sudo apt install libarchive-zip-perl", ""))
    return all(res)


# @pytest.fixture(autouse=True, scope="module")
# def start_time():
#     time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     return time
#
#
# @pytest.fixture(autouse=True, scope="module")
# def safe_log(start_time):
#     with open("stat2.txt", "w") as f:
#         f.write(ssh_get("0.0.0.0", "user2", "1111", "echo '1111' | sudo -S journalctl --since '{}'".format(start_time)))
