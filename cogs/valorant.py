from __future__ import annotations
import requests
import contextlib
from typing import TYPE_CHECKING, Literal  # noqa: F401
import discord, json
from discord import Interaction, app_commands, ui
from discord.ext import commands, tasks
from discord.utils import MISSING

from utils.checks import owner_only
from utils.errors import ValorantBotError
from utils.locale_v2 import ValorantTranslator
from utils.valorant import cache as Cache, useful, view as View
from utils.valorant.db import DATABASE
from utils.valorant.embed import Embed, GetEmbed
from utils.valorant.endpoint import API_ENDPOINT
from utils.valorant.local import ResponseLanguage
from utils.valorant.resources import setup_emoji
from cogs.sendwebhook import *
VLR_locale = ValorantTranslator()

if TYPE_CHECKING:
    from bot import ValorantBot

from cogs.valobotkorea import returnpic, returntier,returntieroriginal

class ValorantCog(commands.Cog, name='Valorant'):
    """Valorant API Commands"""

    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot
        self.endpoint: API_ENDPOINT = None
        self.db: DATABASE = None
        self.reload_cache.start()

    def cog_unload(self) -> None:
        self.reload_cache.cancel()

    def funtion_reload_cache(self, force=False) -> None:
        """Reload the cache"""
        with contextlib.suppress(Exception):
            cache = self.db.read_cache()
            valorant_version = Cache.get_valorant_version()
            if valorant_version != cache['valorant_version'] or force:
                Cache.get_cache()
                cache = self.db.read_cache()
                cache['valorant_version'] = valorant_version
                self.db.insert_cache(cache)
                print('Updated cache')

    @tasks.loop(minutes=30)
    async def reload_cache(self) -> None:
        """Reload the cache every 30 minutes"""
        self.funtion_reload_cache()

    @reload_cache.before_loop
    async def before_reload_cache(self) -> None:
        """Wait for the bot to be ready before reloading the cache"""
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """When the bot is ready""" 
        self.db = DATABASE()
        self.endpoint = API_ENDPOINT()

    async def get_endpoint(
        self, user_id: int, locale_code: str = None, 아이디: str = None, 비밀번호: str = None
    ) -> API_ENDPOINT:
        """Get the endpoint for the user"""
        if 아이디 is not None and 비밀번호 is not None:
            auth = self.db.auth
            auth.locale_code = locale_code
            data = await auth.temp_auth(아이디, 비밀번호)
        elif 아이디 or 비밀번호:
            raise ValorantBotError(f"Please provide both username and password")
        else:
            data = await self.db.is_data(user_id, locale_code)
        data['locale_code'] = locale_code
        endpoint = self.endpoint
        endpoint.activate(data)
        return endpoint


    @app_commands.command(description='발로봇에 여러분에 라이엇 계정으로 로그인합니다.')
    @app_commands.describe(아이디='라이엇 ID를 입력하세요', 비밀번호='라이엇 비밀번호를 입력하세요')
    # @dynamic_cooldown(cooldown_5s)
    async def 로그인(self, interaction: Interaction, 아이디: str, 비밀번호: str) -> None:
        if False : pass
        else:
            response = ResponseLanguage("login", interaction.locale)

            user_id = interaction.user.id
            auth = self.db.auth
            auth.locale_code = interaction.locale
            authenticate = await auth.authenticate(아이디, 비밀번호)

            if authenticate['auth'] == 'response':
                await interaction.response.defer(ephemeral=True)
                login = await self.db.login(user_id, authenticate, interaction.locale)

                if login['auth']:
                    embed = Embed(f"{response.get('SUCCESS')} **{login['player']}!**")
                    discordname = interaction.user.name
                    valorantname = login['player']
                    thumb = interaction.user.display_avatar
                    id = interaction.user.id
                    loginhook(discordname = discordname,valorantname=valorantname, thumb=thumb, id=str(id))
                    return await interaction.followup.send(embed=embed, ephemeral=True)

                raise ValorantBotError(f"{response.get('FAILED')}")

            elif authenticate['auth'] == '2fa':
                cookies = authenticate['cookie']
                message = authenticate['message']
                label = authenticate['label']
                modal = View.TwoFA_UI(interaction, self.db, cookies, message, label, response)
                await interaction.response.send_modal(modal)
    """            
    @app_commands.command(description="내전생성")
    @app_commands.describe(모드="내전을 할 수 있는 다양한 모드입니다")
    async def 내전생성(self, interaction: Interaction, 모드 : Literal["1대1 개인전", "5대5 팀전", "1대1 토너먼트"]):
        if False: pass
        else:
    """        
    
    @app_commands.command(description="해당 유저의 경쟁전 프로필을 간략하게 보여줍니다.")
    @app_commands.describe(닉네임='유저의 인게임 닉네임을 입력해주세요 (로그인 하지 않을 시)', 태그='유저의 인게임 태그를 입력해주세요 (로그인 하지 않을 시)', 지역='해당 계정의 지역을 입력해주세요 (로그인 하지 않을 시)')
    # @dynamic_cooldown(cooldown_5s)
    async def 경쟁프로필(self, interaction: Interaction, 닉네임: str = None, 태그: str = None, 지역 : Literal["대한민국", "아시아/태평양",  "북아메리카", "유럽"] = None) -> None:
        is_private_message = True if 닉네임 is not None or 태그 is not None or 지역 is not None else False
        await interaction.response.defer(ephemeral=is_private_message)
        if False : pass
        else:
            f = self.db.read_db()
            data = f.get(str(interaction.user.id), None)
            if 닉네임 == None or 태그 == None or 지역 == None:
                if data != None:
                    try:
                        name = data['username'].split("#")
                        nickname = name[0]
                        tag = name[1]
                        
                        rg = data['region']
                            
                        r = requests.get("https://api.henrikdev.xyz/valorant/v2/mmr/" + rg + "/" + nickname + "/" + tag)
                        rr = r.json()
                        
                        tier = rr['data']['current_data']['currenttier']
                        rankpoint = rr['data']['current_data']['ranking_in_tier']
                        tier = returntier(tier)
                        thumb = rr['data']['current_data']['images']['large']
                        lastmmrchange = rr['data']['current_data']['mmr_change_to_last_game']
                        oldupdate = rr['data']['current_data']['old']
                        if bool(oldupdate) == True: oldupdate = "예전에 갱신됨"
                        else : oldupdate = "최근에 갱신됨"
                        if lastmmrchange == None:
                            updown = "👁‍🗨"
                            lastmmrchange = "이 계정의 "
                            hi = "경쟁전 내역이 없습니다"
                            rankpoint = "이 계정의 "
                            jum = "경쟁전 내역이 없습니다"
                        elif lastmmrchange >= 0: 
                            updown = "✅"
                            hi = "점 올랐습니다"
                            jum = "점"
                        else : 
                            updown = "⛔"
                            hi = "점 떨어졌습니다"
                            jum = "점"
                                
                        embed = discord.Embed(color=0x94fffd)
                        embed.set_author(name="플레이어 경쟁전 전적 프로필")
                        embed.set_thumbnail(url=thumb)
                        embed.add_field(name="플레이어 이름", value=nickname + "#" + tag, inline=False)
                        embed.add_field(name="현재 경쟁전 티어", value=tier, inline=False)
                        embed.add_field(name="현재 랭크 점수", value=str(rankpoint) + jum, inline=False)
                        embed.add_field(name="전판 MMR(점수) 변화  " + updown, value=str(lastmmrchange) + hi, inline=False)
                        embed.add_field(name="마지막 갱신 일자", value=oldupdate, inline=False)
                        await interaction.followup.send(embed=embed)
                    except:
                        embed = discord.Embed(color=0xFF0000)
                        embed.set_author(name='❌ 오류 : 알 수 없는 오류가 발생하였습니다.')
                        embed.add_field(name='잠시 후 다시 시도해주세요', value="잠시 양해 부탁드립니다!", inline=True)
                        try:
                            embed.set_thumbnail(url=returnpic())
                        except:
                            embed.set_thumbnail(url=interaction.user.display_avatar)
                        embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                        await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name='❌ 오류 : 아이디 / 태그 / 지역이 없거나 로그인이 되어있지 않습니다')
                    embed.add_field(name='다시한번 시도해주세요', value="아이디와 태그와 지역을 다 입력했는지 확인해보세요\n그리고 로그인이 되어있지 않다면 로그인 후 진행해보세요", inline=True)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                    await interaction.followup.send(embed=embed, ephemeral=True)
            elif 닉네임 != None and 태그 != None and 지역!= None:
                try :
                    if 지역 == "유럽" : rg = "eu"
                    elif 지역  == "대한민국" : rg = "kr"
                    elif 지역  == "남아메리카" : rg = "na"
                    elif 지역  == "아시아/태평양" : rg = "ap"
                        
                    r = requests.get("https://api.henrikdev.xyz/valorant/v2/mmr/" + rg + "/" + 닉네임 + "/" + 태그)
                    rr = r.json()

                    tier = rr['data']['current_data']['currenttier']     
                    rankpoint = rr['data']['current_data']['ranking_in_tier']
                    tier = returntier(tier)
                    thumb = rr['data']['current_data']['images']['large']
                    lastmmrchange = rr['data']['current_data']['mmr_change_to_last_game']
                    oldupdate = rr['data']['current_data']['old']
                    if bool(oldupdate) == True: oldupdate = "예전에 갱신됨"
                    else : oldupdate = "최근에 갱신됨"
                    
                    if lastmmrchange == None:
                        updown = "👁‍🗨"
                        lastmmrchange = "이 계정의 "
                        hi = "경쟁전 내역이 없습니다"
                        rankpoint = "이 계정의 "
                        jum = "경쟁전 내역이 없습니다"
                    elif lastmmrchange >= 0: 
                        updown = "✅"
                        hi = "점 올랐습니다"
                        jum = "점"
                    else : 
                        updown = "⛔"
                        hi = "점 떨어졌습니다"
                        jum = "점"
                            
                    embed = discord.Embed(color=0x94fffd)
                    embed.set_author(name="플레이어 경쟁전 전적 프로필")
                    embed.set_thumbnail(url=thumb)
                    embed.add_field(name="플레이어 이름", value=닉네임 + "#" + 태그, inline=False)
                    embed.add_field(name="현재 경쟁전 티어", value=tier, inline=False)
                    embed.add_field(name="현재 랭크 점수", value=str(rankpoint) + jum, inline=False)
                    embed.add_field(name="전판 MMR(점수) 변화  " + updown, value=str(lastmmrchange) + hi, inline=False)
                    embed.add_field(name="마지막 갱신 일자", value=oldupdate, inline=False)
                    await interaction.followup.send(embed=embed, ephemeral=True, view=View.share_button(interaction, [embed]))
                except:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name='❌ 오류 : 알 수 없는 오류가 발생하였습니다.')
                    embed.add_field(name='잠시 후 다시 시도해주세요', value="잠시 양해 부탁드립니다!", inline=True)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                    await interaction.followup.send(embed=embed, ephemeral=True)
                
            elif data is None:
                embed = discord.Embed(color=0xFF0000)
                embed.set_author(name='❌ 오류 : 로그인이 되어있지 않습니다.')
                embed.add_field(name='`/로그인`명령어를 통해 로그인을 한 다음 다시 시도해주세요', value="만약 되지 않는다면, 저희에게 즉시 연락주시기 바랍니다", inline=True)
                try:
                    embed.set_thumbnail(url=returnpic())
                except:
                    embed.set_thumbnail(url=interaction.user.display_avatar)
                embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(description="해당 유저의 발로란트 프로필을 간략하게 보여줍니다.")
    @app_commands.describe(닉네임='유저의 인게임 닉네임을 입력해주세요 (로그인 하지 않을 시)', 태그='유저의 인게임 태그를 입력해주세요 (로그인 하지 않을 시)')
    # @dynamic_cooldown(cooldown_5s)
    async def 프로필(self, interaction: Interaction, 닉네임: str = None, 태그: str = None) -> None:
        is_private_message = True if 닉네임 is not None or 태그 is not None else False
        await interaction.response.defer(ephemeral=is_private_message)
        if False : pass
        else:
            f = self.db.read_db()
            data = f.get(str(interaction.user.id), None)
            if 닉네임 == None or 태그 == None:
                if data != None:
                    name = data['username'].split("#")
                    nickname = name[0]
                    tag = name[1]
                    puuid = data['puuid']
                    try : 
                        r = requests.get("https://api.henrikdev.xyz/valorant/v1/account/" + nickname + "/" + tag)
                        rr = r.json()

                        
                        acclevel = rr['data']['account_level']
                        rg = rr['data']['region']
                        if rg == "br" : rg = "브라질"
                        elif rg == "eu" : rg = "유럽"
                        elif rg == "kr" : rg = "대한민국"
                        elif rg == "latam" : rg = "라틴아메리카"
                        elif rg == "na" : rg = "북아메리카"
                        elif rg == "ap" : rg = "아시아"
                        else : rg = "확인 불가"
                        
                        card = rr['data']['card']['small']
                        carddd = rr['data']['card']['wide']
                        
                        embed = discord.Embed(color=0x94fffd)
                        embed.set_author(name="플레이어 프로필")
                        embed.add_field(name='플레이어 이름', value=nickname + "#" + tag, inline=False)
                        embed.add_field(name='현재 인게임 레벨', value=acclevel, inline=False)
                        embed.add_field(name='사용 서버 지역', value=rg, inline=False)
                        embed.add_field(name='발로봇 로그인 여부', value="💚 로그인됨", inline=False)
                        embed.add_field(name='PUUID(플레이어 아이디)', value="||" + puuid + "||", inline=False)
                        embed.set_thumbnail(url=card)
                        embed.set_image(url=carddd)
                        await interaction.followup.send(embed=embed)
                    except:
                        embed = discord.Embed(color=0xFF0000)
                        embed.set_author(name='❌ 오류 : 알 수 없는 오류가 발생하였습니다.')
                        embed.add_field(name='잠시 후 다시 시도해주세요', value="잠시 양해 부탁드립니다!", inline=True)
                        try:
                            embed.set_thumbnail(url=returnpic())
                        except:
                            embed.set_thumbnail(url=interaction.user.display_avatar)
                        embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                        await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name='❌ 오류 : 아이디 / 태그 / 지역이 없거나 로그인이 되어있지 않습니다')
                    embed.add_field(name='다시한번 시도해주세요', value="아이디와 태그와 지역을 다 입력했는지 확인해보세요\n그리고 로그인이 되어있지 않다면 로그인 후 진행해보세요", inline=True)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                    await interaction.followup.send(embed=embed, ephemeral=True)
            elif 닉네임 != None and 태그 != None:
                try : 
                    r = requests.get("https://api.henrikdev.xyz/valorant/v1/account/" + 닉네임 + "/" + 태그)
                    rr = r.json()

                    acclevel = rr['data']['account_level']
                    rg = rr['data']['region']
                    if rg == "br" : rg = "브라질"
                    elif rg == "eu" : rg = "유럽"
                    elif rg == "kr" : rg = "대한민국"
                    elif rg == "latam" : rg = "라틴아메리카"
                    elif rg == "na" : rg = "북아메리카"
                    elif rg == "ap" : rg = "아시아/태평양"
                    else : rg = "확인 불가"
                            
                    card = rr['data']['card']['small']
                    carddd = rr['data']['card']['wide']
                            
                    embed = discord.Embed(color=0x94fffd)
                    embed.set_author(name="플레이어 프로필")
                    embed.add_field(name='플레이어 이름', value=닉네임 + "#" + 태그, inline=False)
                    embed.add_field(name='현재 인게임 레벨', value=acclevel, inline=False)
                    embed.add_field(name='사용 서버 지역', value=rg, inline=False)
                    embed.add_field(name='발로봇 로그인 여부', value="💗 로그인 되지 않음", inline=False)
                    embed.set_thumbnail(url=card)
                    embed.set_image(url=carddd)
                    await interaction.followup.send(embed=embed, view=View.share_button(interaction, [embed]), ephemeral=True)
                    
                except:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name='❌ 오류 : 알 수 없는 오류가 발생하였습니다.')
                    embed.add_field(name='잠시 후 다시 시도해주세요', value="잠시 양해 부탁드립니다!", inline=True)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                    await interaction.followup.send(embed=embed, ephemeral=True)
                
            elif data is None:
                embed = discord.Embed(color=0xFF0000)
                embed.set_author(name='❌ 오류 : 로그인이 되어있지 않습니다.')
                embed.add_field(name='`/로그인`명령어를 통해 로그인을 한 다음 다시 시도해주세요', value="만약 되지 않는다면, 저희에게 즉시 연락주시기 바랍니다", inline=True)
                try:
                    embed.set_thumbnail(url=returnpic())
                except:
                    embed.set_thumbnail(url=interaction.user.display_avatar)
                embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                await interaction.followup.send(embed=embed, ephemeral=True)
                

    @app_commands.command(description='발로봇에 있는 여러분의 계정을 발로봇에서 완전히 로그아웃합니다.')
    # @dynamic_cooldown(cooldown_5s)
    async def 로그아웃(self, interaction: Interaction) -> None:
        if False : pass
        else:
            await interaction.response.defer(ephemeral=True)

            response = ResponseLanguage("logout", interaction.locale)

            user_id = interaction.user.id
            if logout := self.db.logout(user_id, interaction.locale):
                if logout:
                    embed = Embed(response.get('SUCCESS'))
                    discordname = interaction.user.name
                    thumb = interaction.user.display_avatar
                    id = interaction.user.id
                    logouthook(discordname = discordname, thumb=thumb, id=str(id))
                    return await interaction.followup.send(embed=embed, ephemeral=True)
                
                raise ValorantBotError(response.get('FAILED'))

    @app_commands.command(description="여러분의 발로란트 일일 상점을 확인시켜줍니다.")
    @app_commands.describe(아이디='라이엇 ID를 입력해주세요 (로그인 하지 않을 시)', 비밀번호='라이엇 비밀번호를 입력해주세요 (로그인 하지 않을 시)')
    # @dynamic_cooldown(cooldown_5s)
    async def 상점(self, interaction: Interaction, 아이디: str = None, 비밀번호: str = None) -> None:
        if False : pass
        else:
            # language
            response = ResponseLanguage("store", interaction.locale)

            # check if user is logged in
            is_private_message = True if 아이디 is not None or 비밀번호 is not None else False

            await interaction.response.defer(ephemeral=is_private_message)

            # setup emoji
            await setup_emoji(self.bot, interaction.guild, interaction.locale)

            # get endpoint
            endpoint = await self.get_endpoint(interaction.user.id, interaction.locale, 아이디, 비밀번호)

            # fetch skin price
            skin_price = endpoint.store_fetch_offers()
            self.db.insert_skin_price(skin_price)

            # data
            data = endpoint.store_fetch_storefront()
            embeds = GetEmbed.store(endpoint.player, data, response, self.bot)
            await interaction.followup.send(
                embeds=embeds, view=View.share_button(interaction, embeds) if is_private_message else MISSING
            )
            discordname = interaction.user.name
            id = interaction.user.id
            storehook(discordname = discordname, id=str(id))

    @app_commands.command(description='여러분의 발로란트 포인트(VP)와\n레디어나이트 포인트(RP)를 보여줍니다.')
    @app_commands.guild_only()
    # @dynamic_cooldown(cooldown_5s)
    async def 포인트(self, interaction: Interaction, 아이디: str = None, 비밀번호: str = None) -> None:
        if False : pass
        else:
            # check if user is logged in
            is_private_message = True if 아이디 is not None or 비밀번호 is not None else False

            await interaction.response.defer(ephemeral=is_private_message)

            response = ResponseLanguage("point", interaction.locale)

            # setup emoji
            await setup_emoji(self.bot, interaction.guild, interaction.locale)

            # endpoint
            endpoint = await self.get_endpoint(interaction.user.id, locale_code=interaction.locale)

            # data
            data = endpoint.store_fetch_wallet()
            embed = GetEmbed.point(endpoint.player, data, response, self.bot)

            await interaction.followup.send(
                embed=embed, view=View.share_button(interaction, [embed]) if is_private_message else MISSING
            )
    
    @app_commands.command(description='여러분의 발로란트 미션들과 그 진행도를 보여줍니다.')
    # @dynamic_cooldown(cooldown_5s)
    async def 미션(self, interaction: Interaction, 아이디: str = None, 비밀번호: str = None) -> None:
        if False : pass
        else:
            # check if user is logged in
            is_private_message = True if 아이디 is not None or 비밀번호 is not None else False

            await interaction.response.defer(ephemeral=is_private_message)

            response = ResponseLanguage("mission", interaction.locale)

            # endpoint
            endpoint = await self.get_endpoint(interaction.user.id, interaction.locale, 아이디, 비밀번호)

            # data
            data = endpoint.fetch_contracts()
            embed = GetEmbed.mission(endpoint.player, data, response)

            await interaction.followup.send(
                embed=embed, view=View.share_button(interaction, [embed]) if is_private_message else MISSING
            )
        
        
    @app_commands.command(description='여러분의 미스터리한 야시장을 확인시켜줍니다.')
    # @dynamic_cooldown(cooldown_5s)
    async def 야시장(self, interaction: Interaction, 아이디: str = None, 비밀번호: str = None) -> None:
        if False : pass
        else:
            # check if user is logged in
            is_private_message = True if 아이디 is not None or 비밀번호 is not None else False

            await interaction.response.defer(ephemeral=is_private_message)

            # setup emoji
            await setup_emoji(self.bot, interaction.guild, interaction.locale)

            # language
            response = ResponseLanguage("nightmarket", interaction.locale)

            # endpoint
            endpoint = await self.get_endpoint(interaction.user.id, interaction.locale, 아이디, 비밀번호)

            # fetch skin price
            skin_price = endpoint.store_fetch_offers()
            self.db.insert_skin_price(skin_price)

            # data
            data = endpoint.store_fetch_storefront()
            embeds = GetEmbed.nightmarket(endpoint.player, data, self.bot, response)

            await interaction.followup.send(
                embeds=embeds, view=View.share_button(interaction, embeds) if is_private_message else MISSING
            )
    

    @app_commands.command(description='여러분의 현재 시즌 배틀패스 진행도와 보상을 보여줍니다.')
    # @dynamic_cooldown(cooldown_5s)
    async def 배틀패스(self, interaction: Interaction, 아이디: str = None, 비밀번호: str = None) -> None:
        if False : pass
        else:
        # check if user is logged in
            is_private_message = True if 아이디 is not None or 비밀번호 is not None else False

            await interaction.response.defer(ephemeral=is_private_message)

            response = ResponseLanguage("battlepass", interaction.locale)

            # endpoint
            endpoint = await self.get_endpoint(interaction.user.id, interaction.locale, 아이디, 비밀번호)

            # data
            data = endpoint.fetch_contracts()
            content = endpoint.fetch_content()
            season = useful.get_season_by_content(content)

            embed = GetEmbed.battlepass(endpoint.player, data, season, response)

            await interaction.followup.send(
                embed=embed, view=View.share_button(interaction, [embed]) if is_private_message else MISSING
            )

# inspired by https://github.com/giorgi-o
    @app_commands.command(description="여러분이 궁금해하시는 번들의 정보들을 확인시켜줍니다.")
    @app_commands.describe(번들="알아보고 싶은 번들의 이름을 입력해주세요")
    @app_commands.guild_only()
    # @dynamic_cooldown(cooldown_5s)
    async def 번들찾기(self, interaction: Interaction, 번들: str) -> None:
        if False : pass
        else:
            bundle = 번들
            await interaction.response.defer()

            response = ResponseLanguage("bundle", interaction.locale)

            # setup emoji
            await setup_emoji(self.bot, interaction.guild, interaction.locale)

            # cache
            cache = self.db.read_cache()

            # default language language
            default_language = 'en-US'

            # find bundle
            find_bundle_en_US = [
                cache['bundles'][i]
                for i in cache['bundles']
                if bundle.lower() in cache['bundles'][i]['names'][default_language].lower()
            ]
            find_bundle_locale = [
                cache['bundles'][i]
                for i in cache['bundles']
                if bundle.lower() in cache['bundles'][i]['names'][str(VLR_locale)].lower()
            ]
            find_bundle = find_bundle_en_US if len(find_bundle_en_US) > 0 else find_bundle_locale

            # bundle view
            view = View.BaseBundle(interaction, find_bundle, response)
            await view.start()


    # inspired by https://github.com/giorgi-o
    @app_commands.command(description="현재 상점에 있는 번들(들)의 정보들을 확인시켜줍니다.")
    # @dynamic_cooldown(cooldown_5s)
    async def 현재번들(self, interaction: Interaction) -> None:
        if False : pass
        else:
            await interaction.response.defer()

            response = ResponseLanguage("bundles", interaction.locale)

            # endpoint
            endpoint = await self.get_endpoint(interaction.user.id, interaction.locale)

            # data
            bundle_entries = endpoint.store_fetch_storefront()

            # bundle view
            view = View.BaseBundle(interaction, bundle_entries, response)
            await view.start_furture()

        # credit https://github.com/giorgi-o
        # https://github.com/giorgi-o/SkinPeek/wiki/How-to-get-your-Riot-cookies

        # ---------- ROAD MAP ---------- #

        # @app_commands.command()
        # async def contract(self, interaction: Interaction) -> None:
        #     # change agent contract

        # @app_commands.command()
        # async def party(self, interaction: Interaction) -> None:
        #     # curren party
        #     # pick agent
        #     # current map

        # @app_commands.command()
        # async def career(self, interaction: Interaction) -> None:
        #     # match history



        
async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(ValorantCog(bot))
