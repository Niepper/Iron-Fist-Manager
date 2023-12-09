import os
import shutil
import subprocess
from os import walk
from helper.display import *
from rich import print
from helper.steam import DISABLED_MODS_PATH, ENABLED_MODS_PATH, TEMP_PATH
from helper.dir_handler import getMods, changeModState, unpackMod


def runFunctionFromJson(function):
    try:
        globals()[function]()
    except KeyError:
        print(
            "[bold red]Function Like That does not exist[/bold red]\n[bold darkred]Exitting[blink]...[/blink][/bold darkred]")
        exit(1)


def displayEnabledMods():
    modList = getMods()
    generateModTable(modList)


def displayDisabledMods():
    modList = getMods(DISABLED_MODS_PATH)
    generateModTable(modList, name="Inactive")


def enableMods():
    modList = getMods(DISABLED_MODS_PATH)
    options = generateModTable(modList, True, "Inactive")
    changeModState(options, modList)


def disableMods():
    modList = getMods(ENABLED_MODS_PATH)
    options = generateModTable(modList, True, "Active")
    changeModState(options, modList, False)


def launchGame():
    command = "steam steam://run/389730 &"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)


def addMod(mods: list):
    if not Path.exists(Path(TEMP_PATH)):
        os.makedirs(TEMP_PATH)

    unpackMod(mods)
    modList = getMods(TEMP_PATH)
    options = generateModTable(modList, True, "Soon to be added")
    changeModState(options, modList, isAdd=True)
    shutil.rmtree(TEMP_PATH)


def removeMod():
    modList = getMods(DISABLED_MODS_PATH)
    options = generateModTable(modList, True, "Active")
    removeMod(options, modList)
