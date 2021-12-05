def getAgent(client, agentId):
    content = client.content

    for character in content["characters"]:
        if character["id"] == agentId.upper():
            return character["name"]


def getMap(client, mapId):
    content = client.content

    for i in content["maps"]:
        if "assetPath" in i:
            if i["assetPath"] == mapId:
                return i["name"]


def getMatchData(client, data, puuid):
    output = {"map": data["matchInfo"]["mapId"]}

    for player in data["players"]:
        if player["puuid"] == puuid:
            output["teamId"] = player["teamId"]
            output["agent"] = player["characterId"]
            break

    for team in data["teams"]:
        if team["teamId"] == output["teamId"]:
            output["winLoss"] = "win" if team["won"] else "loss"
            break
    output["score"] = f'{data["teams"][0]["numPoints"]}-{data["teams"][1]["numPoints"]}'
    return output


