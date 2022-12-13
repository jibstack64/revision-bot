"Contains a couple of useful utility functions."

# import required libraries
import discord
import random
import string
import re

def split_strings(string: str) -> list[str]:
    "Splits the provided string by elements surrounded by '\"'."
    
    return re.findall("\"(.*?)\"", string)

def random_string(length: int = 5) -> str:
    "Generates a random string of 'length' size."

    return "".join([random.choice(string.ascii_letters) for x in range(length)])

def full_username(author: discord.Member | discord.User):
    return author.name + "#" + author.discriminator
    