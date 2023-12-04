from os import walk
from helper.display import *
from rich import print
from helper.steam import DISABLED_MODS_PATH
from helper.dir_handler import getMods, moveMod


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
    moveMod(options, modList)


def disableMods():
    pass
