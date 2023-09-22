import requests, random


# 사진 랜덤하게 출력하기
def returnpic():
    try :
        r = requests.get("https://raw.githubusercontent.com/KLDiscord/valorantbotkorea/main/pic.txt")
        r = r.text
        sp = r.split("\n")
        l = []
        for i in range(83):
            l.append(sp[i])
            
        return l[random.randint(1,83)]
    except :
        return None

# 숫자(valorant-api.com)를 티어(1~3으로 바꿔주기)
def returntier(tiernum):
    if tiernum == 3: tier = "아이언 1"
    elif tiernum == 4 : tier = "아이언2"
    elif tiernum == 5 : tier = "아이언3"
    elif tiernum == 6 : tier = "브론즈1"
    elif tiernum == 7 : tier = "브론즈2"
    elif tiernum == 8 : tier = "브론즈3"
    elif tiernum == 9 : tier = "실버1"
    elif tiernum == 10 : tier = "실버2"
    elif tiernum == 11 : tier = "실버3"
    elif tiernum == 12 : tier = "골드1"
    elif tiernum == 13 : tier = "골드2"
    elif tiernum == 14 : tier = "골드3"
    elif tiernum == 15 : tier = "플래티넘1"
    elif tiernum == 16 : tier = "플래티넘2"
    elif tiernum == 17 : tier = "플래티넘3"
    elif tiernum == 18 : tier = "다이아1"
    elif tiernum == 19 : tier = "다이아2"
    elif tiernum == 20 : tier = "다이아3"
    elif tiernum == 21 : tier = "초월자1"
    elif tiernum == 22 : tier = "초월자2"
    elif tiernum == 23 : tier = "초월자3"
    elif tiernum == 24 : tier = "불멸1"
    elif tiernum == 25 : tier = "불멸2"
    elif tiernum == 26 : tier = "불멸3"
    elif tiernum == 27 : tier = "레디언트"
    else : tier = "언랭"
    return tier

# 숫자(valorant-api.com)를 티어 이름으로 바꿔주기
def returntieroriginal(tiernum):
    if tiernum == 3 or tiernum == 4 or tiernum == 5: tier = "아이언"
    elif tiernum == 6 or tiernum == 7 or tiernum == 8 : tier = "브론즈"
    elif tiernum == 9 or tiernum == 10 or tiernum == 11 : tier = "실버"
    elif tiernum == 12 or tiernum == 13 or tiernum == 14 : tier = "골드"
    elif tiernum == 15 or tiernum == 16 or tiernum == 17: tier = "플래티넘"
    elif tiernum == 18 or tiernum == 19 or tiernum == 20 : tier = "다이아"
    elif tiernum == 21 or tiernum == 22 or tiernum == 23 : tier = "초월자"
    elif tiernum == 24 or tiernum == 25 or tiernum == 26 : tier = "불멸"
    elif tiernum == 27 : tier = "레디언트"
    else : tier = "언랭"
    return tier
    