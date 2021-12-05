import asyncio
import time

import discord
import requests
from discord.ext import commands

from Utils.classes import Command
from Utils.database import fetch
from Utils.functions import getMatchData, getAgent, getMap


class BasicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='ping',
                      description='Gives the bot latency in milliseconds.',
                      usage='ping',
                      cls=Command,
                      access=0)
    async def ping(self, context):
        client = self.client

        embed = discord.Embed(
            description=f'🏓 Pong! Latency: `{round(client.latency * 1000)}ms`',
            colour=client.config['embed']['colour']
        )
        await context.send(embed=embed)

    @commands.command(name='search',
                      description='Search for player by name/tag',
                      usage='search [name]#[tag]',
                      cls=Command,
                      access=0)
    async def search(self, context, name):
        client = self.client

        thing = name.split("#")

        response = requests.get(f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{thing[0]}/{thing[1]}?api_key={client.bot["riot_token"]}').json()

        embed = discord.Embed(
            description=f'gameName: {response["gameName"]}\ntagLine: {response["tagLine"]}\npuuid: {response["puuid"]}',
            colour=client.config['embed']['colour']
        )
        await context.send(embed=embed)

    @commands.command(name='update',
                      aliases=['u'],
                      description='Update a players match history',
                      usage='update',
                      cls=Command,
                      access=0)
    async def update(self, context):
        client = self.client
        data = fetch(f'SELECT * FROM Users WHERE userId = "{context.author.id}"')

        matchList = requests.get(f'https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{data[0][1]}?api_key={client.bot["riot_token"]}').json()
        databaseResult = fetch(f'SELECT matchId FROM Matches WHERE puuid = "{data[0][1]}"')
        currentCache = [i[0] for i in databaseResult]

        for i in matchList["history"]:
            if i["matchId"] not in currentCache:
                client.addMatchId({"puuid": data[0][1], "matchId": i["matchId"]})

        timeEst = client.getTimeEstimate()
        embed = discord.Embed(
            title='Updating Cached Matches',
            description=f'<a:loading:916645684537589760> Loading data... (Estimate {timeEst}s left)',
            colour=client.config['embed']['colour']
        )
        message = await context.send(embed=embed)

        while timeEst > 0:
            embed.description = f'<a:loading:916645684537589760> Loading data... (Estimate {timeEst}s left)'
            await message.edit(embed=embed)
            await asyncio.sleep(5)
            timeEst -= 5

        embed.description = f'✅ Data Loaded'
        await message.edit(embed=embed)

    @commands.command(name='matchhistory',
                      aliases=['mh'],
                      description='Search for player by name/tag',
                      usage='search [name]#[tag]',
                      cls=Command,
                      access=0)
    async def matchhistory(self, context, user: discord.Member = None):
        if not user:
            user = context.author
        client = self.client

        embed = discord.Embed(
            title='Match History',
            description="<a:loading:916645684537589760> Loading data...",
            colour=client.config['embed']['colour']
        )
        message = await context.send(embed=embed)

        user = client.cache.getUser(user.id)
        if user:
            matchList = requests.get(f'https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{user["puuid"]}?api_key={client.bot["riot_token"]}').json()

            string = ''
            for i in range(0, 20):
                matchId = matchList["history"][i]["matchId"]
                match = requests.get(f'https://eu.api.riotgames.com/val/match/v1/matches/{matchId}?api_key={client.bot["riot_token"]}').json()
                data = getMatchData(client, match, user["puuid"])
                emoji = "🟢" if data["winLoss"] == "win" else "🔴"
                string += f"{emoji} {getAgent(client, data['agent'])} - {getMap(client, data['map'])}\n"

            embed.description = string
            await message.edit(embed=embed)

        else:
            embed = discord.Embed(
                description='User is not linked.',
                colour=client.config['embed']['colour']
            )
            await message.edit(embed=embed)


def setup(client):
    client.add_cog(BasicCommands(client))
