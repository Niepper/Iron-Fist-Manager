import os
import pathlib
import shutil

from helper.file import File
from helper.steam import ENABLED_MODS_PATH, DISABLED_MODS_PATH, TEMP_PATH


def getMods(path=ENABLED_MODS_PATH):
    files_list = []
    index = 0
    for folder_path, _, file_names in os.walk(path):
        for file_name in file_names:
            file_path = os.path.relpath(folder_path, path)
            files_list.append(File(id=index, name=file_name, path=file_path))
            index += 1
    return files_list


def parseOptions(option: str):
    final = []
    temp = option.split(",")
    for i in temp:
        try:
            final.append(int(i))
        except ValueError:
            for a in i.split():
                if a.isalpha():
                    i = i.replace(a, "")
            if "-" in i:
                a, b = i.split("-")
                for j in range(int(a), int(b) + 1):
                    final.append(j)
            elif "!" in i:
                final.pop(int(i.replace("!", "")) - 1)
    return final


def changeModState(option, modList, isEnable=True, isAdd=False, isCSV=False):
    if isEnable:
        pathFrom, pathTo = DISABLED_MODS_PATH, ENABLED_MODS_PATH
    elif not isAdd:
        pathFrom, pathTo = ENABLED_MODS_PATH, DISABLED_MODS_PATH

    if isAdd:
        pathFrom, pathTo = TEMP_PATH, ENABLED_MODS_PATH

    parsedOption = parseOptions(option)

    for i in parsedOption:
        tempPathFrom = f'{pathFrom}/{modList[i - 1].path}/{modList[i - 1].name}'
        tempPathTo = f'{pathTo}/{modList[i - 1].path}/{modList[i - 1].name}'
        try:
            shutil.move(tempPathFrom, tempPathTo)
        except FileNotFoundError:
            os.makedirs(f'{pathTo}/{modList[i - 1].path}/')
            shutil.move(tempPathFrom, tempPathTo)


def unpackOnly(ArchivePath, ExtractPath):
    ExtractPath = pathlib.Path(ExtractPath)
    shutil.unpack_archive(ArchivePath, ExtractPath)

    for file_path in ExtractPath.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() not in {'.pak', '.csv'}:
            file_path.unlink()


def unpackMod(mods: list):
    mods = list(map(lambda a: pathlib.Path(a).absolute(), mods))

    for i in mods:
        if i.suffix.lower() in [".zip", ".rar"]:
            shutil.unpack_archive(i, TEMP_PATH)
            unpackOnly(i, TEMP_PATH)
        elif i.suffix.lower() == ".pak":
            shutil.move(i, TEMP_PATH + i.name)
        else:
            pass


def uninstallMod(option, modList):
    parsedOption = parseOptions(option)

    for i in parsedOption:
        tempPath = f'{DISABLED_MODS_PATH}/{modList[i - 1].path}/{modList[i - 1].name}'
        os.remove(tempPath)
