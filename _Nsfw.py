import os,sys,inspect

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

class NSFW:
    """일반기능 모음입니다."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def hitomi(self, ctx, title: str):
        """alran.xyz (으)로 히토미 동인지를 zip파일로 업로드 합니다
        ex) ?hitomi 901862 """
        await self.bot.say(":small_blue_diamond: 잠시만 기다려 주세요 완벽한 품질을 위해 시간이 오래걸립니다.")
        if __name__ == "__main__":
            index = str(title)
            if not os.path.exists("hitomi"):
                os.makedirs("hitomi")
            if not os.path.exists("hitomi/"+index):
                os.makedirs("hitomi/"+index)

            Hitomi_js = requests \
                .get("https://hitomi.la/galleries/" + index + ".js") \
                .text.replace("var galleryinfo = ", "")
            Hitomi_list = json.loads(Hitomi_js)
            count = 0
            hitomi_dl_text = await self.bot.say("다운 준비중...")
            for data in Hitomi_list:
                name = data["name"]
                print(name + " / " + index)
                print("process " + name + " started")
                await self.bot.edit_message(hitomi_dl_text, "스레드 사용 -> 프로세스 " + name + " 작업시작")
                threading.Thread(target=modules.hitomi.croll, args=[name, index]).start()

            modules.hitomi.zip('./hitomi/'+index, "./hitomi/"+index+'.zip')
            threading.Thread(modules.https.srvhttp(index)).start()

        embed = discord.Embed(color=0x3796ff)
        embed.add_field(name="alran.xyz에 업로드 완료", value="http://www.alran.xyz/cdn/hitomi/"+index+".zip", inline=True)
        embed.set_footer(text="15분뒤 이링크는 사용할수 없습니다./화질이 좋지않거나 깨짐현상이 나타난다면 2~10초후 ?rehitomi [코드] 를 이용해 주세요")
        await self.bot.say(embed=embed)
    @commands.command(pass_context=True, no_pm=True)
    async def rehitomi(self, ctx, title: str):
        """hitomi 명령어 이용시 이미지 상태가 좋지않으면 사용해주세요
        ex) ?hitomi 901862 """
        index = str(title)
        await self.bot.say(":small_blue_diamond: 잠시만 기다려 주세요 약10초정도가 소요됩니다.")
        print("http://www.alran.xyz/cdn/hitomi/" + index + ".zip/ 재업로드시작")
        modules.hitomi.zip('./hitomi/' + index, "./hitomi/" + index + '.zip')
        threading.Thread(modules.https.srvhttp(index)).start()
        print("http://www.alran.xyz/cdn/hitomi/"+index+".zip/ 재업로드완료")
        embed = discord.Embed(color=0xff8737)
        embed.add_field(name="alran.xyz에 재업로드 완료", value="http://www.alran.xyz/cdn/hitomi/" + index + ".zip", inline=True)
        embed.set_footer(text="15분뒤 이링크는 사용할수 없습니다./아직도 상태가 좋지 않다면 5~15초후 다시 이용해주세요 ")
        await self.bot.say(embed=embed)