import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import bot

import asyncio
import discord

commands = bot.commands

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

class Utility:
    """일반기능 모음입니다."""

    def __init__(self, bot):
        self.bot = bot

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
        embed.add_field(name='아이디', value=ctx.message.server.id, inline=True)
        embed.add_field(name='인원수', value=ctx.message.server.member_count, inline=True)
        embed.add_field(name='주인장', value=ctx.message.server.owner, inline=False)
        embed.add_field(name='역할들(Roles)', value=roles, inline=False)
        embed.set_footer(text="개설 날짜:" + str(ctx.message.server.created_at))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def testplaying(self, ctx):
        await self.bot.say(ctx.message.author.game.name)
        await self.bot.say(dir(ctx.message.author.game._iterator))

    @commands.command(pass_context=True, no_pm=True)
    async def eval(self, ctx, code):
        try:
            await self.bot.say(eval(code))
        except NameError as e:
            await self.bot.say(e)
            await self.bot.say(type(e))
        except IndexError as e:
            await self.bot.say(e)
            await self.bot.say(type(e))
        except Exception as e:
            await self.bot.say(e)
            await self.bot.say(type(e))

    @commands.command(pass_context=True, no_pm=True)
    async def kick(self, ctx, userName: discord.User):
        role = discord.utils.get(ctx.message.server.roles)
        if ctx.message == "MVP" or role.name == "컴플릿팩":
            await kick(userName)

    @commands.command(pass_context=True, no_pm=True)
    async def role(self, ctx, t_role: str, t_name: str):
        """역할 이전 명령어 입니다"""
        role = discord.utils.get(ctx.message.server.roles, name=t_role)

        await self.bot.add_roles(t_name, role)

    @commands.command(pass_context=True, no_pm=True)
    async def r6(self, ctx, name: str):
        """레인보우 식스 시즈 Stats 입니다"""
        url = 'https://r6stats.com/stats/uplay/{0}/casual'
        await self.bot.say(url.format(name))

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
        embed.add_field(name='오퍼', value=a, inline=True)
        embed.add_field(name='주무기', value=b, inline=True)
        embed.add_field(name='보조무기', value=c, inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def ly(self, ctx, a: str, art=""):
        """가사를 출력합니다. ?ly '[제목]' '[아티스트]'
        띄어쓰기가 포함되어있으면 꼭 '' 를 넣어야 합니다.
        아티스트를 모를경우 ? 를 넣어주세요 (않넣으면 가사를 찾을수 없습니다.)
        """

        if art == "?":
            art = ""
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
        await self.bot.say('가사 생성중')
        f1 = open(a.replace(" ", "") + " - " + art + ".txt", 'w', encoding="utf-8")
        f1.write("제목 : " + title + "\n아티스트 : " + artist + "\n\n\n--가사--\n")
        for i in range(len(lines)):
            f1.write(lines[i] + '\n')
        f1.close()
        await self.bot.send_file(ctx.message.channel, a.replace(" ", "") + " - " + art + ".txt")
        f.close()
        os.remove(a.replace(" ", "") + " - " + art + ".txt")
        # os.remove("lyric.json")await client.edit_profile(password=None, avatar=pfp)

    @commands.command(pass_context=True, no_pm=True)
    async def stat(self, ctx):
        """봇 상태를 알려줍니다."""
        servers = list(self.bot.servers)
        modulenames = set(sys.modules) & set(globals())
        allmodules = [sys.modules[name] for name in modulenames]

        a = """**구동시간** {}    **버젼** {}\n"""
        a += """                                              {}\n"""
        a += """**참여서버** {}               \n"""
        a += """**모듈**                      \n"""
        a += """{}\n"""
        a += """*Create by KIBARA*"""
        embed = discord.Embed(color=0x12fe05)
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/340399841882406922/369e94649082cd87bb2a6f98fafd1026.png?size=512")
        embed.add_field(name='키바티온 스텟패널',
                        value=a.format("준비중", "Python 3.6.X", "Bot 7.8", len(servers), list(allmodules)), inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def profile(self, ctx, url: str):
        """프로필사진(아바타)를 변경합니다. (이미지url만 됩니다)"""
        name = random.randrange(1, 1000)
        full_name = str(name) + ".png"
        urllib.request.urlretrieve(url, full_name)
        with open(full_name, 'rb') as f:
            await self.bot.edit_profile(avatar=f.read())

    @commands.command(pass_context=True, no_pm=True)
    async def test(self, ctx, a: str):
        """테스트 명령어 입니다. 뭐가 실행될지"""
        # game = discord.Game(name="Test")
        # await self.bot.change_status(game=Game(name="준비완료"))
        embed = discord.Embed(color=0x12fe05)
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/340399841882406922/369e94649082cd87bb2a6f98fafd1026.png?size=512")
        embed.add_field(name='TEST COMMEND', value=a, inline=True)
        await self.bot.say(embed=embed)
        # role = discord.utils.get(ctx.message.server.roles, name="대기중")
        # await self.bot.say("@"+ctx.message.server.get_member_named(a)+"님 #profile 에 스팀프로필과 레식 닉네임을 남겨주세요")
        # await bot.add_roles(ctx.message.server.get_member_named(a), role.id)

        # await self.bot.send_file(ctx.message.channel, open('test.gif', 'rb'))