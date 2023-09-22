from __future__ import annotations

from typing import TYPE_CHECKING, Literal
import discord
from discord import Interaction, app_commands, ui, SelectOption
from discord.ui import View, Select
from discord import app_commands
from discord.ext import commands
if TYPE_CHECKING:
    from bot import ValorantBot
from typing import Union
from discord.utils import get
from cogs.valobotkorea import returnpic, returntieroriginal
import json, requests
from utils.valorant.db import DATABASE

class Verify(commands.Cog):

    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot
        self.db = DATABASE()
        
    @app_commands.command(description='디스코드 서버에서 여러분의 계정 티어를 인증합니다.')
    @app_commands.describe()
    async def 티어인증(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        f = self.db.read_db()
        data = f.get(str(interaction.user.id), None) # 유저 데이터, 로그인X면 None
        view = ui.View()
        view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtu.be/ojlltgFtqQw?feature=shared"))
        if data == None:
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name='❌ 오류 : 로그인되어있지 않습니다.')
            embed.add_field(name='`/로그인` 명령어를 통해 로그인 후 다시 진행해주세요', value="해결되지 않는다면 **/공식서버**를 입력해 공식 서버에서 말해주세요.", inline=True)
            try:
                embed.set_thumbnail(url=returnpic())
            except:
                embed.set_thumbnail(url=interaction.user.display_avatar)
            embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
            await interaction.followup.send(embed=embed, ephemeral=True, view=view)
        else:
            with open("data/verifysettings.json", "r+", encoding='utf-8') as json_file:
                vvdata = json.load(json_file)
            if str(interaction.guild_id) not in vvdata:
                embed = discord.Embed(color=0xFF0000)
                embed.set_author(name='❌ 오류 : 인증설정이 되어있지 않습니다.')
                embed.add_field(name='서버 관리자가 인증 설정을 아직 하지 않았습니다.', value="관리자이신데 어떻게 설정하는지 모르신다면 `/티어인증설정`을 해주세요", inline=True)
                try:
                    embed.set_thumbnail(url=returnpic())
                except:
                    embed.set_thumbnail(url=interaction.user.display_avatar)
                embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            else:
                try:
                    name = data['username'].split("#")
                    nickname = name[0]
                    tag = name[1]
                    rg = data['region']        
                    r = requests.get("https://api.henrikdev.xyz/valorant/v2/mmr/" + rg + "/" + nickname + "/" + tag)
                    rr = r.json()
                    tier = rr['data']['current_data']['currenttier']
                    tier = returntieroriginal(tier)
                    thumb = rr['data']['current_data']['images']['large']
                    r = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul").json()
                    date = r['dateTime'].split("T") #2023-05-21T08:43:15.4414864
                    time = date[1].split(".")[0]
                    dt = date[0] + " | " +  time
            
                    embed = discord.Embed(color=0x94fffd)
                    embed.set_author(name="서버에서 티어 인증 완료 - " + str(tier) )
                    embed.set_thumbnail(url=thumb)
                    embed.add_field(name="플레이어 이름", value=nickname + "#" + tag, inline=False)
                    embed.add_field(name="현재 경쟁전 티어", value=tier, inline=False)
                    embed.set_footer(text=" 일시 : " + dt + " • 인증유저 : " + interaction.user.display_name)
                    if interaction.guild_id == 698137799999881216:
                        embed.set_image(url="https://media.discordapp.net/attachments/1135549809655300126/1135816310094319656/b620528e459c430f.jpg")
                    
                    if tier == "언랭" : role = "UnRanked"
                    elif tier =="아이언" : role="Iron"
                    elif tier =="브론즈" : role="Bronze"
                    elif tier =="실버" : role="Silver"
                    elif tier =="골드" : role="Gold"
                    elif tier =="플래티넘" : role="Platinum"
                    elif tier =="다이아" : role="Diamond"
                    elif tier =="초월자" : role="Ascendant"
                    elif tier =="불멸" : role="Immortal"
                    elif tier =="레디언트" : role="Radiant"
                    with open("data/verifysettings.json", "r+", encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        rolename = data[str(interaction.guild.id)]['RoleNames'][role]
                        logchannel = data[str(interaction.guild.id)]["LogChannel"]
                        verchannel = data[str(interaction.guild.id)]["Channel"]
                        mode = data[str(interaction.guild.id)]["Mode"]
                        
                    if interaction.channel_id != verchannel:
                        embed = discord.Embed(color=0xFF0000)
                        embed.set_author(name='❌ 오류 : 여기는 인증 채널이 아닙니다.')
                        embed.add_field(name='서버 관리자가 채널 설정을 이 채널로 하지 않았습니다', value="관리자이신데 어떻게 설정하는지 모르신다면 `/티어인증설정`을 해주세요", inline=True)
                        try:
                            embed.set_thumbnail(url=returnpic())
                        except:
                            embed.set_thumbnail(url=interaction.user.display_avatar)
                        embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                        await interaction.followup.send(embed=embed, ephemeral=True, view=view)
                    else:
                        member = interaction.user # 역할 추가하기
                        role = get(member.guild.roles, name=rolename)
                        await member.add_roles(role)
                        
                        #유저 닉네임 변경
                        
                        if interaction.user.guild_permissions.administrator == True:
                            log = "관리자의 닉네임은 권한이 부족해 변하지 않았습니다."
                        else:
                            if mode == "NoChange":
                                log = "유저의 닉네임은 변하지 않았습니다."
                                
                            elif mode == "TierCurrent" :
                                await interaction.user.edit(nick = "[" + tier + "] " + interaction.user.nick)
                                log = "유저 닉네임이 **"+ "[" + tier + "] " + interaction.user.nick + "** (으)로 바뀌었습니다."
                                
                            elif mode == "NicknameTag" :
                                await interaction.user.edit(nick = nickname + "#" + tag)
                                log = "유저 닉네임이 **"+ nickname + "#" + tag + "** (으)로 바뀌었습니다."
                                
                            elif mode == "TierNicknameTag" :
                                await interaction.user.edit(nick = "[" + tier + "] " + nickname + "#" + tag)
                                log = "유저 닉네임이 **"+  "[" + tier + "] " + nickname + "#" + tag + "** (으)로 바뀌었습니다."
                                
                            elif mode == "Nickname" :
                                await interaction.user.edit(nick = nickname)
                                log = "유저 닉네임이 **"+ nickname + "** (으)로 바뀌었습니다."
                                
                        embed2 = discord.Embed(color=0x94fffd)
                        embed2.set_author(name="[로그] 유저가 인증을 진행했습니다 - " + str(tier))
                        embed2.set_thumbnail(url=thumb)
                        embed2.add_field(name="플레이어 이름", value=nickname + "#" + tag, inline=False)
                        embed2.add_field(name="현재 경쟁전 티어", value=tier, inline=False)
                        embed2.add_field(name="로그", value=log, inline=False)
                        embed2.set_footer(text=" 일시 : " + dt + " • 인증유저 : " + interaction.user.name)
                        
                        channel  = self.bot.get_channel(logchannel)
                        await channel.send(embed=embed2)

                        await interaction.followup.send(embed=embed, ephemeral=True, view=view)          # 결과 유저에게 보내기  
                except:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name='❌ 오류 : 알 수 없는 오류가 발생했습니다.')
                    embed.add_field(name='잠시만 기다리시거나 다시한번 시도해보세요', value="해결되지 않는다면 **/공식서버**를 입력해 공식 서버에서 말해주세요.", inline=True)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                    await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            
    @app_commands.command(description='[관리자 전용] /티어인증 명령어를 위해 설정을 진행합니다.')
    @app_commands.describe(닉네임변경='인증 후 해당 유저의 서버 닉네임을 어떻게 변경할지 설정합니다', 인증채널 = '유저들이 인증할 채널을 설정합니다', 로그채널='로그가 올라올 채널을 설정합니다.')
    async def 티어인증설정(self, interaction: Interaction,닉네임변경 : Literal["변경 안함", "(인게임 닉네임) 으로 변경","[티어] (현재 디스코드 닉네임) 으로 변경",  "(인게임 닉네임#태그) 으로 변경", "[티어] (인게임 닉네임#태그) 로 변경"], 인증채널 : discord.TextChannel, 로그채널 : discord.TextChannel, 언랭:discord.Role, 아이언:discord.Role, 브론즈:discord.Role, 실버:discord.Role, 골드:discord.Role, 플래티넘:discord.Role, 다이아:discord.Role, 초월자:discord.Role, 불멸:discord.Role, 레디언트:discord.Role) -> None:
        await interaction.response.defer()
        view = ui.View()
        view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtu.be/ojlltgFtqQw?feature=shared"))
        if interaction.user.guild_permissions.administrator == True:
            if 닉네임변경 == "변경 안함":
                Change = "NoChange"
            elif 닉네임변경 =="[티어] (현재 디스코드 닉네임) 으로 변경":
                Change = "TierCurrent"
            elif 닉네임변경 == "(인게임 닉네임#태그) 으로 변경":
                Change = "NicknameTag"
            elif 닉네임변경 == "[티어] (인게임 닉네임#태그) 로 변경":
                Change = "TierNicknameTag"
            elif 닉네임변경 == "(인게임 닉네임) 으로 변경":
                Change = "Nickname"
            if 로그채널.id == 인증채널.id:
                embed = discord.Embed(color=0xFF0000)
                embed.set_author(name='❌ 오류 : 인증채널과 로그채널은 달라야 합니다.')
                embed.add_field(name='채널을 올바르게 설정해보세요', value="서버 설정에서 역할을 제대로 설정하였는지 다시한번 확인해보세요.", inline=True)
                try:
                    embed.set_thumbnail(url=returnpic())
                except:
                    embed.set_thumbnail(url=interaction.user.display_avatar)
                embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            if 언랭.is_default() == True or 언랭.is_bot_managed() == True or 언랭.is_assignable() == False or 아이언.is_default() == True or 아이언.is_bot_managed() == True or 아이언.is_assignable() == False or 브론즈.is_default() == True or 브론즈.is_bot_managed() == True or 브론즈.is_assignable() == False or 실버.is_default() == True or 실버.is_bot_managed() == True or 실버.is_assignable() == False or 골드.is_default() == True or 골드.is_bot_managed() == True or 골드.is_assignable() == False or 플래티넘.is_default() == True or 플래티넘.is_bot_managed() == True or 플래티넘.is_assignable() == False or 다이아.is_default() == True or 다이아.is_bot_managed() == True or 다이아.is_assignable() == False or 초월자.is_default() == True or 초월자.is_bot_managed() == True or 초월자.is_assignable() == False or 불멸.is_default() == True or 불멸.is_bot_managed() == True or 불멸.is_assignable() == False or 레디언트.is_default() == True or 레디언트.is_bot_managed() == True or 레디언트.is_assignable() == False :
                embed = discord.Embed(color=0xFF0000)
                embed.set_author(name='❌ 오류 : 역할이 올바르지 않습니다.')
                embed.add_field(name='역할을 올바르게 설정해보세요', value="서버 설정에서 역할을 제대로 설정하였는지 다시한번 확인해보세요.", inline=True)
                try:
                    embed.set_thumbnail(url=returnpic())
                except:
                    embed.set_thumbnail(url=interaction.user.display_avatar)
                embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            
            else:
                try:
                    with open("data/verifysettings.json", "r+", encoding='utf-8') as json_file:
                        
                        data = json.load(json_file)
                        data[str(interaction.guild.id)] = {}
                        data[str(interaction.guild.id)]["Channel"] = 인증채널.id
                        data[str(interaction.guild.id)]["LogChannel"] = 로그채널.id
                        data[str(interaction.guild.id)]["Mode"] = Change
                        data[str(interaction.guild.id)]['RoleNames'] = {}
                        data[str(interaction.guild.id)]['RoleNames']['UnRanked'] = str(언랭.name)
                        data[str(interaction.guild.id)]['RoleNames']['Iron'] = str(아이언.name)
                        data[str(interaction.guild.id)]['RoleNames']['Bronze'] = str(브론즈.name)
                        data[str(interaction.guild.id)]['RoleNames']['Silver'] = str(실버.name)
                        data[str(interaction.guild.id)]['RoleNames']['Gold'] = str(골드.name)
                        data[str(interaction.guild.id)]['RoleNames']['Platinum'] = str(플래티넘.name)
                        data[str(interaction.guild.id)]['RoleNames']['Diamond'] = str(다이아.name)
                        data[str(interaction.guild.id)]['RoleNames']['Ascendant'] = str(초월자.name)
                        data[str(interaction.guild.id)]['RoleNames']['Immortal'] = str(불멸.name)
                        data[str(interaction.guild.id)]['RoleNames']['Radiant'] = str(레디언트.name)
                            
                    with open('data/verifysettings.json', 'w+', encoding='utf-8') as json_file:
                        json.dump(data, json_file, ensure_ascii=False, indent=2)
                        
                    embed = discord.Embed(color=0x50C878)
                    embed.set_author(name='티어 인증 설정 완료!')
                    embed.add_field(name='인증채널', value="#" + str(인증채널.name), inline=False)
                    embed.add_field(name='로그채널', value="#" + str(로그채널.name), inline=False)
                    embed.add_field(name='닉네임 변경', value=닉네임변경, inline=False)
                    embed.add_field(name='티어 역할', value="**언랭** : " + 언랭.name + " | **아이언** : " + 아이언.name + " | **브론즈** : " + 브론즈.name + " | **실버** : " + 실버.name + " | **골드** : " + 골드.name + " | **플래티넘** : " + 플래티넘.name + " | **다이아** : " + 다이아.name + " | **초월자** : " + 초월자.name + " | **불멸** : " + 불멸.name + " | **레디언트** : " + 레디언트.name, inline=False)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    r = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul").json()
                    date = r['dateTime'].split("T") #2023-05-21T08:43:15.4414864
                    time = date[1].split(".")[0]
                    dt = date[0] + " | " +  time
                    embed.set_footer(text=" 일시 : " + dt + " • 설정한 유저 : " + interaction.user.display_name)
                
                    await interaction.followup.send(embed=embed)
                except:
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name='❌ 오류 : 알 수 없는 오류가 발생했습니다.')
                    embed.add_field(name='잠시만 기다리시거나 다시한번 시도해보세요', value="해결되지 않는다면 **/공식서버**를 입력해 공식 서버에서 말해주세요.", inline=True)
                    try:
                        embed.set_thumbnail(url=returnpic())
                    except:
                        embed.set_thumbnail(url=interaction.user.display_avatar)
                    embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
                    await interaction.followup.send(embed=embed, ephemeral=True, view=view)
           
        else:
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name='❌ 오류 : 유저가 관리자가 아닙니다.')
            embed.add_field(name='다시한번 시도해주세요', value="서버 설정에서 해당 유저에게 관리자 권한이 있는지 확인해보세요", inline=True)
            try:
                embed.set_thumbnail(url=returnpic())
            except:
                embed.set_thumbnail(url=interaction.user.display_avatar)
            embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
            await interaction.followup.send(embed=embed, ephemeral=True, view=view)
            
    

        
async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(Verify(bot))
    