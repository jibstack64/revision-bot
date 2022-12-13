# import required libraries
from util import smod, db, embed, log, card
from discord.ext import commands, tasks
import discord
import asyncio
import atexit
import string
import random
import re
import os

# static vars
AUTH_TOKEN = open("token.txt", "r").read()
MIN_PREFIX, MAX_PREFIX = 2, 8
DATABASE_PATH = "database.json"
DEFAULT_PREFIX = "$"
DEBUG = True

# initialise database
db.initialise(DATABASE_PATH)

# on exit, save database
atexit.register(lambda : db.write(DATABASE_PATH))

# initialise bot
bot = commands.Bot(lambda bot, ctx : 
    (db.fetch(db.database, "guild", ctx.guild.id if ctx.guild != None else ctx.author.id).get("prefix")
    if db.fetch(db.database, "guild", ctx.guild.id if ctx.guild != None else ctx.author.id) != None else DEFAULT_PREFIX),
    intents=discord.Intents.all(), help_command=None)

# LOOPED EVENTS

async def remind_loop():
    while True:
        for dp in db.database:
            for u in dp["remind"]:
                user = await bot.fetch_user(u)
                if len(dp["cards"]) < 1:
                    break
                car = dp["cards"][0]
                dp["cards"].pop(0)
                dp["cards"].append(car)
                path = card.generate(car["question"], car["answer"], car["identifier"])
                file = discord.File(path, filename="card.png")
                await user.send(file=file)
                os.remove(path)
        await asyncio.sleep((60^2)*24)

# EVENT HANDLERS

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    log.warning(f"Error in command '{ctx.command.name}' (called by '{smod.full_username(ctx.author)}'):\n"
        + str(error.with_traceback(None)))
    
@bot.event
async def on_ready():
    log.success("Bot connected and ready.")
    bot.loop.create_task(remind_loop())

@bot.before_invoke
async def ensure_datastore(ctx: commands.Context):
    if ctx.guild == None:
        ctx.guild = ctx.author
    log.success(f"[{ctx.guild.id}] '{smod.full_username(ctx.author)}' ran '{ctx.command.name}'.")
    if not db.exists(db.database, "guild", ctx.guild.id):
        db.generate_guild(ctx.guild.id, DEFAULT_PREFIX)

# COMMANDS

@bot.command("prefix")
async def prefix(ctx: commands.Context, prefix: str):
    guild = db.fetch(db.database, "guild", ctx.guild.id)
    if len(prefix) > MAX_PREFIX or len(prefix) < MIN_PREFIX:
        return await ctx.reply(embed=embed.error("Error!", f"Your prefix must be at least {MIN_PREFIX} characters long, and at most {MAX_PREFIX}."))
    if guild["prefix"] == prefix:
        return await ctx.reply(embed=embed.error("Error!", f"The prefix is already `{prefix}`."))
    else:
        guild["prefix"] = prefix
        return await ctx.reply(embed=embed.success("Success!", f"The prefix has been changed to `{prefix}`."))

@bot.command("help")
async def help_(ctx: commands.Context):
    print(ctx.author.name)

@bot.command("add")
async def card_add(ctx: commands.Context, *, content: str):
    split = smod.split_strings(content)
    print(split)
    if len(split) < 2:
        return await ctx.reply(embed=embed.error(ctx, "Error!", "Missing required arguments. Consult the `help` command."))
    elif len(split) > 2:
        return await ctx.reply(embed=embed.error(ctx, "Error!", "Too many arguments. Consult the `help` command."))
    question, answer = tuple(smod.split_strings(content))
    # regex - no need for intensive checking

    # fetch data and add card
    while True:
        # practically impossible, but remember the engineers rule: if it can, it will!
        card_id = smod.random_string()
        exists = db.exists(db.fetch(db.database, "guild", ctx.guild.id)["cards"], "identifier", card_id)
        if exists:
            continue
        else:
            break

    # add card
    db.generate_card(ctx.guild.id, card_id, question, answer, "")

    # success!!!
    em = embed.success(ctx, f"Success!",
        f"Your revision card has been added to the database. Its identification code is `{card_id}`.")
    return await ctx.reply(embed=em)

@bot.command("remove")
async def card_remove(ctx: commands.Context, card_id: str):
    guild = db.fetch(db.database, "guild", ctx.guild.id)
    card = db.fetch(guild["cards"], "identifier", card_id)
    if card == None:
        return await ctx.reply(embed=embed.error(ctx, "Error!", f"Card of id `{card_id}` does not exist."))
    else:
        db.remove(guild["cards"], "identifier", card_id)
        return await ctx.reply(embed=embed.success(ctx, "Success!", f"Card of id `{card_id}` has been removed."))

@bot.command("list")
async def card_list(ctx: commands.Context, page: int = 1):
    cards = db.fetch(db.database, "guild", ctx.guild.id)["cards"]
    if len(cards) == 0:
        return await ctx.reply(embed=embed.error(ctx, "Empty!", "No revision cards have been added."))
    else:
        pages: list[list[dict]] = []
        p = 0
        c = 0
        for card in cards:
            try:
                pages[p]
            except IndexError:
                pages.append([])
            pages[p].append(card)
            if c == 10:
                p += 1
                c = 1
                continue
            c += 1

        if page > len(pages):
            return await ctx.reply(embed=embed.error(ctx, "Error!", f"Page {page} does not exist."))
        em = embed.success(ctx, f"Cards [Page {page}/{len(pages)}]:")
        for c in pages[page-1]:
            em.add_field(name="[`"+c["identifier"]+"`] "+c["question"], value="||"+c["answer"]+"||", inline=True)
        return await ctx.reply(embed=em)
    
@bot.command("remind")
async def remind(ctx: commands.Context):
    guild = db.fetch(db.database, "guild", ctx.guild.id)
    if ctx.author.id in guild["remind"]:
        guild["remind"].pop(ctx.author.id)
        return await ctx.reply(embed=embed.success(ctx, "Success!", "The reminder has been activated. You will be given revision cards to answer daily."))
    else:
        guild["remind"].append(ctx.author.id)
        return await ctx.reply(embed=embed.success(ctx, "Success!", "You will now **not** be given revision cards daily."))

@bot.command("remind-status")
async def remind_status(ctx: commands.Context):
    guild = db.fetch(db.database, "guild", ctx.guild.id)
    if ctx.author.id in guild["remind"]:
        return await ctx.reply(embed=embed.success(ctx, "Active!", "You are currently given revision cards daily."))
    else:
        return await ctx.reply(embed=embed.success(ctx, "Unactive!", "You are *not* being given revision cards daily."))

# finally, run bot
if __name__ == "__main__":
    bot.run(AUTH_TOKEN) if DEBUG else bot.run(AUTH_TOKEN, log_handler=None)
