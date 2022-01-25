import asyncio
import discord
import json
import gspread
from datetime import datetime
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()
global tommorow, commands, wazne, eegs, today
wazne = ""
today = str(datetime.today().date())
tommorow = str(datetime.today().date() + timedelta(days=1))
with open('commands.json', encoding="utf8")as file:
    commands = json.load(file)

eegs = {
    "haha(1)": "haha(2)",
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

    LAB_1 = discord.Embed(title='Plan na {}:'.format(when), colour=discord.Colour.from_rgb(234, 46, 255), description= commands["wazne"])
    LAB_1.add_field(name='Przedmioty', value=vals[row][1], inline=True)
    LAB_1.add_field(name="Kolosy", value=vals[row][2], inline=True)
    LAB_1.add_field(name="Zadania", value=vals[row][3], inline=True)

    LAB_2 = discord.Embed(title='Plan na {}:'.format(when), colour=discord.Colour.from_rgb(234, 46, 255),description= commands["wazne"])
    LAB_2.add_field(name='Przedmioty', value=vals[row][4], inline=True)
    LAB_2.add_field(name="Kolosy", value=vals[row][5], inline=True)
    LAB_2.add_field(name="Zadania", value=vals[row][6], inline=True)

    LAB_3 = discord.Embed(title='Plan na {}:'.format(when), colour=discord.Colour.from_rgb(234, 46, 255),description= commands["wazne"])
    LAB_3.add_field(name='Przedmioty', value=vals[row][7], inline=True)
    LAB_3.add_field(name="Kolosy", value=vals[row][8], inline=True)
    LAB_3.add_field(name="Zadania", value=vals[row][9], inline=True)


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
    elif message.content.startswith('!') and commands.get(message.content.lower()[1:]):
        await message.channel.send(embed = discord.Embed(description=commands.get(message.content.lower()[1:]),colour=discord.Colour.from_rgb(234, 46, 255)))
    elif(message.content == 'Przypominajko!' or message.content.lower() == 'co jutro?'):
        try:
            getData(0)
            if   ("Laby 1" in str(message.author.roles)):
                await message.channel.send(embed = LAB_1)
            elif ("Laby 2" in str(message.author.roles)):
                await message.channel.send(embed = LAB_2)
            elif("Laby 3" in str(message.author.roles)):
                await message.channel.send(embed = LAB_3)
            else:
                await message.channel.send("Nie potrafie ci pomóc")
        except:
            print("")
    elif(message.content.lower() == "co dzisiaj?" or message.content.lower() == "co dziś?"):
        try:
            getData(1)
            if ("Laby 1" in str(message.author.roles)):
                await message.channel.send(embed = LAB_1)
            elif ("Laby 2" in str(message.author.roles)):
                await message.channel.send(embed = LAB_2)
            elif("Laby 3" in str(message.author.roles)):
                await message.channel.send(embed = LAB_3)
            else:
                await message.channel.send("Nie potrafie ci pomóc")
        except:
            print("")
    elif("Co w" in message.content and "?" in message.content.lower()):
        for i in range(len(dayz)):
            if dayz[i] in message.content.lower():
                try:
                    getData(dayz[i])
                    if   ("Laby 1" in str(message.author.roles)):
                        await message.channel.send(embed = LAB_1)
                    elif ("Laby 2" in str(message.author.roles)):
                        await message.channel.send(embed = LAB_2)
                    elif ("Laby 3" in str(message.author.roles)):
                        await message.channel.send(embed = LAB_3)
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
    else:
        for i in pics:
            if i in message.content.lower():
                emoji = discord.utils.get(client.emojis, name='szacun')
                await message.add_reaction(emoji)
                await message.channel.send(file = discord.File(pics[i]))
        for i in eegs:
            if i in message.content.lower():
                await message.channel.send(eegs[i])

#Unikalny identyfikator autoryzacyjny Dla API discorda
client.run("Prywatny Token")
