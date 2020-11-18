import discord
import json
import random
import asyncio
import os
from discord.ext import commands

# seconds the bot wait until someone is chosen
TIMEOUT = 15

with open('./challenges.json') as challenges:
  data = json.load(challenges)

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Ready!")

@client.command()
async def challenge(ctx):
    randomChallenge = random.choice(data)
    embed = discord.Embed(title = randomChallenge.get("title"), description = randomChallenge.get("challenge"), color = discord.Colour.green())
    embed.add_field(name="Tip:", value = "React within " + str(TIMEOUT) + " seconds to participate in challenge", inline = False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    await asyncio.sleep(TIMEOUT)
    msg = await msg.channel.fetch_message(msg.id)
    users = set()
    for reaction in msg.reactions:
        async for user in reaction.users():
            if user.name != 'PUBG challenges':
                users.add(user.name)
    if len(users) >= 1:
        default_message = " will pay for the season passes ;)"
        loser_in_bold = "**"+random.choice(tuple(users))+"**"
        response = loser_in_bold + default_message
        await ctx.send(response)


token = os.environ.get('pubgchallengestoken')
client.run(token)
