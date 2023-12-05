import os
import shutil

from helper.steam import ENABLED_MODS_PATH, DISABLED_MODS_PATH
from helper.mods import File


def getMods(path=ENABLED_MODS_PATH):
    files_list = []
    index = 0
    for folder_path, _, file_names in os.walk(path):
        for file_name in file_names:
            file_path = os.path.relpath(folder_path, path)
            files_list.append(File(id=index, name=file_name, path=file_path))
            index += 1
    return files_list


def understandOption(option: str):
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


def moveMod(option, modList, isEnable=True):
    if isEnable:
        pathFrom, pathTo = DISABLED_MODS_PATH, ENABLED_MODS_PATH
    else:
        pathFrom, pathTo = ENABLED_MODS_PATH, DISABLED_MODS_PATH
    parsedOption = understandOption(option)

    for i in parsedOption:
        tempPathFrom = f'{pathFrom}/{modList[i - 1].path}/{modList[i - 1].name}'
        tempPathTo = f'{pathTo}/{modList[i - 1].path}/{modList[i - 1].name}'
        try:
            shutil.move(tempPathFrom, tempPathTo)
        except FileNotFoundError:
            os.makedirs(f'{pathTo}/{modList[i - 1].path}/')
            shutil.move(tempPathFrom, tempPathTo)




def addMod():
    pass