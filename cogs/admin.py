from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from utils.checks import owner_only
import discord
from discord import Interaction, app_commands, ui, SelectOption
from discord.ui import View, Select
from discord import app_commands
from discord.ext import commands
if TYPE_CHECKING:
    from bot import ValorantBot
from typing import Union

from cogs.valobotkorea import returnpic
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ext.commands import has_permissions
import json, requests


class Admin(commands.Cog):
    """Error handler"""

    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot
        

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, sync_type: Literal['guild', 'global']) -> None:
        """Sync the application commands"""

        async with ctx.typing():
            if sync_type == 'guild':
                self.bot.tree.copy_global_to(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Synced guild !")
                return

            await self.bot.tree.sync()
            await ctx.reply(f"Synced global !")

    @commands.command()
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, unsync_type: Literal['guild', 'global']) -> None:
        """Unsync the application commands"""

        async with ctx.typing():
            if unsync_type == 'guild':
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Un-Synced guild !")
                return

            self.bot.tree.clear_commands()
            await self.bot.tree.sync()
            await ctx.reply(f"Un-Synced global !")
            
    @app_commands.command(description='다양한 명령어들을 더 쉽게 사용하는 법들을 알려줍니다.')
    @app_commands.describe(명령어='더 알고싶은 명령어를 골라주세요')
    #'쿠키로그인', '로그인', '로그아웃', '상점', '포인트', '미션', '야시장', '배틀패스',
    async def 도움말(self, interaction: Interaction, 명령어: Literal['로그인','로그아웃', '상점', '야시장','배틀패스', '미션','포인트', '번들찾기', '현재번들', '티어인증설정', '티어인증', '알림 등록', '알림 목록', '알림 모드', '알림 채널', '알림 테스트', '프로필', '경쟁프로필', '공식서버', '초대하기', '도움말', '개인정보', '업뎃로그', '정보', '후원하기']) -> None:
        """Shows basic information about the bot."""
        embed = discord.Embed(color=0xFFFFFF)
        try :
            embed.set_thumbnail(url=returnpic())
        except:
            embed.set_thumbnail(url=interaction.user.display_avatar)
        view = ui.View()
        
        if 명령어 == "로그인":
            embed.set_author(name="로그인 명령어 도움말")
            embed.add_field(name='🎁 로그인 명령어',value="발로봇에 여러분에 라이엇\n계정으로 로그인합니다.",inline=True)
            embed.add_field(name='예시 : `/로그인 [ID] [비밀번호]`',value="*참고*  : ID, 비밀번호는 반드시 라이엇 ID와 비밀번호여야 합니다!",inline=False)
            view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtu.be/BvshbJ7zS-o?feature=shared"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/login#login"))
            
        elif 명령어 == "로그아웃":
            embed.set_author(name="로그아웃 명령어 도움말")
            embed.add_field(name='🎄 로그아웃 명령어',value="발로봇에 있는 여러분의 계정을\n발로봇에서 완전히 로그아웃합니다.",inline=True)
            embed.add_field(name='예시 : `/로그아웃`',value="*참고*  : 로그아웃 시 데이터베이스에 있는\n모든 정보는영구적으로 삭제됩니다!",inline=False)
            view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtu.be/BvshbJ7zS-o?feature=shared&t=55"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/login#logout"))
            
        elif 명령어 == "상점":
            embed.set_author(name="상점 명령어 도움말")
            embed.add_field(name='💎 상점 명령어',value="여러분의 발로란트 일일 상점을 확인시켜줍니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/상점`',value="*참고*  : 로그인 되어있지 않는 다른 계정의 상점을 확인하기\n위해서는 `/상점 [ID] [비밀번호]`로 사용해주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/store#store"))
            
        elif 명령어 == "야시장":
            embed.set_author(name="야시장 명령어 도움말")
            embed.add_field(name='💻 야시장 명령어',value="여러분의 미스터리한 야시장을 확인시켜줍니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/야시장`',value="*참고*  : 로그인 되어있지 않는 다른 계정의 야시장을 확인하기\n위해서는 `/야시장 [ID] [비밀번호]`로 사용해주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/store#nightmarket"))
        
        elif 명령어 == "배틀패스":
            embed.set_author(name="배틀패스 명령어 도움말")
            embed.add_field(name='🥇 배틀패스 명령어',value="여러분의 현재 시즌 배틀패스 진행도와 보상을 보여줍니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/배틀패스`',value="*참고*  : 로그인 되어있지 않는 다른 계정의 배틀패스를 확인하기\n위해서는 `/배틀패스 [ID] [비밀번호]`로 사용해주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/store#nightmarket"))
            
        elif 명령어 == "미션":
            embed.set_author(name="미션 명령어 도움말")
            embed.add_field(name='🎨 미션 명령어',value="여러분의 발로란트 미션들과 그 진행도를 보여줍니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/미션`',value="*참고*  : 로그인 되어있지 않는 다른 계정의 미션을 확인하기\n위해서는 `/미션 [ID] [비밀번호]`로 사용해주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/utils#mission"))
            
        elif 명령어 == "포인트":
            embed.set_author(name="포인트 명령어 도움말")
            embed.add_field(name='🎮 포인트 명령어',value="여러분의 발로란트 포인트(VP)와\n레디어나이트 포인트(RP)를 보여줍니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/포인트`',value="*참고*  : 로그인 되어있지 않는 다른 계정의 포인트를 확인하기\n위해서는 `/포인트 [ID] [비밀번호]`로 사용해주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/utils#points"))
            
        elif 명령어 == "번들찾기":
            embed.set_author(name="번들찾기 명령어 도움말")
            embed.add_field(name='🔎 번들찾기 명령어',value="여러분이 궁금해하시는 번들의 정보들을 확인시켜줍니다.",inline=True)
            embed.add_field(name='예시 : `/번들찾기 [번들이름]`',value="*참고*  : 2.0이 포함된 번들은 첫번째가 기본, 두번째가 2.0 번들입니다!",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/bundle#searchbundle"))
            
        elif 명령어 == "현재번들":
            embed.set_author(name="현재번들 명령어 도움말")
            embed.add_field(name='🏆 현재번들 명령어',value="현재 상점에 있는 번들(들)의 정보들을 확인시켜줍니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/현재번들`',value="*참고*  : 발로란트 상점에 2개의 번들이 떠있는 경우 가끔씩\n오류가 날 수 있으나 금방 해결됩니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/bundle#currentbundle"))
            
        elif 명령어 == "티어인증설정":
            embed.set_author(name="티어인증설정 명령어 도움말")
            embed.add_field(name='⌚ 티어인증설정 명령어',value="**[관리자 전용]** `/티어인증` 명령어를 위해 설정을 진행합니다.\n이 명령어는 제대로 사용하기에는 다소 복잡하니 밑에\n**영상 도움말** 또는 **더 자세한 도움말**을 확인해주세요",inline=True)
            embed.add_field(name='예시 : `/티어인증설정 [닉네임 변경모드] [인증채널] [로그채널] [언랭역할] [아이언역할] [브론즈역할] [실버역할] [골드역할] [플래역할] [다이아역할] [초월자역할] [불멸역할] [레디언트역할]`',value="*참고*  : 티어 인증 설정 시 설정한 역할들과 같은 이름의 역할이\n서버에 없어야 오류가 생기지 않고 인증됩니다!",inline=False)
            view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtu.be/ojlltgFtqQw?feature=shared&t=7"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/verify#setting"))
            
        elif 명령어 == "티어인증":
            embed.set_author(name="티어인증 명령어 도움말")
            embed.add_field(name='✅ 티어인증 명령어',value="디스코드 서버에서 여러분의 계정 티어를 인증합니다.\n이 명령어는 가끔 API 요청 수가 너무 과도하면\n티어 인증에 딜레이가 걸릴 수 있습니다.",inline=True)
            embed.add_field(name='예시 : `/티어인증`',value="*참고*  : 티어인증시 역할이 지급되지 않는다면 서버 관리자에게 문의해보세요",inline=False)
            view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtu.be/ojlltgFtqQw?feature=shared&t=131"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/verify#verify"))
            
        elif 명령어 == "알림 등록":
            embed.set_author(name="알림 등록 명령어 도움말")
            embed.add_field(name='🧸 알림 등록 명령어',value="알림을 보내주었으면 하는 스킨들을 설정합니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/알림 등록 [스킨이름]`',value="*참고*  : 알림 설정한 스킨 목록을 보기 위해서는\n`/알림 목록` 명령어를 통해 확인하실 수 있습니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/notify#add"))
            
        elif 명령어 == "알림 목록":
            embed.set_author(name="알림 목록 명령어 도움말")
            embed.add_field(name='📜 알림 목록 명령어',value="`/알림 등록` 명령어에서 등록해둔 스킨들 목록을 확인합니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/알림 목록`',value="*참고*  : 알림 목록에서 스킨을 등록 해제하기 위해서는\n밑에 스킨 순서 숫자에 해당하는 버튼을 눌러주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/notify#list"))
            
        elif 명령어 == "알림 모드":
            embed.set_author(name="알림 모드 명령어 도움말")
            embed.add_field(name='💡 알림 모드 명령어',value="`/알림 등록` 명령어에서 등록해둔 스킨의 알림을 어떻게 보낼지 설정합니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/알림 모드 [모드]`',value="*참고*  : 알림 모드 설정은 **특정 스킨**을 추천합니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/notify#mod"))
            
        elif 명령어 == "알림 채널":
            embed.set_author(name="알림 채널 명령어 도움말")
            embed.add_field(name='🔨 알림 채널 명령어',value="알림을 보낼 곳을 DM과 서버 채널 중에서 설정합니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/알림 채널 [DM 또는 채널]`',value="*참고*  : 만약 설정한 채널이 없어지면 알림은 작동하지 않습니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/notify#channel"))
            
        elif 명령어 == "알림 테스트":
            embed.set_author(name="알림 테스트 명령어 도움말")
            embed.add_field(name='🔋 알림 테스트 명령어',value="알림을 제대로 설정했나 확인 차원에서 테스트합니다.\n사용하기 위해서는 `/로그인`명령어로 로그인 되어있어야 합니다.",inline=True)
            embed.add_field(name='예시 : `/알림 테스트`',value="*참고*  : 알림 테스트는 `/알림 채널` 명령어로 설정한 채널과는\n상관 없이 무조건 DM으로 테스트됩니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/notify#test"))
            
        elif 명령어 == "프로필":
            embed.set_author(name="프로필 명령어 도움말")
            embed.add_field(name='📰 프로필 명령어',value="해당 유저의 발로란트 프로필을 간략하게 보여줍니다.\n로그인 되어있지 않아도 닉네임,태그만으로도 확인 가능합니다.",inline=True)
            embed.add_field(name='예시 : `/프로필 (닉네임) (태그)`',value="*참고*  : 로그인 되어있지만 닉네임과 태그를 입력하시면\n로그인된 계정 대신 입력한 계정의 프로필을 보여줍니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/profile#profile"))
            
        elif 명령어 == "경쟁프로필":
            embed.set_author(name="경쟁프로필 명령어 도움말")
            embed.add_field(name='📱 경쟁프로필 명령어',value="해당 유저의 경쟁전 프로필을 간략하게 보여줍니다.\n로그인 되어있지 않아도 닉네임,태그만으로도 확인 가능합니다.",inline=True)
            embed.add_field(name='예시 : `/경쟁프로필 (닉네임) (태그)  (지역)`',value="*참고*  : 로그인 되어있지만 닉네임과 태그를 입력하시면\n로그인된 계정 대신 입력한 계정의 경쟁프로필을 보여줍니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/profile#competitive"))
            
        elif 명령어 == "공식서버":
            embed.set_author(name="공식서버 명령어 도움말")
            embed.add_field(name='📺 공식서버 명령어',value="발로봇 공식 지원 서버로 초대합니다!",inline=True)
            embed.add_field(name='예시 : `/공식서버`',value="*참고*  : 발로봇 공식서버에도 많은 관심 부탁드려요!",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/others#server"))
        
        elif 명령어 == "초대하기":
            embed.set_author(name="초대하기 명령어 도움말")
            embed.add_field(name='😍 초대하기 명령어',value="발로봇을 여러분의 서버에 초대합니다!",inline=True)
            embed.add_field(name='예시 : `/초대하기`',value="*참고*  : 여러분의 서버에서 직접 발로봇을 더 좋게 즐기세요!",inline=False)
            view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://www.youtube.com/watch?v=coHu8Wc4HfE"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/invite#command"))
            
        elif 명령어 == "도움말":
            embed.set_author(name="도움말 명령어 도움말")
            embed.add_field(name='🔊 도움말 명령어',value="다양한 명령어들을 더 쉽게 사용하는 법들을 알려줍니다.",inline=True)
            embed.add_field(name='예시 : `/도움말 [명령어이름]`',value="*참고*  : 지금 보고 계시는 도움말은 개발자가 순수 직접 다 썼습니다!",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))

            
        elif 명령어 == "개인정보":
            embed.set_author(name="개인정보 명령어 도움말")
            embed.add_field(name='🧮 개인정보 명령어',value="발로봇의 개인정보 활용 동의서와 이용 약관을 확인시켜줍니다.",inline=True)
            embed.add_field(name='예시 : `/개인정보`',value="*참고*  : 해당 TOS & PP는 23.08.02에 작성된 v.2.0입니다.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/tos#command"))
        
        elif 명령어 == "업뎃로그":
            embed.set_author(name="업뎃로그 명령어 도움말")
            embed.add_field(name='📂 업뎃로그 명령어',value="발로봇의 최근 버전 업데이트 로그를 보여줍니다.",inline=True)
            embed.add_field(name='예시 : `/업뎃로그`',value="*참고*  : 현재 버전은 v.1.7.1입니다!",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/others#updlog"))
            
        elif 명령어 == "정보":
            embed.set_author(name="정보 명령어 도움말")
            embed.add_field(name='🎫 정보 명령어',value="발로봇의 기본적인 정보들을 보여줍니다.",inline=True)
            embed.add_field(name='예시 : `/정보`',value="*참고*  : 오류/지원은 개발자 DM 대신 공식 서버에서 해주세요.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/others#info"))
            
        elif 명령어 == "후원하기":
            embed.set_author(name="후원하기 명령어 도움말")
            embed.add_field(name='📀 후원하기 명령어',value="발로봇의 개발자에게 후원해주세요!",inline=True)
            embed.add_field(name='예시 : `/정보`',value="*참고*  : 여러분의 후원은 발로봇을 더욱더 발전시킬 수 있습니다!.",inline=False)
            #view.add_item(ui.Button(label="유튜브 영상 도움말 보러가기", emoji="🎥", url="https://youtube.com"))
            view.add_item(ui.Button(label="더 자세한 도움말 보러가기", emoji="👓", url="https://valobot.gitbook.io/valobot/others#donate"))
            
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(description='봇에 대한 기본적인 정보들을 줍니다')
    async def 정보(self, interaction: Interaction) -> None:
        with open('buildinfo.json', 'r') as f:
            json_data = json.load(f)
            
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='발로봇 by Team DoubleEight')
        embed.add_field(name='**처음 시작**',value="> <t:1667314800>",inline=True)
        embed.add_field(name='**현재 핑**',value=f'> `{str(round(self.bot.latency*1000))} ms (±50ms)`',inline=True)
        embed.add_field(name='**서버 수**',value=f"> `{str(len(self.bot.guilds))}`",inline=True)
        embed.add_field(name='**개발자**',value="DoubleEight (@doubleeight)",inline=True)
        embed.add_field(name='**현재 버전**',value="v.1.7.1 (b.0." + str(json_data['number']) + ")",inline=True)
        view = ui.View()
        view.add_item(ui.Button(label='웹사이트', emoji="💻", url="https://valobot.netlify.app", row=0))
        view.add_item(ui.Button(label='디스코드 서버', emoji="📂", url="https://valobot.netlify.app/discord", row=0))
        view.add_item(ui.Button(label='초대하기', emoji="✨", url="https://valobot.netlify.app/invite", row=0))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1045603394087305248/1105483098617041097/val_logo.png?width=682&height=658")
        embed.set_image(url="https://media.discordapp.net/attachments/1096063160596832418/1096420055455125597/NEWLOGO.png?width=1277&height=658")
        await interaction.response.send_message(embed=embed, view=view)
        
    @app_commands.command(description='발로봇 공식 지원 서버로 초대합니다!')
    async def 공식서버(self, interaction: Interaction) -> None:
        buttonchoosebot  = discord.ui.Button(url="https://valobot.netlify.app/discord",style = discord.ButtonStyle.primary, label="디스코드 서버 참가하기")
        buttons_view = discord.ui.View()
        buttons_view.add_item(buttonchoosebot)
        
        embed2 = discord.Embed(color=0x94fffd)
        embed2.set_author(name="발로봇 공식 서버입니다!")
        embed2.set_thumbnail(url="https://media.discordapp.net/attachments/1045603394087305248/1110475666903797871/val_logo.png")
        embed2.add_field(name="많은 관심과 사랑 부탁드려요", value="by. Team DoubleEight", inline=True)
        
        await interaction.response.send_message(embed=embed2, view=buttons_view)
        
            
    @app_commands.command(description='발로봇을 여러분의 서버에 한번 초대해보세요!')
    async def 초대하기(self, interaction: Interaction) -> None:
        buttonchoosebot  = discord.ui.Button(url="https://valobot.netlify.app/invite",style = discord.ButtonStyle.primary, label="서버에 초대하기")
        buttons_view = discord.ui.View()
        buttons_view.add_item(buttonchoosebot)
        
        embed2 = discord.Embed(color=0xAFE1AF)
        embed2.set_author(name="발로봇을 여러분 서버에서도 사용해보세요")
        embed2.set_thumbnail(url="https://media.discordapp.net/attachments/1045603394087305248/1110475666903797871/val_logo.png")
        embed2.add_field(name="무려 2000서버에서 사용중입니다!", value="by. Team DoubleEight", inline=True)
        
        await interaction.response.send_message(embed=embed2, view=buttons_view)
        
    @app_commands.command(description='발로봇의 개발자에게 후원하세요!')
    async def 후원하기(self, interaction: Interaction) -> None:
        embed2 = discord.Embed(color=0xFFEA00)
        embed2.set_author(name="개발자에게 후원해주세요!")
        embed2.set_thumbnail(url="https://media.discordapp.net/attachments/1045603394087305248/1110475666903797871/val_logo.png")
        embed2.set_image(url="https://media.discordapp.net/attachments/1129331050796036186/1147319123890671696/9aUQQ4YjU9vmKuHT_cZAL61VKpKsLolynnI46BhOZQuKxGJygZ6BJK2zTHoX3pcNQmmcfzcVEZQcythY1lRXBQ.png")
        embed2.add_field(name="토스 1908-9445-1803", value="여러분께 더 좋은 경험을 제공해드리기 위해서\n보내주신 돈은 전액 개발비에 사용합니다.\n\n*TMI : 현재 개발 수익은 마이너스에요 ㅠㅠ*", inline=True)
        
        await interaction.response.send_message(embed=embed2)
        
        
    @app_commands.command(description='발로봇의 최근 버전 업데이트 로그를 보여줍니다.')
    async def 업뎃로그(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='발로봇 v.1.7.1 업데이트 로그')
        embed.add_field(
            name='v.1.7.1때 업데이트된 것들',
            value=f"**1.** `/티어인증`, `/티어인증설정`, `/공식서버`, `/초대하기`, `/후원하기` 명령어를 발로봇에 새롭게 추가했어요\n"
            "**2.** `/야시장`, `/도움말` 명령어들을 더욱더 유용하게 개선했어요 \n"
            "**3.** 도움말을 훨신 더 깔끔하게 바꾸고, 기존 간단한 도움말에서 더 자세한 도움말과 영상 도움말을 만들었어요\n"
            "**4.** html이었던 기존 웹사이트에서 좀 더 역동적인 next.js기반의 부드러운 웹사이트로 개선했어요\n"
            "**5.** TOS와 PP를 v.2.0으로 새롭게 개편했어요\n",
            inline=False,
        )
        try :
            embed.set_thumbnail(url=returnpic())
        except:
            embed.set_thumbnail(url=interaction.user.display_avatar)
        view = ui.View()
        view.add_item(ui.Button(label='더 자세하게 영상으로 확인하기', emoji="💻", url="https://www.youtube.com/watch?v=ORKF84SVTK4", row=0))
        await interaction.response.send_message(embed=embed, view=view)
    
    @app_commands.command(description='발로봇의 개인정보 활용 동의서와 이용 약관을 확인시켜줍니다.')
    async def 개인정보(self, interaction: Interaction) -> None:
        """Shows basic information about the bot."""
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='발로봇 개인정보 활용 동의서와 이용 약관')
        embed.add_field(name=f'{interaction.user.display_name}님, 발로봇 개인정보 활용 동의서와 이용 약관을 확인해주세요', value=f"버전 2.2, 2023.08.10", inline=False)
        embed.add_field(
            name='1. 이용약관',
            value="""1-1. 발로봇과 웹사이트 등 발로봇에 관련된 모든 것들을 이하 '서비스'라 칭하고
서비스를 이용하는 모두를 '사용자'라고 칭한다.
또한 서비스를 제공하는 개발진을 '서비스 제공자'라고 칭한다.
1-2. 사용자는 서비스를 이용하기 위해서는 반드시 이용약관(TOS)와 개인정보 활용 동의서(PP)를 모두 확인하고 동의해야만 하고, 만일 미확인하거나 동의하지 않을 시 일어나는 모든 일들의 책임은 사용자가 모두 진다.
1-3. 사용자가 서비스를 이용하는 중에 사용자 본인의 부주의로 일어나는 모든 일의 책임은 사용자 본인에게 모두 있으며, 서비스 제공자는 그 어떤 것도 배상하지 않는다.""",
            inline=False,
        )
        embed.add_field(
            name='2. 서비스의 보호',
            value="""2-1. 사용자는 서버스를 이용하면서 서비스 측에 그 어떠한 피해를 주지 않아야 하고
서비스에게 피해를 조금이라도 주었을 시 모두 본인이 변상하고 후속 조치까지 취하도록 한다.
2-2. '피해'의 종류에는 서비스 해킹, 디스코드 / 호스팅 서버 테러, 봇에게 직접 테러 등이 있다.""",
            inline=False,
        )
        embed.add_field(
            name='3. 수집하는 개인정보',
            value="""3-1. 서비스는 사용자에게서 사용자에 대한 개인정보를 수집하고, 수집한 개인정보들을 사용할 수 있다.
3-2. 서비스는 일시적으로 '사용자의 라이엇 ID와 비밀번호', '사용자의 디스코드 프로필 사진',
'사용자의 디스코드 닉네임'을 수집하고 사용한 뒤 그 뒤에 곧바로 영구적으로 폐기한다.
3-3. 서비스는 '사용자의 라이엇 Auth토큰과 Ent토큰, 쿠키', '사용자의 디스코드 ID(int)'
'사용자의 언어', '사용자의 발로란트 서버 지역', '사용자의 디스코드 서버 이름'을 수집하고 DB에 저장하고,
사용자의 요청이 있을 시 언제든지 DB으로부터 그 정보를 불러와 사용한다.""",
            inline=False,
        )
        embed.add_field(
            name='4. 개인정보의 파기와 보안',
            value="""4-1. 사용자가 개인정보 파기를 원할 시, 앱 내에서 /로그아웃 명령어를 사용해 데이터베이스에서 자신의 모든 개인정보들을 영구적으로 삭제할 수 있으며, 이에 대한 불이익은 없고,
다시 /로그인 명령어를 사용할시 데이터베이스에 새롭게 업데이트되어 저장된다.
4-2. 서비스 제공자의 잘못으로 인해 사용자의 개인정보가 제3자에게 유출/판매 되었을 때에는 서비스 제공자가 모든 책임을 다 지고 모두에게 합당한 보상을 해주어야 한다.
4-3. 하지만 만약 사용자 본인의 잘못으로 인해 개인정보가 제3자에게 유출/판매 되었을 시에는 사용자가 모든 책임을 지고, 서비스 제공자는 그 어떤 책임도 지지 않으며, 사용자에게 그 어떤 것도 변상할 의무가 없다.""",
            inline=False,
        )
        embed.add_field(
            name='5. TOS와 PP',
            value="""5-1. 위 이용약관과 개인정보 활용에 동의해야만 사용이 가능하며, 동의하지 않을 시 다시 동의하기 전까지는 서비스의 사용이 불가능하다.
Tos and Pp v.2.0 | 23.08.02""",
            inline=False,
        )
        try :
            embed.set_thumbnail(url=returnpic())
        except:
            embed.set_thumbnail(url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    

        
async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(Admin(bot))
