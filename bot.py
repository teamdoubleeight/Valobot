from __future__ import annotations
import requests
import asyncio, os, sys, traceback, aiohttp, discord, json
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, ExtensionNotFound, NoEntryPointError
from dotenv import load_dotenv
from utils import locale_v2
from discord import SyncWebhook
from utils.valorant.cache import get_cache
load_dotenv()
from cogs.sendwebhook import *


initial_extensions = ['cogs.admin', 'cogs.errors', 'cogs.notify', 'cogs.valorant', 'cogs.verify']

# intents required
intents = discord.Intents.default()
intents.message_content = True

vv = "1.7.1"
    
BOT_PREFIX = '/'

r = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul")
r = r.json()
date = r['dateTime'].split("T") #2023-05-21T08:43:15.4414864
time = date[1].split(".")[0]
dt = date[0] + " | " +  time

with open('buildinfo.json', 'r') as f:
    json_data = json.load(f)

ghlt = str(json_data['number'] + 1)

print("빌드 버전 : " + json_data['version'])
print("버전의 빌드 횟수 : " + ghlt)
print("빌드 일시 : " + dt)
json_data['version']  = vv
json_data['number'] = json_data['number'] + 1
json_data['datetime'] = dt


class ValorantBot(commands.AutoShardedBot):
    debug: bool
    bot_app_info: discord.AppInfo

    def __init__(self) -> None:
        super().__init__(command_prefix=BOT_PREFIX, case_insensitive=True, intents=intents)
        self.session: aiohttp.ClientSession = None
        self.bot_version = '1.7.1'
        self.tree.interaction_check = self.interaction_check

    @staticmethod
    async def interaction_check(interaction: discord.Interaction) -> bool:
        locale_v2.set_interaction_locale(interaction.locale)  # bot responses localized # wait for update
        locale_v2.set_valorant_locale(interaction.locale)  # valorant localized
        return True

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner
        
    async def on_ready(self) -> None:

        await self.tree.sync()
        username = str(self.user)
        print(f"들어간 사용자 : {username}")

        activity_type = discord.ActivityType.listening
        await self.change_presence(activity=discord.Activity(type=activity_type, name=f"{str(len(self.guilds))} 서버들에서 /도움말 듣는 중"))
        
        

    async def setup_hook(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        try:
            self.owner_id = int(os.getenv('OWNER_ID'))
        except ValueError:
            self.bot_app_info = await self.application_info()
            self.owner_id = self.bot_app_info.owner.id

        self.setup_cache()
        await self.load_cogs()
        # await self.tree.sync()

    async def load_cogs(self) -> None:
        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
            except (
                ExtensionNotFound,
                NoEntryPointError,
                ExtensionFailed,
            ):
                print(f'Failed to load extension {ext}.', file=sys.stderr)
                traceback.print_exc()
                
    

    @staticmethod
    def setup_cache() -> None:
        try:
            open('data/cache.json')
        except FileNotFoundError:
            get_cache()

    async def close(self) -> None:
        await self.session.close()
        await super().close()

    async def start(self, debug: bool = False) -> None:
        self.debug = debug
        return await super().start(os.getenv('TOKEN'), reconnect=True)


def run_bot() -> None:
    bot = ValorantBot()
    asyncio.run(bot.start())

with open('buildinfo.json', 'w', encoding='utf-8') as make_file:
    json.dump(json_data, make_file, indent="\t")
    
buildhook(vv=vv, ghlt=ghlt, dt=dt)

if __name__ == '__main__':
    run_bot()
    
    
