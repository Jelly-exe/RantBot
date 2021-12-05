import asyncio
import inspect
import time

import discord
import requests
from discord.ext import commands

from Utils.classes import Command, Group
from Utils.database import insert, fetch


class BasicAdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.group(name='say',
                    invoke_without_command=True,
                    usage='say [text/embed]',
                    description='Make the bot say something.',
                    cls=Group,
                    access='botAdmin')
    async def say(self, context):
        raise commands.MissingRequiredArgument(inspect.Parameter('UsageError', inspect.Parameter.POSITIONAL_ONLY))

    @commands.is_owner()
    @say.command(name='text',
                 description='Make the bot say something in message format.',
                 usage='say text [text]',
                 access='botAdmin',
                 cls=Command)
    async def text_say(self, context, *, content):
        time.sleep(0.05)
        await context.message.delete()
        await context.send(content)

    @commands.is_owner()
    @say.command(name='embed',
                 description='Make the bot say something in message format.',
                 usage='say embed [embed title;embed content]',
                 access='botAdmin',
                 cls=Command)
    async def embed_say(self, context, *, content):
        client = self.client
        content = content.split(';')

        if len(content) != 2:
            raise commands.MissingRequiredArgument(inspect.Parameter('UsageError', inspect.Parameter.POSITIONAL_ONLY))

        embed = discord.Embed(
            title=content[0],
            description=content[1],
            colour=client.config['embed']['colour']
        )
        embed.set_footer(text=client.config['embed']['footer']['text'], icon_url=client.config['embed']['footer']['url'])

        time.sleep(0.05)
        await context.message.delete()
        await context.send(embed=embed)

    @commands.is_owner()
    @commands.command(name='react',
                      description='React to a message with a reaction (Must run in channel)',
                      usage='react [message id] [reaction]',
                      access='botAdmin',
                      cls=Command)
    async def react(self, context, messageId, reaction):
        time.sleep(0.05)
        await context.message.delete()

        message = await context.message.channel.fetch_message(messageId)
        await message.add_reaction(reaction)

    @commands.is_owner()
    @commands.command(name='link',
                      description='Manually link a user with a valorant account',
                      usage='link [user] [name]#[tag]',
                      access='botAdmin',
                      cls=Command)
    async def link(self, context, user: discord.Member, name):
        client = self.client

        thing = name.split("#")

        response = requests.get(f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{thing[0]}/{thing[1]}?api_key={client.bot["riot_token"]}').json()
        insert("INSERT INTO Users(userId, puuid, gameName, tagLine) VALUES(?, ?, ?, ?)", (user.id, response["puuid"], response["gameName"], response["tagLine"]))

        matchList = requests.get(f'https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{response["puuid"]}?api_key={client.bot["riot_token"]}').json()
        databaseResult = fetch(f'SELECT matchId FROM Matches WHERE puuid = "{response["puuid"]}"')
        currentCache = [i[0] for i in databaseResult]

        for i in matchList["history"]:
            if i["matchId"] not in currentCache:
                client.addMatchId({"puuid": response["puuid"], "matchId": i["matchId"]})

        timeEst = client.getTimeEstimate()
        embed = discord.Embed(
            title='Linking User',
            description=f'{user.mention} has been linked with `{name}`.\n\n<a:loading:916645684537589760> Loading data... (Estimate {timeEst}s left)',
            colour=client.config['embed']['colour']
        )
        message = await context.send(embed=embed)

        while timeEst > 0:
            embed.description = f'{user.mention} has been linked with `{name}`.\n\n<a:loading:916645684537589760> Loading data... (Estimate {timeEst}s left)'
            await message.edit(embed=embed)
            await asyncio.sleep(5)
            timeEst -= 5

        embed.description = f'{user.mention} has been linked with `{name}`.\n\n✅ Data Loaded'
        await message.edit(embed=embed)


def setup(client):
    client.add_cog(BasicAdminCommands(client))
