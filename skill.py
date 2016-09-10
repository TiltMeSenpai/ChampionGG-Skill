from .. import Skill
from tabulate import tabulate
import requests
import os
import asyncio

class RoleSkill(Skill):
    async def parse(self, message, lane, best="best", number=5, question=None):
        if lane == "bot": lane = "adc"
        if lane == "mid": lane = "middle"
        if best in ["best", "top"]:
            url = "http://api.champion.gg/stats/role/{}/bestPerformance?api_key={}&page=1&limit={}".format(
                lane, os.environ["CHAMPION_GG_KEY"], number)
        else:
            url = "http://api.champion.gg/stats/role/{}/worstPerformance?api_key={}&page=1&limit={}".format(
                    lane, os.environ["CHAMPION_GG_KEY"], number)
        champs = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
        champs = champs.json()
        data = [["#", "Name", "Win Percent", "Play Percent", "Ban Rate"]]
        for i, champ in enumerate(champs["data"]):
            data.append([i+1, champ["name"], champ["general"]["winPercent"],
                champ["general"]["playPercent"], champ["general"]["banRate"]])
        return "According to Champion.gg:\n```"+tabulate(data, headers="firstrow")+"```"

class ChampSkill(Skill):
    async def on_load(self):
        url = "http://api.champion.gg/champion?api_key={}".format(os.environ["CHAMPION_GG_KEY"])
        champs = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
        champs = champs.json()
        self.champs={}
        for champ in champs:
            self.engine.register_entity(champ["name"], "champion", "league")
            self.champs[champ["name"]] = champ["key"]
        print(self.champs)

    async def parse(self, message):
        pass
