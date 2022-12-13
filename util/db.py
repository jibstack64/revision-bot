"Functions for writing to and from the database."

# import required libraries
import json

database: list[dict] = []

def initialise(path: str) -> None:
    globals()["database"] = read(path)

def generate_card(guild_id: str, card_id: str, question: str, answer: str, image: str) -> None:
    "Inserts a dictionary containing a card's data into a guild in the database."

    guild = fetch(database, "guild", guild_id)
    guild["cards"].append({
        "identifier": card_id,
        "question": question,
        "answer": answer,
        "image": image
    })

def generate_guild(guild_id: str, prefix: str) -> None:
    "Inserts a dictionary containing a guild's data into the database."

    container = {
        "guild": guild_id,
        "prefix": prefix,
        "remind": [],
        "remind-frequency": 86400,
        "cards": []
    }
    append(container)

def replace(parent: list[dict], key: str, value: str, obj: object) -> bool:
    "Traverses 'parent' for an element that has 'key' equal to 'value', and replace it with 'obj'. Returns True if success."

    for x in range(parent):
        if parent[x][key] == value:
            parent[x] = obj
            return True
    return False

def remove(obj: list[dict], key: str, value: str) -> bool:
    "Traverses 'obj' and removes the object where 'key' == 'value'."

    for x in range(obj):
        if obj[x][key] == value:
            obj.pop(x)
            return True
    return False

def exists(obj: list[dict] | dict, key: str, value: str) -> bool:
    "Traverses obj. If a list, traverses child dictionaries for key == value. Otherwise, traverse obj for key == value."

    if isinstance(obj, list):
        for x in obj:
            if x[key] == value:
                return True
        return False
    else:
        for k, v in obj.items():
            if obj[k] == v:
                return True
        return False

def write(path: str) -> None:
    "Writes the database to 'path' as JSON."

    json.dump(database, open(path, "w"), indent=4)

def read(path: str) -> list[dict]:
    "Reads the JSON from 'path' to the database variable."

    return json.load(open(path, "r"))

def append(obj: object) -> None:
    "Appends 'obj' to the database."

    database.append(obj)

def fetch(obj: list[dict], key: str, value: str) -> dict[str, object] | None:
    "Fetches the object in 'obj' thats 'key' == 'value'."

    for x in obj:
        if x[key] == value:
            return x
    return None
