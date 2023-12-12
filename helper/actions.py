import shutil
import subprocess

from rich import print

from helper.dir_handler import getMods, changeModState, unpackMod, uninstallMod
from helper.display import *
from helper.steam import DISABLED_MODS_PATH, ENABLED_MODS_PATH, TEMP_PATH, SELECTEDGAME


def runFunctionFromJson(function):
    try:
        globals()[function]()
    except KeyError:
        print(
            "[bold red]Function Like That does not exist[/bold red]\n[bold darkred]Exitting...[/bold darkred]")
        exit(1)


def displayEnabledMods():
    try:
        modList = getMods()
        generateModTable(modList)
    except Exception as e:
        failMessage(e)


def displayDisabledMods():
    try:
        modList = getMods(DISABLED_MODS_PATH)
        generateModTable(modList, name="Inactive Mods")
    except Exception as e:
        failMessage(e)


def enableMods():
    try:
        modList = getMods(DISABLED_MODS_PATH)
        options = generateModTable(modList, True, "Inactive Mods")
        changeModState(options, modList)
        successMessage(options, modList, "enabled")
    except Exception as e:
        failMessage(e)


def disableMods():
    try:
        modList = getMods()
        options = generateModTable(modList, True)
        changeModState(options, modList, False)
        successMessage(options, modList, "disabled")
    except Exception as e:
        failMessage(e)


def launchGame():
    try:
        command = f'steam steam://run/{SELECTEDGAME["id"]} &'
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        failMessage(e)


def addMod(mods: list):
    try:
        if not Path.exists(Path(TEMP_PATH)):
            os.makedirs(TEMP_PATH)

        unpackMod(mods)
        modList = getMods(TEMP_PATH)
        options = generateModTable(modList, True, "Mods To Add")
        changeModState(options, modList, isAdd=True)
        shutil.rmtree(TEMP_PATH)
        successMessage(options, modList, "added")
    except Exception as e:
        failMessage(e)


def removeMods():
    try:
        modList = getMods(DISABLED_MODS_PATH)
        options = generateModTable(modList, True, "Inactive Mods")
        uninstallMod(options, modList)
        successMessage(options, modList, "removed")
    except Exception as e:
        failMessage(e)
