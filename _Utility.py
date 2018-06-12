import os,sys,inspect,random,time
import datetime
import random
from bs4 import BeautifulSoup
import requests

import bot
import Load_setting
import modules.r6oper

import asyncio
import discord

import threading

from Naked.toolshed.shell import execute_rb
import r6sapi as api
import json

#세팅 불러오기####################################
commands = bot.commands
lang = Load_setting.lang["lang"]
##################################################

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

procs = []


class Utility:
    """일반기능 모음입니다."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def lang(self, ctx, language:str):
        Load_setting.langa(language)
        lang = Load_setting.lang["lang"];

    @commands.command(pass_context=True, no_pm=True)
    async def srvinfo(self, ctx):

        roles = '*'
        for role in range(len(ctx.message.server.roles)):
            if (role != 0):
                roles += ctx.message.server.roles[role].name + ","
        roles += '*'

        embed = discord.Embed(color=0x12fe05, title=ctx.message.server.name, description=ctx.message.server.owner.nick)
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        # embed.add_field(name=' ', value=ctx.message.server.owner.nick, inline=False)
        embed.add_field(name='ID', value=ctx.message.server.id, inline=True)
        embed.add_field(name='Members', value=ctx.message.server.member_count, inline=True)
        embed.add_field(name='Owner', value=ctx.message.server.owner, inline=False)
        embed.add_field(name='Authority(Roles)', value=roles, inline=False)
        embed.set_footer(text="Opening date:" + str(ctx.message.server.created_at))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def hic(self, ctx, text:str, n:int):
        say = await self.bot.say(text)
        for i in range(n):
            ra = random.randrange(1, 4)
            if (ra == 1):
                await self.bot.edit_message(say, "*"+text+"*")
            if (ra == 2):
                await self.bot.edit_message(say, "**" + text + "**")
            if (ra == 3):
                await self.bot.edit_message(say, "***" + text + "***")
            if (ra == 4):
                await self.bot.edit_message(say, "``" + text + "``")
            if (ra == 5):
                await self.bot.edit_message(say, "```" + text + "```")
            time.sleep(0.01)




    @commands.command(pass_context=True, no_pm=True)
    async def r6(self, ctx, name: str):
        """레인보우 식스 시즈 Stats 입니다"""
        A_link = 'http://r6db.com'
        driver = webdriver.PhantomJS('F:\\KIBA_TION - 복사본\\phantomjs\\bin\\phantomjs.exe')
        driver.implicitly_wait(2)
        driver.get('http://r6db.com/search/PC/'+name)
        driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div[2]/div/div/div/a').click()
        driver.implicitly_wait(1)
        jsontxt = driver.page_source
        print(jsontxt)
        driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/a[3]').click()
        driver.implicitly_wait(2)
        jsontxt = driver.page_source
        print(jsontxt)
        #req = requests.get('http://r6db.com/search/PC/'+name)
        #html = req.text
        #soup = BeautifulSoup(html, 'html.parser')
        #playerlink = soup.find(class_='playercard')['href']
        #print(playerlink)
        #req = requests.get(playerlink[0].get('href'))
        #html = req.text
        #soup = BeautifulSoup(html, 'html.parser')
        #jsonlink = soup.select('#mount > div > div.app__page > div.page.player.' + playerlink.replace("https://r6db.com/player/", '') + ' > div.page__head > div > div > div > div.playerheader__content > div.playerheader__info > div.playerheader__links > a:nth-child(3)').get('href')
        #req = requests.get(jsonlink)
        #jsontxt = req.text

        data = json.loads(jsontxt)
        embed = discord.Embed(color=0x12fe05)
        embed.add_field(name='이름/레벨(Name/Lv)', value=data['name']+'/'+data['level'], inline=True)
        embed.add_field(name='MMR(Matchmaking Rating)', value=data['rank']['apac']['mmr'], inline=True)
        embed.add_field(name='W/L(Win/Loss)', value=data['rank']['apac']['wins']+'/'+data['rank']['apac']['losses'], inline=True)
        embed.add_field(name='K/D(Kill/Death)',value=int(data['stats']['ranked']['kills'])/int(data['stats']['ranked']['deaths']), inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def r6oper(self, ctx, n: str):
        """레인보우 식스 시즈 렌덤 오퍼 추천기 입니다"""
        img = "https://pbs.twimg.com/profile_images/945079417109385216/l0FfXDZg_400x400.jpg"
        if (n == "d" or n == "D"):
            a, b, c, img = modules.r6oper.defence()
        if (n == "a" or n == "A"):
            a, b, c, img = modules.r6oper.attack()
        if (n != "d" and n != "D" and n != "a" and n != "A"):
            await self.bot.say("누가 장난치래? 어?!")
        embed = discord.Embed(color=0x12fe05)
        embed.set_thumbnail(url=img)
        embed.add_field(name='오퍼(Oper)', value=a, inline=True)
        embed.add_field(name='주무기(Main)', value=b, inline=True)
        embed.add_field(name='보조무기(Sub)', value=c, inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def rdm(self, ctx, a:int, b:int):
        embed = discord.Embed(color=0xccff02)
        embed.add_field(name='Random NUM', value=str(random.randrange(a,b)), inline=True)
        await self.bot.say(embed=embed)
        #await self.bot.say()

    @commands.command(pass_context=True, no_pm=True)
    async def tmm(self, ctx, *, player: str):
        A=[]
        player = player.split(' ')
        random.shuffle(player)
        templelen=int(len(player))/2
        A.append(str(player[int(templelen):]).replace('[','').replace("'",'').replace(',','\n').replace(']','').replace(' ',''))
        A.append(str(player[:int(templelen)]).replace('[','').replace("'",'').replace(',','\n').replace(']','').replace(' ',''))
        if random.choice(A) == A[0]:
            embed = discord.Embed(color=0x04adff)
            embed.add_field(name='Blue TEAM', value=A[1], inline=True)
            #https://lh5.googleusercontent.com/lM-GIyTXP3ZTtolqu9vT7nefG7pepNFkc4PeTdz8tP-UZm7x-X4CiSWArxIJKVP0kP01U7IKl1ycO09gThb9=w1364-h925-rw
            embed.set_thumbnail(url="https://lh5.googleusercontent.com/lM-GIyTXP3ZTtolqu9vT7nefG7pepNFkc4PeTdz8tP-UZm7x-X4CiSWArxIJKVP0kP01U7IKl1ycO09gThb9=w1364-h925-rw")
            await self.bot.say(embed=embed)
            embed = discord.Embed(color=0xff9b04)
            embed.add_field(name='Orange TEAM', value=A[0], inline=True)
            #https://lh4.googleusercontent.com/1mjM4ebLGPGwBPM9nSeOHoBp7yqvxmQmNTQ8nko99AZaI9KB_0ghStmuLZaSbPg5GDgw3GgMfbILWCqHsTqN=w1364-h925-rw
            embed.set_thumbnail(url="https://lh4.googleusercontent.com/1mjM4ebLGPGwBPM9nSeOHoBp7yqvxmQmNTQ8nko99AZaI9KB_0ghStmuLZaSbPg5GDgw3GgMfbILWCqHsTqN=w1364-h925-rw")
            await self.bot.say(embed=embed)

        if random.choice(A) == A[1]:
            embed = discord.Embed(color=0x04adff)
            embed.add_field(name='Blue TEAM', value=A[0], inline=True)
            await self.bot.say(embed=embed)
            embed = discord.Embed(color=0xff9b04)
            embed.add_field(name='Orange TEAM', value=A[1], inline=True)
            await self.bot.say(embed=embed)


    @commands.command(pass_context=True, no_pm=True)
    async def ly(self, ctx, *, a: str, art=""):
        """가사를 출력합니다. ?ly '[제목]' '[아티스트]'
        띄어쓰기가 포함되어있으면 꼭 '' 를 넣어야 합니다.
        아티스트를 모를경우 ? 를 넣어주세요 (않넣으면 가사를 찾을수 없습니다.)
        """
        f = open("simple.rb", 'w', encoding="utf-8")
        data = '''require './modules/alsong.rb'

puts Alsong.get_lyrics("''' + a + '''","''' + art + '''")
        '''
        f.write(data)
        f.close()
        success = execute_rb('simple.rb', '')
        print(success)
        f = open("lyric.json", 'r', encoding="utf-8")
        data = f.read()
        lyric = json.loads(data)

        title = lyric[0]['title']
        artist = lyric[0]['artist']
        lines = [line['text'] for line in lyric[1:]]
        await self.bot.say(lang[1]['ly']['get_ly'])
        f1 = open(a.replace(" ", "+") + "가사.txt", 'w', encoding="utf-8")
        f1.write(lang[1]['ly']['ly_form']['title']+" : " + title + "\n"+lang[1]['ly']['ly_form']['artist']+" : " + artist + "\n\n\n"+lang[1]['ly']['ly_form']['ly']+"\n")
        for i in range(len(lines)):
            f1.write(lines[i] + '\n')
        f1.close()
        await self.bot.send_file(ctx.message.channel, a.replace(" ", "+") + "가사.txt")
        f.close()
        os.remove(a.replace(" ", "+") + "가사.txt")

    @commands.command(pass_context=True, no_pm=True)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await self.bot.say("PONG!!")
        ping = (time.monotonic() - before) * 1000
        await self.bot.edit_message(message, f"응답  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')

    @commands.command(pass_context=True, no_pm=True)
    async def profile(self, ctx, url: str):
        """프로필사진(아바타)를 변경합니다. (개발자만 됩니다)"""
        full_name = "profile" + ".png"
        with open(full_name, 'rb') as f:
            await self.bot.edit_profile(avatar=f.read())

    @commands.command(pass_context=True, no_pm=True)
    async def test(self, ctx, a: str):
        """테스트 명령어 입니다. 뭐가 실행될지"""
        msg = await self.bot.say("test")
        res = await self.bot.wait_for_reaction(['👍', '👎'], message=msg)
        await self.bot.send_message(ctx.message.channel, '{0.user} 반응 {0.reaction.emoji}!'.format(res))