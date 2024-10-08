import os
from configparser import ConfigParser
from pathlib import Path
import chardet


class FileLog:
    def read_version(self, minecraft_directory):
        path = os.path.join(minecraft_directory)
        file = open('version', 'a', encoding='utf-8')
        file.close()
        file = open('version', 'r', encoding='utf-8')
        while True:
            line = file.readline()
            if not line:
                break
            if path + '\n' == line:
                file.close()
                return False
        file.close()
        return True

    def write_version(self, minecraft_directory):
        path = os.path.join(minecraft_directory)
        with open('version', 'a', encoding='utf-8') as file:
            file.writelines(str(path) + '\n')
            file.close()


def read_version_and_check(path):
    file = open('version', 'a', encoding='utf-8')
    file.close()
    file = open('version', 'r', encoding='utf-8')
    while True:
        line = file.readline()
        if not line:
            break
        if path + '\n' == line:
            file.close()
            return True
    file.close()
    return False


def check_version_list():
    file = open('version', 'a')
    file.close()

    with open('version', 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open('version', 'r', encoding=encoding) as file:
        list_stings = []
        while True:
            line = file.readline()
            if not line:
                break

            if os.path.isdir(line.strip()):
                list_stings.append(line)

    with open('version', 'w', encoding=encoding) as file:
        file.writelines(list_stings)


def get_version_list():
    file = open('version', 'a', encoding='utf-8')
    file.close()
    file = open('version', 'r', encoding='utf-8')
    list_version = []
    while True:
        line = file.readline()

        if not line:
            break

        buff = ""
        for i in line[::-1]:
            if i != '\\':
                buff += i
            else:
                break

        buff = buff[::-1]

        if buff[-1] == '\n':
            buff = buff[:len(buff) - 1]

        list_version.append(buff)

    file.close()
    return list_version


def directory_path_version():
    file = open('version', 'a', encoding='utf-8')
    file.close()
    file = open('version', 'r', encoding='utf-8')
    list_directory = dict()
    while True:
        line = file.readline()

        if not line:
            break

        buff = ""
        for i in line[::-1]:
            if i != '\\':
                buff += i
            else:
                break

        buff = buff[::-1]

        if buff[-1] == '\n':
            buff = buff[:len(buff) - 1]

        list_directory[buff] = line[:len(line) - len(buff) - 2]

    file.close()
    return list_directory
