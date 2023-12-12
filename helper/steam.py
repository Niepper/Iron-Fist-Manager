import json as js
import os
from pathlib import Path


def getGame():
    jsonPath = Path("./configs/gamesList.json")
    with open(jsonPath) as file:
        return js.load(file)


currGame = getGame()

SELECTED_GAME = currGame["games"][currGame["currentlySelected"]]


def getSteamGameLocation():
    steamLinuxRoot = os.path.expanduser("~/.steam/steam")
    libraryFolders = [steamLinuxRoot]
    gameId = SELECTED_GAME["id"]
    # Check if the Steam library folders file exists
    libraryFoldersName = os.path.join(steamLinuxRoot, "steamapps/libraryfolders.vdf")
    if os.path.isfile(libraryFoldersName):
        with open(libraryFoldersName, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith('"path"'):
                    folder_path = line.split('"')[3].replace("\\\\", "/")
                    libraryFolders.append(os.path.expanduser(folder_path))

    # Search for the game manifest file
    for libraryFolder in libraryFolders:
        manifestFile = os.path.join(libraryFolder, "steamapps", "appmanifest_{}.acf".format(gameId))
        if os.path.isfile(manifestFile):
            return libraryFolder

    return None


print(SELECTED_GAME)
GamePath = getSteamGameLocation()
ENABLED_MODS_PATH = GamePath + SELECTED_GAME["contentPath"] + "/Paks/~mods/"
CSV_PATH = GamePath + SELECTED_GAME["contentPath"] + "/ModData/customize_item_data/mods/"
DISABLED_MODS_PATH = os.path.expanduser("~/.config/TekkenModManager/Disabled/")
TEMP_PATH = "/tmp/"
