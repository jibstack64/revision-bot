"Functions for generating pretty-looking embeds."

# import required libraries
from discord.ext.commands import Context
from discord import Colour
from discord import Embed
from . import smod

def credit(ctx: Context) -> Embed:
    "Forms an embed containing credits to 'ctx.author'."

    embed = Embed()
    embed.set_footer(text=f"Requested by {smod.full_username(ctx.author)}.", icon_url=ctx.author.avatar.url)
    return embed

def success(ctx: Context, title: str, description: str = "") -> Embed:
    "Creates and returns a success embed with the title and description provided."

    embed = credit(ctx)
    embed.title = title
    embed.description = description
    embed.colour = Colour.brand_green()
    return embed

def error(ctx: Context, title: str, description: str = "") -> Embed:
    "Creates and returns an error embed with the title and description provided."

    embed = credit(ctx)
    embed.title = title
    embed.description = description
    embed.colour = Colour.brand_red()
    return embed
