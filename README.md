<h1 align="center">
  <br>
  <a href="https://github.com/staciax/ValorantStoreChecker-discord-bot"></a>
  <br>
  발로봇 - 한국인들의 발로란트 봇
  <br>
</h1>

<h4 align="center">상점, 야시장, 스킨 알림등을 한번에!</h4>

<p align="center">
  <a href="https://github.com/teamdoubleeight/Valobot">
     <img src="https://img.shields.io/github/v/release/teamdoubleeight/Valobot" alt="release">
  </a>
  <a href="https://github.com/Rapptz/discord.py/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord.py">
 <a href="https://github.com/teamdoubleeight/Valobot/blob/main/LICENSE">
     <img src="https://img.shields.io/github/license/teamdoubleeight/Valobot" alt="License">

</p>

<p align="center">
  <a href="#about">정보</a>
  •
  <a href="#installation">설치하기</a>
  •
  <a href="#usage">사용하기</a>
</p>

<!-- Inspired by Red Discord Bot -->
<!-- https://github.com/Cog-Creators/Red-DiscordBot -->

## 노트 ⚠️
- 이 프로젝트는 staciax님의 오픈소스 봇인 Valorant-DiscordBot을 기반으로 만들어졌습니다. [여기](https://github.com/staciax/Valorant-DiscordBot)
- 모든 권리는 staciax에게 있지만, 발로봇이 만든 그 외에 모든 것들의 권리는 Team DoubleEight에게 있습니다.


# 정보

인게임 내 상점,야시장 등을 보여주고, 스킨 알림, 티어인증과 같은
편리한 것들을 사용할 수 있는 좋은 봇입니다.
Python 3으로 만들어졌으며, Discord.py를 사용합니다 <br>

## 설치하기

* [Python 3.8+](https://www.python.org/downloads/)

* requirements 설치하기

* 디스코드 봇 만들기

*  **Privileged Gateway Intents**에서 [`MESSAGE CONTENT INTENT`](/resources/dc_MESSAGE_CONTENT_INTENT.png) 켜기

* 봇 [권한](/resources/dc_BOT_PERMS.png) 활성화하기

*  [`bot & applications.commands`](/resources/dc_SCOPES.png) scopes와 함꼐 봇을 서버에 초대하기

* 끝

```bash
pip install -r requirements.txt
```

```bash
# manual install package
pip discord.py
pip install requests
pip install python-dotenv
```

* 봇 토큰과 오너 ID를 .env에다가 넣어놓으세요 [.env](/.env)

```
TOKEN='TOKEN'
OWNER_ID='ID'
```

* 봇 실행하기

```bash
python bot.py
```

* 그 외 다른 사용법들은 본가를 참조하세요 [여기](https://github.com/staciax/Valorant-DiscordBot)

## License

이 프로젝트는 GNUv3 라이센스를 기반으로 만들어졌습니다. 라이선스를 확인하세요.



