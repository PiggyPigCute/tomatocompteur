import csv
import sys

import discord

import config

OUTPUT_FILE = "dates.csv"

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    guild = client.get_guild(config.GUILD_ID)
    channel = guild.get_channel(config.CHANNEL_ID) if guild else None

    if channel is None:
        print("Salon introuvable, vérifie GUILD_ID et CHANNEL_ID dans config.py")
        await client.close()
        sys.exit(1)

    dates = []
    async for message in channel.history(limit=None, oldest_first=True):
        if message.author.bot:
            dates.append(message.created_at.isoformat())

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date"])
        writer.writerows([[date] for date in dates])

    print(f"{len(dates)} messages de bots trouvés, dates exportées dans {OUTPUT_FILE}")
    await client.close()


client.run(config.TOKEN)
