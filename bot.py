import sys
import random 
import urllib.request
import time, datetime
import os, queue
import asyncio
import discord
import youtube_dl
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

import wave
import threading
import shutil
import socket; import urllib; import re

import http.server
from django.shortcuts import render
from django.http import HttpResponse



import modules.hitomi
import modules.https


from discord import utils
from discord.game import Game
from discord.object import Object
from discord.enums import ChannelType
from discord.voice_client import VoiceClient
from discord.ext.commands.bot import _get_variable

import _Music
import _Nsfw
import _Utility
import _Fun

import Load_setting

import speech_recognition as sr

#세팅 불러오기####################################
BOT_TOKEN = Load_setting.data["bot"][0]["token"]
prefix = Load_setting.data["bot"][1]["prefix"]
lang = Load_setting.lang["lang"]
##################################################

client = discord.Client()
playlist = queue.Queue()
playtime = time.time()
playlist.put("start")
playlist_json_val=''

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

class VoiceEntry:

    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '| {0.title} | {1.display_name}  '
        duration = self.player.duration
        if duration:
            fmt = fmt + ' ``[{0[0]}:{0[1]}/{1[0]}:{1[1]}]``'.format(divmod(round(time.time()-playtime), 60), divmod(duration, 60))


        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            playlist.get_nowait()
            self.current = await self.songs.get()
            embed = discord.Embed(color=0x12fe05)
            embed.set_thumbnail(url="https://lh5.googleusercontent.com/ulXZx4YUbQ00yKNOUh5GqhZe2Ta-3HMb3fpdQ5Lg6ZE15apd3zvcWgh3PSCgpEjbnPc-HG8B29xTQur5YFIz=w853-h947-rw")
            playtime = time.time()
            embed.add_field(name=':small_blue_diamond: '+lang[0]['playing'], value=str(self.current), inline=True)
            await self.bot.send_message(self.current.channel, embed=embed)

            self.current.player.start()

            await self.play_next_song.wait()

#명령어 함수###################################
class Music:
    """음성채팅에 관한 명령어 입니다.
    """

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def on_voice_state_update(self, ctx):
        await self.bot.send_message(ctx.message.channel, discord.VoiceClient.poll_voice_ws(self).gi_frame)
        #msg=await self.bot.send_message(ctx.message.channel, "음성인식 시작")
        #with sr.Microphone() as source:
        #    r = sr.Recognizer()
        #    audio = r.listen(source)
        #    command = r.recognize_google(audio)
        #    await self.bot.edit_message(msg, command)

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel: discord.Channel):
        """음성채널에 원격소환합니다. !join (채널코드)"""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say(':small_blue_diamond: '+lang[1]['join']['is_channal'])
        except discord.InvalidArgument:
            await self.bot.say(':small_blue_diamond: '+lang[1]['join']['not_channal'])
        else:
            await self.bot.say(':small_blue_diamond: '+lang[1]['join']['success'] + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """봇을 자신이 있는 음성챗으로 소환합니다."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say(lang[1]['summon']['no_target'])
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def eval(self, ctx, *,code):
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
    async def play(self, ctx, *, song: str):
        """음악을 신청합니다.
        !play (유튜브,사운드클라우드 링크/유튜브 검색어)
        이외 직접 호스팅한 mp3,mp4 파일도 재생 가능합니다.
        """

        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
            'speed': 100,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next,
                                                          before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ")
        except Exception as e:
            fmt = ':small_orange_diamond: '+lang[1]['play']['RD_ERROR']+' ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:


            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)

            await self.bot.say(':small_blue_diamond: '+lang[1]['play']['list_append'] + str(entry))

            await state.songs.put(entry)
            playlist.put(entry)
            playtime = time.time()
            if player.is_live == True:
                await self.bot.say(
                    ':small_orange_diamond: ' + player.title + lang[1]['play']['is_live'])

            #self.bot.loop.create_task(_Utility.Utility.ly(str(entry)))

    @commands.command(pass_context=True, no_pm=True)
    async def rplay(self, ctx):

        """autoplay.txt에 있는 곡을 랜덤으로 재생합니다."""
        await self.bot.say(':small_blue_diamond: '+lang[1]['rplay']['pick_song'])
        f = open("autoplay.txt", 'r')
        urls = f.readlines()
        rn = random.randrange(0, len(urls))
        song = urls[rn]
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next,
                                                          before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        except Exception as e:
            fmt = ':small_orange_diamond: '+lang[1]['rplay']['RD_ERROR']+' ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say(':small_blue_diamond: '+lang[1]['rplay']['list_append'] + str(entry))
            await state.songs.put(entry)
            if player.is_live == True:
                await self.bot.say(
                    ':small_orange_diamond: ' + player.title + lang[1]['rplay']['is_live'])
        f.close()

    @commands.command(pass_context=True, no_pm=True)
    async def rpadd(self, ctx, *, song: str):
        """autoplay.txt에 곡을 추가합니다 (한번에 여러개 가능)"""
        txtf = 'autoplay.txt'
        f = open(txtf, 'a')
        f.write("\n" + song)
        await self.bot.say(':small_blue_diamond: ' + song + lang[1]['rpadd']['add'])
        print(song + ' add in ' + txtf)
        f.close()

    @asyncio.coroutine
    async def autoplay_Task(bot, self, ctx: str, *, ch1: discord.Channel):
        while (True):
            if state.current is None:
                self.bot = bot
                f = open("autoplay.txt", 'r')
                urls = f.readlines()
                rn = random.randrange(0, len(urls))
                song = urls[rn]
                state = self.get_voice_state(ctx.message.server)
                opts = {
                    'default_search': 'auto',
                    'quiet': True,
                }

                if state.voice is None:
                    try:
                        await self.create_voice_client(ch1)
                    except discord.ClientException:
                        await self.bot.say(':small_blue_diamond: 이미 채널에 있습니다.')
                    except discord.InvalidArgument:
                        await self.bot.say(':small_blue_diamond: 음성채널이 아니거나 없습니다. ')
                    else:
                        await self.bot.say(':small_blue_diamond: 완료 >_< : ' + ch1.name)

                try:
                    player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next,
                                                                  before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -filter:v "setpts=0.5*PTS"')
                except Exception as e:
                    fmt = ':small_orange_diamond: 요청 처리중 오류발생! ㅜ.ㅜ ```py\n{}: {}\n```'
                    await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
                else:
                    player.volume = 0.6
                    entry = VoiceEntry(ctx.message, player)
                    await state.songs.put(entry)
                    state.current.requester = "BOT"
                    if player.is_live == True:
                        await self.bot.say(
                            ':small_orange_diamond: ' + player.title + '\n현재자동재생중인 영상은 실시간 스트리밍입니다\n가끔 버퍼링으로 재생이 지연될수 있습니다!')

    @commands.command(pass_context=True, no_pm=True)
    async def des(self, ctx):
        """현재 재생중인 음악의 설명을 봅니다"""

        state = self.get_voice_state(ctx.message.server)
        player = state.player
        await self.bot.say(':small_blue_diamond: '+lang[1]['des']['print']+' \n```{}```'.format(player.description))

    @commands.command(pass_context=True, no_pm=True)
    async def link(self, ctx):
        """현재 재생중인 음악의 링크를 출력합니다."""

        state = self.get_voice_state(ctx.message.server)
        player = state.player
        if player.is_live == False:
            await self.bot.say(':small_blue_diamond: '+lang[1]['link']['print_link']+' \n``{}``'.format(player.download_url))
        else:
            await self.bot.say(':small_orange_diamond: '+lang[1]['link']['is_live'])

    @commands.command(pass_context=True, no_pm=True)
    async def thnail(self, ctx, *, url: str):
        """유튜브 영상의 썸네일을 불러옵니다.
        ?thumnail [영상 일렬번호]
        예) ?thumnail xY3_28MorZE
        """
        await self.bot.say(':small_blue_diamond: '+lang[1]['thnail']['print'])
        url = 'http://img.youtube.com/vi/' + url + '/0.jpg'
        name = random.randrange(1, 1000)
        full_name = "tmp_" + str(name) + ".jpg"
        urllib.request.urlretrieve(url, full_name)
        await self.bot.send_file(ctx.message.channel, open(full_name, 'rb'))

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value: int):
        """현재 재생중인 음악의 볼륨을 조절합니다"""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            if value > 100:
                value = 100
            player.volume = value / 100
            await self.bot.say(':small_blue_diamond: '+lang[1]['volume']['set']+' - {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """재생중인 음악을 일시중지 합니다."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """일시중지된 음악을 재생합니다."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """재생을 중지하고 음성채널에서 나가게 합니다.
        대기열도 초기화 됩니다.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)
        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass
            playlist.queue.clear()
            playtime = time.time()

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """음악 스킵을 투표합니다. 곡 신청자가 스킵하면 강제스킵 됩니다.
        3명이 투표하면 스킵됩니다.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say(":small_blue_diamond: "+lang[1]['skip']['not_song'])
            return

        voter = ctx.message.author
        if voter == state.current.requester or state.current.requester == "BOT":
            await self.bot.say(':small_blue_diamond: '+lang[1]['skip']['master_skip'])
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 2:
                await self.bot.say(':small_blue_diamond: '+lang[1]['skip']['not_vote'])
                state.skip()
            else:
                await self.bot.say(':small_blue_diamond: '+lang[1]['skip']['vote']+' [{}/2]'.format(total_votes))
        else:
            await self.bot.say(':small_blue_diamond: '+lang[1]['skip']['already_skip'])

    async def retxt_playlist(self, ctx, playtext):
        await self.bot.edit_message(playtext, ':small_blue_diamond: '+lang[0]['playing']+' - {0} [스킵: {1}/2]'.format(state.current, skip_count))

    @commands.command(pass_context=True, no_pm=True)
    async def playlist(self, ctx):
        """현재 재생리스트 음악 제목/상태를 보여줍니다"""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say(':small_blue_diamond: '+lang[1]['playlist']['no_playlist'])
        else:
            skip_count = len(state.skip_votes)
            #playtext = await self.bot.say(
            #    ':small_blue_diamond: 플레이중 - {0} [스킵: {1}/2]'.format(state.current, skip_count))

            print_playlist = "```md\n"+lang[1]['playlist']['playlist']+"\n"

            #embed = discord.Embed(color=0x3796ff)
            #embed.add_field(name="Playlist", value="", inline=False)
            for i in range(playlist.qsize()):
                # print_playlist += playlist[ctx.message.server.id][i]+"\n"
                if (i == 0):
                    # await self.bot.say("**"+playlist[ctx.message.server.id][i]+"**")
                    state = self.get_voice_state(ctx.message.server)
                    print_playlist += "#"+lang[0]['playing']+" - {0} [SKIP: {1}/2]".format(str(state.current).replace("``","",2), skip_count) + "\n"
                    #embed.add_field(name="**플레이중 - " + playlist[i] + "**", value="", inline=False)
                    # embed.add_field(name=print_playlist, value=' ', inline=False)
                if (i > 0):
                    # await self.bot.say(playlist[ctx.message.server.id][i])
                    print_playlist += "" + str(i) + ". " + str(playlist.queue[i]) + "\n"
                    #embed.add_field(name="``" + str(i) + "``" + playlist[i], value="", inline=False)
                    # embed.add_field(name=' ', value=print_playlist, inline=False)
            print_playlist += "\n```"
            #await self.bot.say(embed=embed)
            await self.bot.say(print_playlist)
###########################################################

#커맨드 추가/로그인########################################
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), description='Made by **KO_KIBA** with **discord.py**')
print("[SETTING] Prefix Setting {"+prefix+"}")

bot.add_cog(Music(bot))
print("[SETTING] ADD Command Script : Music()")
bot.add_cog(_Nsfw.NSFW(bot))
print("[SETTING] ADD Command Script : NSFW()")
bot.add_cog(_Utility.Utility(bot))
print("[SETTING] ADD Command Script : Utility()")
bot.add_cog(_Fun.Fun(bot))
print("[SETTING] ADD Command Script : Fun()")
@bot.event
async def on_ready():
    print('[SETTING] READY..\n')
    print('[SETTING] CHECK Token_{0.id}'.format(bot.user))
    print('로그인--\n{0} (ID: {0.id})'.format(bot.user))
    await bot.change_status(game=Game(name="Running-?help"))


@bot.event
async def on_member_join(member):
    server = member.server
    channel = discord.Channel(server=server, id="366215186866241538")
    fmt = "{0.mention}님 ``{1.name}``에 어서오세요.\n{0.mention}さん ``{1.name}``にようこそ"
    if server.id == '366215186866241536' :
        await bot.send_message(channel, fmt.format(member, server))
    else:
        pass
#web.start()



bot.run(BOT_TOKEN)


print("[BOT] Good Bye")
