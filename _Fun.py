import os,sys,inspect,random,time

import bot

import asyncio
import discord

commands = bot.commands

class Fun:
    """서버관리 등 어드민 명령어부류입니다"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def kick(self, ctx, userName: discord.User):
        try:
            role = discord.utils.get(ctx.message.server.roles)
            for role in ctx.message.author.roles:
                if role.permissions.kick_members == True:
                    await kick(userName)
                    await client.send_message(ctx.message.channel, ":small_blue_diamond: 킥완료 >_<")
                if role.permissions.kick_members == False:
                    await client.send_message(ctx.message.channel, ":small_orange_diamond: 당신은 권한이 없네요 ㅠ")
        except discord.Forbidden:
            await client.send_message(ctx.message.channel, ":small_orange_diamond: 봇이 권한이 없네요~...")
            return
        except discord.HTTPException:
            await client.send_message(ctx.message.channel, ":small_orange_diamond: 킥 실패")
            return

    @commands.command(pass_context=True, no_pm=True)
    async def ban(self, ctx, userName: discord.User):
        try:
            for role in ctx.message.author.roles:
                if role.permissions.ban_members == True:
                    await self.bot.ban(ctx.message.channel.server, userName)
                    await self.bot.send_message(ctx.message.channel, ":small_blue_diamond: 밴완료 >_<")
                if role.permissions.ban_members == False:
                    await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 당신은 권한이 없네요 ㅠ")
        except discord.Forbidden:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 봇이 권한이 없네요~...")
            return
        except discord.HTTPException:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 밴 실패")
            return

    @commands.command(pass_context=True, no_pm=True)
    async def unban(self, ctx, userName: discord.User):
        try:
            for role in ctx.message.author.roles:
                if role.permissions.ban_members == True:
                    await self.bot.unban(ctx.message.channel.server, userName)
                    await self.bot.send_message(ctx.message.channel, ":small_blue_diamond: 언밴완료 >_<")
                if role.permissions.ban_members == False:
                    await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 당신은 권한이 없네요 ㅠ")
        except discord.Forbidden:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 봇이 권한이 없네요~...")
            return
        except discord.HTTPException:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 언밴 실패")
            return

    @commands.command(pass_context=True, no_pm=True)
    async def role(self, ctx, t_role: str, t_name: str):
        """역할 부여 명령어 입니다"""
        try:
            for role in ctx.message.author.roles:
                if role.permissions.manage_roles == True:
                    role = discord.utils.get(ctx.message.server.roles, name=t_role)
                    await self.bot.add_roles(t_name, role)
                if role.permissions.manage_roles == False:
                    await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 당신은 권한이 없네요 ㅠ")
        except discord.Forbidden:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 봇이 권한이 없네요~...")
            return
        except discord.HTTPException:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 부여 실패")
            return

    @commands.command(pass_context=True, no_pm=True)
    async def cmn(self, ctx, user_id="NULL", *, name):
        """유저의 닉네임을 지정합니다"""
        try:
            for role in ctx.message.author.roles:
                if role.permissions.change_nickname == True:
                    if user_id == "NULL" :
                        await self.bot.change_nickname(ctx.message.author, str(name))
                    if user_id != "NULL" :
                        await self.bot.change_nickname(user_id, str(name))
                if change_nickname == False:
                    await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 당신은 권한이 없네요 ㅠ")
        except discord.Forbidden:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 봇이 권한이 없네요~...")
            return
        except discord.HTTPException:
            await self.bot.send_message(ctx.message.channel, ":small_orange_diamond: 지정 실패")
            return
