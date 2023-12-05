import os


def get_steam_game_location():
    steam_root = os.path.expanduser("~/.steam/steam")
    library_folders = [steam_root]
    game_id = 389730
    # Check if the Steam library folders file exists
    library_folders_file = os.path.join(steam_root, "steamapps/libraryfolders.vdf")
    if os.path.isfile(library_folders_file):
        with open(library_folders_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith('"path"'):
                    folder_path = line.split('"')[3].replace("\\\\", "/")
                    library_folders.append(os.path.expanduser(folder_path))

    # Search for the game manifest file
    for library_folder in library_folders:
        manifest_file = os.path.join(library_folder, "steamapps", "appmanifest_{}.acf".format(game_id))
        if os.path.isfile(manifest_file):
            return library_folder

    return None


GamePath = get_steam_game_location()
ENABLED_MODS_PATH = GamePath + "/steamapps/common/TEKKEN 7/TekkenGame/Content/Paks/~mods/"
CSV_PATH = GamePath + "/steamapps/common/TEKKEN 7/TekkenGame/Content/ModData/customize_item_data/mods/"
DISABLED_MODS_PATH= os.path.expanduser("~/.config/TekkenModManager/Disabled/")