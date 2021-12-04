import discord
import requests
from discord.ext import commands

from Utils.classes import Command


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


def setup(client):
    client.add_cog(BasicCommands(client))
