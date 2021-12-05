import requests
from discord.ext import tasks, commands

from Utils.database import insert
from Utils.functions import getMatchData, getAgent, getMap


class CacheMatches(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sendToDB.start()

    @tasks.loop(seconds=1.5)
    async def sendToDB(self):
        client = self.client

        matchData = client.getMatchId()
        if matchData:
            match = requests.get(f'https://eu.api.riotgames.com/val/match/v1/matches/{matchData["matchId"]}?api_key={client.bot["riot_token"]}').json()
            data = getMatchData(client, match, matchData["puuid"])

            insert("INSERT INTO Matches(matchId, puuid, agent, map, winLoss, score) VALUES(?, ?, ?, ?, ?, ?)", (matchData["matchId"], matchData["puuid"], getAgent(client, data['agent']), getMap(client, data['map']), data['winLoss'], data['score']))

    @sendToDB.before_loop
    async def before_sendToDB(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(CacheMatches(client))
