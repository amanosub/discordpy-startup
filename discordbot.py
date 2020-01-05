import sys
import discord
import random
import asyncio
import time
import datetime
import urllib.request
import json
import re
import os
import traceback
import math
from discord.ext import tasks
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')

client = discord.Client()
#TOKEN = os.environ['DISCORD_BOT_TOKEN']
TOKEN = "NjYyOTk5MzU2MDMwNTgyNzg1.XhCIWw.-Nt4qCftYJ1p1vMp10IDsOdN-04"

edit_flag = True

test_ch = None
test_ch_numch = None
test_ch_num = 0
test_flag = True
t_flag = True
yui_ans_msg = None
t_ch = None

@client.event
async def on_ready():
    global t_ch
    t_ch = client.get_channel(662999883892129802)

@tasks.loop(seconds=30)
async def t_loop():
    if t_flag==True:
        t_ch = client.get_channel(662999883892129802)
        tao=client.get_user(526620171658330112)
        if tao:
            def test_check (t_msg):
                if t_msg.author != tao:
                    return 0
                if t_msg.channel!=t_ch:
                    return 0
                return 1

            try:
                t_res=await client.wait_for('message',timeout=10,check = test_check)
            except asyncio.TimeoutError:
                await t_ch.send('::t')
            else:
                pass

@tasks.loop(seconds=30)
async def test_check_loop():
    if test_flag==True:
        tao=client.get_user(526620171658330112)
        if tao:
            def test_check (d_msg):
                if d_msg.author != tao:
                    return 0
                if d_msg.channel!=test_ch:
                    return 0
                return 1

            try:
                t_res=await client.wait_for('message',timeout=30,check = test_check)
            except asyncio.TimeoutError:
                await test_ch.send('::attack とまってない?')
            else:
                pass


@tasks.loop(seconds=60)
async def st_loop():
    await client.change_presence(activity=discord.Game(name="t!help│ここの専属BOTです！"))

@client.event
async def on_ready():

    global t_ch
    t_ch = client.get_channel(662999883892129802)
    #起動時刻（日本時刻）
    dateTime = datetime.now(JST)
    st_loop.start()
    test_check_loop.start()
    t_loop.start()
    await client.change_presence(activity=discord.Game(name="t!help│ここの専属BOTです！"))
    print('◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢')
    print("‣BOT NAME\n '+(client.user.name)")
    print('‣BOT ID\n '+str(client.user.id))
    print('‣LOGIN TIME\n '+str(dateTime.now(JST)))
    print('◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢')
    await t_ch.send("::t start")

@client.event
async def on_message(message):

    if message.content=='t!ping':

        embed=discord.Embed(title='**Ping測定中**')
        msg=await message.channel.send(embed=embed)

        result=(msg.created_at - message.created_at).microseconds // 1000
        await msg.edit(embed=discord.Embed(title=f'**Pong!\n{result}ms**'))




    if message.content == "t!help":
        desc = 't!say [内容]\n```言ったことをオウム返しだよ```'
        desc += "\nt!ping```現在のサクラのping値を測定するよ```"
        desc += "\nt!ch [チャンネルメンション]\n```指定チャンネルで自動で戦うよ```"
        desc += "\nt!stop\n```上のシステムを止めるよ```"
        desc += "\nt!tstart\n```トレーニングをする（はずだ）よ```"
        desc += "\nt!tstop\n```トレーニングを終わらせる（はずだ）よ```"

        embed = discord.Embed(title="BOT取扱説明書",description=f"{desc}",color=discord.Colour.green())
        await message.channel.send(embed=embed)


    me = client.user
    mio = client.get_user(644153226597498890)
    tao = client.get_user(526620171658330112)
    startlog_ch = client.get_channel(663000776179974184)
    stoplog_ch = client.get_channel(663000837848694794)


    if message.embeds and message.embeds[0].description and message.author == tao :
        dateTime = datetime.now()

        if f"{client.user.mention}はレベルアップした！" in message.embeds[0].description:
            lv = message.embeds[0].description.split("`")[1]
            embed = discord.Embed(
                title = "━LvUP━",
                description = f"**__{lv}__**",
                color = discord.Color.blue())
            embed.set_footer(text = datetime.now(JST))
            await asyncio.gather(*(c.send(embed=embed) for c in client.get_all_channels() if c.name == 'botレベルアップログ'))


    global test_ch
    global test_flag
    if message.content.startswith("t!ch "):
        test_ch_m = message.content.split('t!ch ')[1]
        test_ch = discord.utils.get(message.guild.text_channels, mention=test_ch_m)
        embed=discord.Embed(
            title=f"[**testch**]ログ",
            description=f'```使用者　│『{message.author}』\n使用者ID│『{message.author.id}』\n使用ch名│『{message.channel.name}』\n指定ch名│『{test_ch.name}』```チャンネルのメンション\n{test_ch.mention}'
        )
        embed.set_thumbnail(url=message.author.avatar_url)
        await startlog_ch.send(embed=embed)
        embed=discord.Embed(title='Play開始')
        await message.author.send(embed=embed)
        await asyncio.sleep(1)
        test_flag=True
        await test_ch.send("::attack")


    if message.content=='t!stop':
        test_flag=False
        await asyncio.sleep(5)
        await test_ch.send('::re')
        embed=discord.Embed(title='Play停止')
        await message.author.send(embed=embed)

    if message.channel == test_ch and message.embeds and test_flag==True:
        if message.embeds[0].title and 'が待ち構えている' in message.embeds[0].title:
            if test_ch.id == 663001179248394250:
                lv=message.embeds[0].title.split('Lv.')[1].split(' ')[0]
                await test_ch.edit(name=f'┃honpen┃lv{lv}')
            await asyncio.sleep(1)
            await test_ch.send("::attack 先手必勝!!")



    if message.channel==test_ch and test_flag==True:
        if f"{me.display_name}はやられてしまった" in message.content:
            await asyncio.sleep(0.2)
            await test_ch.send('::item e')

        elif f"{me.name}の攻撃" in message.content and f"{me.name}のHP" in message.content and not f"{me.name}はやられてしまった" in message.content:
            await asyncio.sleep(0.2)
            await test_ch.send(f'::attack ')


        elif message.embeds and message.embeds[0].description:
            if 'このチャンネルの全てのPETが全回復した！' in message.embeds[0].description:
                await asyncio.sleep(0.5)
                await test_ch.send('::attack 復活乁( ˙ ω˙乁)')

            elif f"{client.user.mention}はもうやられている！" in message.embeds[0].description:
                await asyncio.sleep(0.5)
                await test_ch.send("::i e 復活！")



    if message.content == "t!t":
        await message.channel.send("::t")

    global t_flag
    t_ch = client.get_channel(662999883892129802)

    me = client.user
    tao = client.get_user(526620171658330112)
    global yui_ans_msg

    if message.content == "t!t":
        await message.channel.send("::t")

    if message.channel == t_ch and message.author == mio:
        if message.embeds:
            if message.embeds[0].footer.text and "TAOのトレーニング" in message.embeds[0].footer.text:
                if not yui_ans_msg == (message.embeds[0].description).split("`")[1]:
                    yui_ans_msg = (message.embeds[0].description).split("`")[1]
                    await t_ch.send(yui_ans_msg)

    if message.content=='t!tstart':
        t_flag=True
        embed = discord.Embed(
        title=f"トレーニング開始\nt_flag = {t_flag}"
        )
        await message.author.send(embed = embed)
    if message.content=='t!tstop' :
        t_flag=False
        embed = discord.Embed(
        title=f"トレーニング終了\nt_flag = {t_flag}"
        )
        await message.author.send(embed = embed)


    if message.content=='t!tstart':
        t_flag=True
        embed = discord.Embed(
        title=f"トレーニング開始\nt_flag = {t_flag}"
        )
        await message.author.send(embed = embed)

    if message.content=='t!tstop' :
        t_flag=False
        embed = discord.Embed(
        title=f"トレーニング終了\nt_flag = {t_flag}"
        )
        await message.author.send(embed = embed)

    if message.content.startswith("t!say "):
        await message.delete()
        await message.channel.send(message.content.split("t!say ")[1])


    if message.content == 't!st':
        await message.channel.send('::status ')

    # 「りせ」と発言したら「::re」が返る処理
    if message.content == 't!re':
        await message.channel.send('::reset')

    if message.content == 't!atk':

        await message.channel.send("::attack")

    if message.content == 't!i e':
        await message.channel.send('::i e')


    if message.content == 't!i f' and message.author_id!=446610711230152706:
            await message.channel.send('::i f')


    if message.content == 't!rmap':
        await message.channel.send('::rmap')

    if message.content.startswith('t!sinka '):
        await message.channel.send('::sinka')
        reaction=message.content.split('t!sinka ')[1]
        def role_check(tao_msg):
            if not tao_msg.embeds:
                return 0
            if tao_msg.channel != message.channel:
                return 0
            return 1

        try:
            ans_msg = await client.wait_for('message', timeout=40, check=role_check)
        except:
            embed = discord.Embed(title='Error!!', description='もう一度試して見てね（￣▽￣;）\nもしかして以下の点が該当してないかな？\n‣TAOからの反応が40秒以内に来なかった\n‣TAOがオフライン\n‣TAOが修理中', color=discord.Color.green())
            await message.channel.send(embed=embed)
        else:
            await asyncio.sleep(5)
            await ans_msg.add_reaction(reaction)
    if message.content.startswith('t!role '):
        role_num = message.content.split('t!role ')[1]
        if not role_num in ["0","1","2","3"]:
            embed = discord.Embed(title='番号エラー!',
                              description=f'{role_num}に該当する役職はないよ!\n**役職番号**\n0│Adventure系\n1│Warrior系\n2│Mage系\n3│Thief系\nコマンドは`y!role [役職番号]`だよ。',
                              color=discord.Color.red())
            embed.set_footer(icon_url={message.author.avater_url},text=f"{message.author.name}")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('::role')

            def role_check(tao_msg):
                if not tao_msg.embeds:
                    return 0
                if tao_msg.channel != message.channel:
                    return 0
                return 1

            try:
                ans_msg = await client.wait_for('message', timeout=40, check=role_check)
            except:
                embed = discord.Embed(title='Error!!', description='もう一度試して見てね（￣▽￣;）\nもしかして以下の点が該当してないかな？\n‣TAOからの反応が40秒以内に来なかった\n‣TAOがオフライン\n‣TAOが修理中', color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                await asyncio.sleep(2)
                if role_num == '0':
                    await ans_msg.add_reaction(f'\u0030\u20e3')
                elif role_num == '1':
                    await ans_msg.add_reaction(f'\u0031\u20e3')
                elif role_num == '2':
                    await ans_msg.add_reaction(f'\u0032\u20e3')
                elif role_num == '3':
                    await ans_msg.add_reaction(f'\u0033\u20e3')

    # 「あいてむ」と発言したら「::i」が返る処理
    if message.content == 't!i':
        await message.channel.send('::i')

    # 「ろぐいん」と発言したら「::login」が返る処理
    if message.content == 't!login':
        await message.channel.send('::login')



@client.event
async def on_message_edit(before,after):
    global edit_flag
    if edit_flag == True:

        if after.channel == t_ch and t_flag == True and after.embeds[0].description and before.embeds != after.embeds:
            edit_flag=False
            if "正解" in after.embeds[0].description:
                await t_ch.send("::t Training")

            if after.embeds and after.embeds[0].description:
                if f"{client.user.mention}はレベルアップした！" in after.embeds[0].description:
                    dateTime = datetime.now(JST)
                    lv = after.embeds[0].description.split("`")[1]
                    embed = discord.Embed(
                        title = "━LvUP━",
                        description = f"**__{lv}__**",
                        color = discord.Color.green())
                    embed.set_footer(text = f"{dateTime.year}年{dateTime.month}月{dateTime.day}日　{dateTime.hour}時{dateTime.minute}分{dateTime.second}秒")
                    \
                    await asyncio.gather(*(c.send(embed=embed) for c in client.get_all_channels() if c.name == 'botレベルアップログ'))


        await asyncio.sleep(0.1)
        edit_flag = True

client.run(TOKEN)
