import os
import re
from pathlib import Path
from time import sleep
from rich.table import Table
from rich import print
from rich.console import Console
import json as js

from helper.dir_handler import understandOption
from helper.steam import SELECTEDGAME


def getOptions():
    jsonPath = Path("./helper/options.json")
    with open(jsonPath) as file:
        return js.load(file)


def wrongAnswer():
    print("Given Incorrect value. Try again")
    sleep(2)
    os.system("clear")


def init():
    console = Console()
    os.system("clear")
    while True:
        options = getOptions()
        for i in options:
            console.print(f'[bold yellow]{i["id"]}.[/bold yellow][bold] {i["name"]} [/bold]')

        console.print(f'[bold]Which one do you want to select [1-{len(options)}][/bold]:', end="")

        a = input(" ")
        try:
            if int(a) not in range(1, len(options) + 1):
                wrongAnswer()
            else:
                return options[int(a) - 1]["function"]
        except ValueError:
            wrongAnswer()


def generateModTable(file: list, do_input=False, name="Active Mods"):
    table = Table(title=f'{SELECTEDGAME["name"]} {name}', row_styles=["", "dim"])
    table.add_column("Id", justify="center", no_wrap=True)
    table.add_column("Name", justify="left")
    table.add_column("Path", justify="right")

    for filer in file:
        table.add_row(str(filer.id + 1) + ".", filer.name, filer.path)

    print(table)

    if do_input:
        print(
            f"[bold yellow] Which one you want to select [1-{len(table.rows)}][/bold yellow] [bold](eg. 1-5; 1,2,3,4,5; !4): [/bold]",
            end="")
        a = input("")
        return a


def successMessage(options, modlist, message):
    options = understandOption(options)
    effectedMods = []
    for i in options:
        effectedMods.append(modlist[i - 1].name)

    modified_extensions = ', '.join([re.sub(r'\.\w+\b', '', ext) for ext in effectedMods])

    print(f"[bold green]Successfully {message} {modified_extensions}[/bold green]")
    sleep(2)


def failMessage(message):
    print(f"[bold red]{message}[/bold red]")
    sleep(2)
