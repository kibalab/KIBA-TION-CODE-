import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import bot

import asyncio
import discord
import youtube_dl

playlist = []

commands = bot.commands

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class VoiceEntry:
    p_time = 0

    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def play_count(q_time):
        for i in range(q_time):
            time.sleep(1)
            VoiceEntry.p_time = i

    def playlist_del(q_time: int):
        time.sleep(q_time)
        playlist.pop(0)

    def playlist_del_rdy(duration):
        threading.Thread(target=VoiceEntry.playlist_del, args=(duration,)).start()
        threading.Thread(target=VoiceEntry.play_count, args=(duration,)).start()

    def __str__(self):
        fmt = '| {0.title} | {1.display_name}  '
        duration = self.player.duration
        if duration:
            fmt = fmt + ' ``[{0[0]}:{0[1]}/{1[0]}:{1[1]}]``'.format(divmod(VoiceEntry.p_time, 60), divmod(duration, 60))

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
            self.current = await self.songs.get()
            embed = discord.Embed(color=0x12fe05)
            embed.add_field(name=':small_blue_diamond: 플레이중', value=str(self.current), inline=True)
            await self.bot.send_message(self.current.channel, embed=embed)
            self.current.player.start()
            await self.play_next_song.wait()


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
    async def join(self, ctx, *, channel: discord.Channel):
        """음성채널에 원격소환합니다. !join (채널코드)"""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say(':small_blue_diamond: 이미 채널에 있습니다.')
        except discord.InvalidArgument:
            await self.bot.say(':small_blue_diamond: 음성채널이 아니거나 없습니다. ')
        else:
            await self.bot.say(':small_blue_diamond: 완료 >_< : ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """봇을 자신이 있는 음성챗으로 소환합니다."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('님이 음성채널에 없음. 들어가서 하셈')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song: str):
        """음악을 신청합니다.
        !play (유튜브,사운드클라우드 링크/유튜브 검색어)
        이외 직접 호스팅한 mp3,mp4 파일도 재생 가능합니다.
        """

        if "tvple.com" in song:
            await self.bot.say("티비플")
            r = requests.get(song)
            soup = BeautifulSoup(r.text, "html.parser")
            mrs = soup.Xpath('/html/body/main/div[2]/div/section/div/div[1]/div/div[2]/div/div[3]/div[1]/video/source')
            for mr in mrs:
                print(mr['src'])
                song = mr['src']

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
            fmt = ':small_orange_diamond: 요청 처리중 오류발생! ㅜ.ㅜ ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say(':small_blue_diamond: 대기열추가 ' + str(entry))
            await state.songs.put(entry)
            playlist.append(player.title)
            VoiceEntry.playlist_del_rdy(player.duration)
            if player.is_live == True:
                await self.bot.say(
                    ':small_orange_diamond: ' + player.title + '\n이 영상은 실시간 스트리밍입니다\n가끔 버퍼링으로 재생이 지연될수 있습니다!')

    @commands.command(pass_context=True, no_pm=True)
    async def rplay(self, ctx):

        """autoplay.txt에 있는 곡을 랜덤으로 재생합니다."""
        await self.bot.say(':small_blue_diamond: 선곡중입니다. 기다려주세욥!')
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
            fmt = ':small_orange_diamond: 요청 처리중 오류발생! ㅜ.ㅜ ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say(':small_blue_diamond: 대기열추가 ' + str(entry))
            await state.songs.put(entry)
            playlist.append(player.title)
            VoiceEntry.playlist_del_rdy(player.duration)
            if player.is_live == True:
                await self.bot.say(
                    ':small_orange_diamond: ' + player.title + '\n이 영상은 실시간 스트리밍입니다\n가끔 버퍼링으로 재생이 지연될수 있습니다!')
        f.close()

    @commands.command(pass_context=True, no_pm=True)
    async def rpadd(self, ctx, *, song: str):
        """autoplay.txt에 곡을 추가합니다 (한번에 여러개 가능)"""
        txtf = 'autoplay.txt'
        f = open(txtf, 'a')
        f.write("\n" + song)
        await self.bot.say(':small_blue_diamond: ' + song + ' 를 랜덤플레이에 추가하였습니다.')
        print(song + ' add in ' + txtf)
        f.close()

    @commands.command(pass_context=True, no_pm=True)
    async def aplay(self, ctx, *, ch: int):
        """자동플레이 입니다.
        (실행할 음성채널ID를 입력해주세요)"""
        my_music = Music()
        self.bot.loop.create_task(my_music.autoplay_Task(ctx, ch))

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
    async def testplay(self, ctx, *, song: str):
        """음악을 신청합니다.
        !play (유튜브,사운드클라우드 링크/유튜브 검색어)
        이외 직접 호스팅한 mp3,mp4 파일도 재생 가능합니다.
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
            'outtmpl': '/tmp/dump_audio.%(ext)s'
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            with youtube_dl.YoutubeDL(opts) as ydl:
                ydl.download([song])
            player = voice.create_ffmpeg_player('/tmp/dump_audio.webm')
            player.start()
        except Exception as e:
            fmt = ':small_orange_diamond: 요청 처리중 오류발생! ㅜ.ㅜ ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say(':small_blue_diamond: 대기열추가 ' + str(entry))
            await state.songs.put(entry)
            if player.is_live == True:
                await self.bot.say(
                    ':small_orange_diamond: ' + player.title + '\n이 영상은 실시간 스트리밍입니다\n가끔 버퍼링으로 재생이 지연될수 있습니다!')

    @commands.command(pass_context=True, no_pm=True)
    async def des(self, ctx):
        """현재 재생중인 음악의 설명을 봅니다"""

        state = self.get_voice_state(ctx.message.server)
        player = state.player
        await self.bot.say(':small_blue_diamond: 영상/음악 설명 \n```{}```'.format(player.description))

    @commands.command(pass_context=True, no_pm=True)
    async def link(self, ctx):
        """현재 재생중인 음악의 링크를 출력합니다."""

        state = self.get_voice_state(ctx.message.server)
        player = state.player
        if player.is_live == False:
            await self.bot.say(':small_blue_diamond: 영상 다운링크 \n``{}``'.format(player.download_url))
        else:
            await self.bot.say(':small_orange_diamond: 스트리밍 영상 링크는 제공이 제작자에 의해 제한되있습니다.')

    @commands.command(pass_context=True, no_pm=True)
    async def thnail(self, ctx, *, url: str):
        """유튜브 영상의 썸네일을 불러옵니다.
        ?thumnail [영상 일렬번호]
        예) ?thumnail xY3_28MorZE
        """
        await self.bot.say(':small_blue_diamond: 영상 썸네일')
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
            await self.bot.say(':small_blue_diamond: 볼륨 설정 - {:.0%}'.format(player.volume))

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
        playlist = []

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """음악 스킵을 투표합니다. 곡 신청자가 스킵하면 강제스킵 됩니다.
        3명이 투표하면 스킵됩니다.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say(":small_blue_diamond: 스킵할 노래가 없습니다! ('.')")
            return

        voter = ctx.message.author
        if voter == state.current.requester or state.current.requester == "BOT":
            await self.bot.say(':small_blue_diamond: 요청자 권한 건너뛰기 요청')
            state.skip()
            VoiceEntry.playlist_del_rdy(0)
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 2:
                await self.bot.say(':small_blue_diamond: 투표 없이 노래 건너뛰기. ')
                state.skip()
                VoiceEntry.playlist_del_rdy(0)
            else:
                await self.bot.say(':small_blue_diamond: 건너뛰기 투표 요청 [{}/2]'.format(total_votes))
        else:
            await self.bot.say(':small_blue_diamond: 이미 건너뛰기 했습니다. ')

    async def retxt_playlist(self, ctx, playtext):
        await self.bot.edit_message(playtext,
                                    ':small_blue_diamond: 플레이중 - {0} [스킵: {1}/2]'.format(state.current, skip_count))

    @commands.command(pass_context=True, no_pm=True)
    async def playlist(self, ctx):
        """현재 재생리스트 음악 제목/상태를 보여줍니다"""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say(':small_blue_diamond: 플레이중인게 없습니다.. ')
        else:
            skip_count = len(state.skip_votes)
            playtext = await self.bot.say(
                ':small_blue_diamond: 플레이중 - {0} [스킵: {1}/2]'.format(state.current, skip_count))
            # threading.Thread(target=Music.retxt_playlist, args=(self, ctx, playtext)).start()

            print_playlist = "\n"
            # embed = discord.Embed(color=0x3796ff)
            for i in range(len(playlist)):
                # print_playlist += playlist[i]+"\n"
                if (i == 0):
                    # await self.bot.say("**"+playlist[i]+"**")
                    print_playlist += "**플레이중 - " + playlist[i] + "**" + "\n"
                    # embed.add_field(name=print_playlist, value=' ', inline=False)
                if (i > 0):
                    # await self.bot.say(playlist[i])
                    print_playlist += "``" + i + "``" + playlist[i] + "\n"
                    # embed.add_field(name=' ', value=print_playlist, inline=False)
            print_playlist = "\n"
            # await self.bot.say(embed=embed)
            await self.bot.say(print_playlist)
