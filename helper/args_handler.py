import argparse

parser = argparse.ArgumentParser(
    prog='Niepper\'s Iron Fist Manager',
    description='Mod Manager for Tekken 7/Tekken 8',
    epilog='It is what it is')

parser.add_argument('modPath', nargs='*', type=str, help='path to a mod you want to add')
