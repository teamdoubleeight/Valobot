import discord, requests
from discord import SyncWebhook

def buildhook(vv,ghlt,dt):
    embed = discord.Embed(color=0x1b8dde)
    embed.set_author(name='발로봇이 빌드 되었습니다')
    embed.add_field(name='발로봇 빌드 버전', value=vv, inline=False)
    embed.add_field(name='버전의 빌드 횟수', value=ghlt + "번째", inline=False)
    embed.add_field(name='빌드 일시', value=dt, inline=False)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1045603394087305248/1105483098617041097/val_logo.png?width=682&height=658")
    embed.set_footer(text="발로봇 많은 사랑과 관심 부탁드립니다!", icon_url="https://media.discordapp.net/attachments/1045603394087305248/1105483098617041097/val_logo.png?width=682&height=658")


    webhook = SyncWebhook.from_url("URL")
    webhook.send(embed=embed)


def storehook(discordname, id):
    embed = discord.Embed(color=0xfac48e)
    r = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul").json()
    date = r['dateTime'].split("T") #2023-05-21T08:43:15.4414864
    time = date[1].split(".")[0]
    dt = date[0] + " | " +  time
    embed.set_author(name='유저가 상점을 확인하였습니다')
    embed.add_field(name="디스코드 이름", value=discordname, inline=False)
    embed.add_field(name="디스코드 ID (int)", value=id, inline=False)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1041/1041883.png")
    embed.set_footer(text=" 일시 : " + dt, icon_url="https://media.discordapp.net/attachments/1045603394087305248/1105483098617041097/val_logo.png?width=682&height=658")


    webhook = SyncWebhook.from_url("URL")
    webhook.send(embed=embed)


def logouthook(discordname, thumb, id):
    embed = discord.Embed(color=0xfc0000)
    r = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul").json()
    date = r['dateTime'].split("T") #2023-05-21T08:43:15.4414864
    time = date[1].split(".")[0]
    dt = date[0] + " | " +  time
    embed.set_author(name='유저가 발로봇에서 로그아웃 했습니다')
    embed.add_field(name="디스코드 이름", value=discordname, inline=False)
    embed.add_field(name="디스코드 ID (int)", value=id, inline=False)
    embed.set_thumbnail(url=thumb)
    embed.set_footer(text= " 일시 : " + dt, icon_url="https://media.discordapp.net/attachments/1045603394087305248/1105483098617041097/val_logo.png?width=682&height=658")


    webhook = SyncWebhook.from_url("URL")
    webhook.send(embed=embed)

def loginhook(discordname, valorantname, thumb, id):
    embed = discord.Embed(color=0x2cfc03)
    r = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul").json()
    date = r['dateTime'].split("T") #2023-05-21T08:43:15.4414864
    time = date[1].split(".")[0]
    dt = date[0] + " | " +  time
    embed.set_author(name='유저가 발로봇에 로그인 했습니다')
    embed.add_field(name="디스코드 이름", value=discordname, inline=False)
    embed.add_field(name="디스코드 ID (int)", value=id, inline=False)
    embed.add_field(name="인게임 닉네임/태그", value=valorantname, inline=False)
    embed.set_thumbnail(url=thumb)
    embed.set_footer(text=" 일시 : " + dt, icon_url="https://media.discordapp.net/attachments/1045603394087305248/1105483098617041097/val_logo.png?width=682&height=658")


    webhook = SyncWebhook.from_url("URL")
    webhook.send(embed=embed)
    

    
