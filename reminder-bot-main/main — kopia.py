import asyncio
import discord
import gspread
from datetime import datetime
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()
global tommorow, commands, wazne, eegs, today
wazne = ""
today = str(datetime.today().date())
tommorow = str(datetime.today().date() + timedelta(days=1))
commands = {
    "ao": "Analiza Obwodów\nWykład: Teams AO_II_2020_zima\nUPEL: https://upel2.cel.agh.edu.pl/wiet/course/view.php?id=1061",
    "mn": "Metody Numeryczne\nWykład: Teams Met_Num_2020_zima",
    "cue": "Cyfrowe Układy Elektroniczne\nWykład: Teams IET_KE_CUE\nLaby: Teams CUE2 zima 2020/2021, kod:j6hf5t0",
    "ee": "Elementy Elektroniczne\nWykład i Laby: https://iet-agh.webex.com/meet/dziurdzi",
    "ts": "Teoria Sygnałów\nWykład, Laby, Ćwiczenia: https://iet-agh.webex.com/meet/korohoda\nMateriały: http://home.agh.edu.pl/~korohoda/rok_2020_2021_zima/TS_EL_2/ (klucz: teor_+syg*7)\nhttps://upel2.cel.agh.edu.pl/wiet/course/view.php?id=1074 ",
    "po": "Programowanie Obiektowe\nWykład: https://iet-agh.webex.com/iet-agh/j.php?MTID=m1b88ee8d5b211e226ccb1b32bf968c07 \nLaby: skype: rafal.fraczek@cyfronet.pl\n  https://docs.google.com/document/d/1ZCi0pdhFpTjp16Vc8hD3hTf_W4TmSiwrQ09xzo-FW2Y/edit?usp=drivesdk",
    "ap": "Automatyka Przemysłowa\nWykład: https://iet-agh.webex.com/join/jacek.ostrowski",
    "pz": "Podstawy Zarządzania\nWykład: Teams Wykłady_Podstawy Zarządzania\n UPEL: https://upel2.cel.agh.edu.pl/wiet/course/view.php?id=966 ",
    "ważne": wazne,
    "wazne": wazne,
    "halp": "**S P I S   K O M E N D:**\n!<skrótprzedmiotu> - linki związane z danym przedmiotem (PZ, AO, CUE, EE, TS, MN, AP, PO)\nCo jutro? - pokazuje co jutro\nCo dzisiaj?/Co dziś? - pokazuje co dzisiaj\n Co w <dzień tygodnia>? pokazuje co w dany dzień C:"
}
pics = {
    "korohod": "korohoda.png",
    "sypk": "sypka.png",
    "co?": "co.png"
}
eegs = {
    "haha(1)": "haha(2)",
    "korochod": "chacha(1)",
    "karwatowski": "\"Symulacja nie pokazuje czy układ działa prawidłowo, jest tylko kilka wyników i też nie są one sprawdzone\""
}
dayz = ("poniedziałek", "wtorek", "środ", "czwartek", "piątek")
def getData(when):
    global sheet, vals, LAB_1, LAB_2, LAB_3, row, mess
    mess = ""
    tommorow = str(datetime.today().date() + timedelta(days=1))
    today = str(datetime.today().date())
    tot = [tommorow, today]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gclient = gspread.authorize(creds)
    sheet = gclient.open("sheet1").sheet1
    vals = sheet.get_all_values()
    if when == 0:
        mess = "Jutro({}) masz:\nPrzedmioty: {}\nKolosy: {}\nZadania: {}\n{}"
        row = 0
        for i in range(len(vals)):
            if (str(vals[i][0]) == tommorow):
                row = i
            if (str(vals[i][0]) == "WAŻNE INFO NA TEN TYDZIEŃ:" and str(vals[i][1]) != ""):
                commands["wazne"] = str("**------WAŻNE!------**\n" + vals[i][1])
                commands["ważne"] = commands["wazne"]
                print(wazne)
            else:
                commands["wazne"] = ""
                commands["ważne"] = commands["wazne"]
            when = str(tommorow)
    elif when == 1:
        mess = "Dzisiaj({}) masz:\nPrzedmioty: {}\nKolosy: {}\nZadania: {}\n{}"
        row = 0
        for i in range(len(vals)):
            if (str(vals[i][0]) == today):
                row = i
            if (str(vals[i][0]) == "WAŻNE INFO NA TEN TYDZIEŃ:" and str(vals[i][1]) != ""):
                commands["wazne"] = str("**------WAŻNE!------**\n" + vals[i][1])
                commands["ważne"] = commands["wazne"]
                print(wazne)
            else:
                commands["wazne"] = ""
                commands["ważne"] = commands["wazne"]
            when = str(today)
    else:
        row = 0
        for i in range(len(dayz)):
            if str(when) == dayz[i]:
                for i in range(len(vals)):
                    if(when in str(vals[i][10]).lower()):
                        row = i
                        print(i)
                        if when == "wtorek":
                            mess = "We {} masz:\nPrzedmioty: {}\nKolosy: {}\nZadania: {}\n{}"
                        else:
                            mess = "W {} masz:\nPrzedmioty: {}\nKolosy: {}\nZadania: {}\n{}"
        if when == "środ":
            when = "środę"

    LAB_1 = mess.format(when, vals[row][1], vals[row][2],vals[row][3], commands["wazne"])
    LAB_2 = mess.format(when, vals[row][4], vals[row][5],vals[row][6], commands["wazne"])
    LAB_3 = mess.format(when, vals[row][7], vals[row][8],vals[row][9], commands["wazne"])

getData(0)

@client.event
async def on_ready():
    print(f'{client.user} has connected')


@client.event
async def on_message(message):
    global lastAuthor, linkAuthor, vc
    lastAuthor = message.author
    if message.author == client.user:
        return
    elif message.content.lower() == "wykurwiaj":
        print("CH")
        vc.stop()
        await vc.disconnect()
        print("uj")
    elif message.content.startswith('!') and commands.get(message.content.lower()[1:]):
        await message.channel.send(commands.get(message.content.lower()[1:]))
    elif(message.content == 'Przypominajko!' or message.content.lower() == 'co jutro?'):
        try:
            getData(0)
            if (message.author == "adam_mickiewicz#9427"):
                await message.channel.send("Sukrwysynu jebany\n ")
            elif ("Laby 1" in str(message.author.roles)):
                await message.channel.send(LAB_1)
            elif ("Laby 2" in str(message.author.roles)):
                await message.channel.send(LAB_2)
            elif("Laby 3" in str(message.author.roles)):
                await message.channel.send(LAB_3)
            else:
                await message.channel.send("Nie potrafie ci pomóc")
        except:
            print("")
    elif(message.content.lower() == "co dzisiaj?" or message.content.lower() == "co dziś?"):
        try:
            getData(1)
            if (message.author == "adam_mickiewicz#9427"):
                await message.channel.send("Sukrwysynu jebany\n ")
            elif ("Laby 1" in str(message.author.roles)):
                await message.channel.send(LAB_1)
            elif ("Laby 2" in str(message.author.roles)):
                await message.channel.send(LAB_2)
            elif("Laby 3" in str(message.author.roles)):
                await message.channel.send(LAB_3)
            else:
                await message.channel.send("Nie potrafie ci pomóc")
        except:
            print("")
    elif("Co w" in message.content and "?" in message.content.lower()):
        for i in range(len(dayz)):
            if dayz[i] in message.content.lower():
                try:
                    getData(dayz[i])
                    if (message.author == "adam_mickiewicz#9427"):
                        await message.channel.send("Sukrwysynu jebany\n ")
                    elif ("Laby 1" in str(message.author.roles)):
                        await message.channel.send(LAB_1)
                    elif ("Laby 2" in str(message.author.roles)):
                        await message.channel.send(LAB_2)
                    elif ("Laby 3" in str(message.author.roles)):
                        await message.channel.send(LAB_3)
                    else:
                        await message.channel.send("Nie potrafie ci pomóc")
                except:
                    print("")
    elif("chillera" in message.content.lower()):
        print(message.author.voice.channel)
        vc = await message.author.voice.channel.connect()
        vc.stop()
        vc.play(discord.FFmpegPCMAudio('sample1.mp3'), after=lambda e: print("OK", e))
        await message.channel.send("Odtwarzanie **sample1.mp3** autorstwa **Sylwester Zackonor Mącznik**")
    elif(message.content.lower() == "gotowe"):
        print(message.author.voice.channel)
        vc = await message.author.voice.channel.connect()
        vc.stop()
        vc.play(discord.FFmpegPCMAudio('gotowe.mp3'), after=lambda e: print("OK", e))
    elif("link" in message.content or "linka" in message.content):
        global linkevent
        await message.channel.send("Czy jesteś pewien, że sprawdziłeś sekcję \"LINKI\"???")
        linkAuthor = message.author
        linkevent = 1
    elif("nie" in message.content.lower() and linkevent == 1):
        if(linkAuthor == lastAuthor):
            await message.channel.send("To kurwa sprawdź 🤦‍")
            await message.channel.send(file=discord.File('gorlich.jpg'))
            linkAuthor =""
            lastAuthor =""
            linkevent = 0
    elif("tak" in message.content.lower() and linkevent == 1):
        if (linkAuthor == lastAuthor):
            await message.channel.send("To zobacz jeszcze tutaj: https://docs.google.com/document/d/1AEpgHGvYnHHg0PCNaBX5As3rcggNjfzjuwfU0wpVZpI/edit")
            linkAuthor = ""
            lastAuthor = ""
            linkevent = 0
    else:
        for i in pics:
            if i in message.content.lower():
                emoji = discord.utils.get(client.emojis, name='szacun')
                await message.add_reaction(emoji)
                await message.channel.send(file = discord.File(pics[i]))
                if (i == "korohod" and message.author.voice is not None):
                    print(message.author.voice.channel)
                    vc = await message.author.voice.channel.connect()
                    vc.stop()
                    vc.play(discord.FFmpegPCMAudio('korohoda_song.mp3'), after=lambda e: print("OK", e))
        for i in eegs:
            if i in message.content.lower():
                await message.channel.send(eegs[i])

client.run("NzY1MjMwODY0MDI3MDkwOTQ1.X4Ryxw.BvbbT2huAM9WIUfsOP00-gYiPRg")
