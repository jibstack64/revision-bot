"Functions for logging events."

# import required libraries
from colorama import Fore as Colour
import datetime
import colorama
import os

# win support
if os.name == "nt":
    colorama.init(convert=True)

log: list[str] = []

def paint(text: str, colour: str | list[str]) -> str:
    "Paints 'text' with 'colour', adding termination codes automatically."

    log.append(text)
    return ("".join(colour) if isinstance(colour, list) else colour) + text + Colour.RESET

def fatal(text: str, code: int = 1) -> None:
    "Prints 'text' as red and exits the program."

    log.append(text)
    print(paint(text, Colour.LIGHTRED_EX))
    exit(code)

def success(text: str) -> None:
    "Prints 'text' as green."

    log.append(text)
    print(paint(text, Colour.LIGHTGREEN_EX))

def warning(text: str) -> None:
    "Prints 'text' as yellow."

    log.append(text)
    print(paint(text, Colour.YELLOW))

def write_log() -> None:
    "Writes the log to a logfile."

    with open(f"logs/log-{datetime.datetime.now().strftime('%H-%M-%S')}.txt", "w") as f:
        f.write("\n".join(log))
        f.close()
