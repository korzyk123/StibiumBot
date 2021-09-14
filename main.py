import requests
import tabulate
import discord
import os
import io
from discord.ext import commands

TOKEN = 'ODg2NjAxNzYwNDIzMTc4MjUy.YT3-Ow.hryNyl2xGGsJ8zJHyB4UTj9UN1s'
bot = commands.Bot(command_prefix='/')



# @bot.command(pass_context=True)  # разрешаем передавать агрументы
# async def test(ctx, arg):  # создаем асинхронную фунцию бота
#    await ctx.send(arg)  # отправляем обратно аргумент


@bot.command()
async def commandlist(ctx):
    helpEmbed = discord.Embed(title="StriatumBot [A]",
                              description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
    helpEmbed.add_field(name="`/commandlist`", value="Показывает этот список", inline=False)
    helpEmbed.add_field(name="`/user [ID]`", value="Показывает информацию про пользователя", inline=False)
    helpEmbed.add_field(name="`/getid [username]`", value="Показывает ID пользователя по его имени", inline=False)
    helpEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
    await ctx.send(embed=helpEmbed)


@bot.command()
async def user(ctx, reqrobid):
    RequestedUserId = reqrobid

    print('Processing request of: author: ' + str(ctx.author.id) + '; SearchedRobloxID: ' + str(reqrobid))

    embedProc = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                          description="Запрос пользователя <@" + str(ctx.author.id) + "> обрабатывается...")
    await ctx.send(embed=embedProc)

    glob_info = requests.get('https://users.roblox.com/v1/users/' + RequestedUserId).json()
    friends = requests.get('https://friends.roblox.com/v1/users/' + RequestedUserId + '/friends').json()
    prev_usernames = requests.get('https://users.roblox.com/v1/users/' + RequestedUserId + '/username-history',
                                  params={'limit': '100', 'sortOrder': 'Asc'}).json()
    avatar_info = requests.get('https://avatar.roblox.com/v1/users/' + RequestedUserId + '/avatar').json()
    followers = requests.get('https://friends.roblox.com/v1/users/' + RequestedUserId + '/followers').json()
    detailedGroupInfo = requests.get('https://groups.roblox.com/v2/users/' + RequestedUserId + '/groups/roles').json()

    dataForFile = ""
    fr_table = []
    fr_process = 0
    usr_list = []
    usedAssets_list = []
    followersTable_list = []
    detailedGroupInfo_table = []
    for _ in friends['data']:
        fr_table.append([fr_process + 1, friends['data'][fr_process]['name'], str(friends['data'][fr_process]['id'])])
        fr_process = fr_process + 1
    fr_process = 0
    for _ in prev_usernames['data']:
        usr_list.append(prev_usernames['data'][fr_process]['name'])
        fr_process = fr_process + 1
    fr_process = 0
    for _ in avatar_info['assets']:
        usedAssets_list.append(
            [fr_process + 1, avatar_info['assets'][fr_process]['name'], avatar_info['assets'][fr_process]['id'],
             avatar_info['assets'][fr_process]['assetType']['id'],
             avatar_info['assets'][fr_process]['assetType']['name']])
        fr_process = fr_process + 1
    fr_process = 0
    for _ in followers['data']:
        followersTable_list.append(
            [fr_process + 1, followers['data'][fr_process]['name'], followers['data'][fr_process]['id']])
        fr_process = fr_process + 1
    fr_process = 0
    for _ in detailedGroupInfo['data']:
        detailedGroupInfo_table.append([fr_process + 1, detailedGroupInfo['data'][fr_process]['group']['name'],
                                        detailedGroupInfo['data'][fr_process]['group']['id'],
                                        detailedGroupInfo['data'][fr_process]['group']['memberCount'],
                                        detailedGroupInfo['data'][fr_process]['role']['id'],
                                        detailedGroupInfo['data'][fr_process]['role']['name'],
                                        detailedGroupInfo['data'][fr_process]['role']['rank']])
        fr_process = fr_process + 1
    nameForPost = "`" + glob_info["name"] + "`"
    displayNameForPost = "`" + glob_info["displayName"] + "`"
    idForPost = "`" + str(glob_info["id"]) + "`"
    createdDateForPost = "`" + glob_info["created"] + "`"
    externalAppDisplayNameForPost = "`" + str(glob_info["externalAppDisplayName"]) + "`"
    if glob_info["isBanned"]:
        bannedForPost = "✅ `(да)`"
    elif not glob_info["isBanned"]:
        bannedForPost = "❎ `(нет)`"
    fr_process = 0
    prn_usrnms = []
    for _ in usr_list:
        prn_usrnms.append([fr_process + 1, usr_list[fr_process]])
        fr_process = fr_process + 1
    if not prn_usrnms:
        prevUsernamesForPost = '`Этот пользователь никогда не менял своё имя.`'
        prevUsernamesForPost_PTABLE = 'Этот пользователь никогда не менял своё имя.'
    else:
        prevUsernamesForPost_PTABLE = tabulate.tabulate(prn_usrnms, headers=['#', 'Username'])
        prevUsernamesForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'
    if not fr_table:
        friendsForPost = "`Этот пользователь не имеет друзей.`"
        friendsForPost_PTABLE  = 'Этот пользователь не имеет друзей.'
    else:
        friendsForPost_PTABLE = tabulate.tabulate(fr_table, headers=["#", "Username", "ID"])
        friendsForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'

    usedAssetsFor_PTABLE = tabulate.tabulate(usedAssets_list,
                                          headers=["#", "Asset Name", "Asset ID", "Asset:AssetTypeID", "Asset Type"])
    usedAssetsForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'

    if not followersTable_list:
        followersTableForPost = "`Этот пользователь не следует ни за одним другим пользователем.`"
        followersTableForPost_PTABLE = 'Этот пользователь не следует ни за одним другим пользователем.'
    else:
        followersTableForPost_PTABLE = tabulate.tabulate(followersTable_list, headers=["#", "Username", "ID"])
        followersTableForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'
    if not detailedGroupInfo_table:
        groupsForPost = "`Этот пользователь не участвует ни в одной группе.`"
        groupsForPost_PTABLE = "Этот пользователь не участвует ни в одной группе."
    else:
        groupsForPost_PTABLE = tabulate.tabulate(detailedGroupInfo_table,
                                          headers=["#", "Groups' name", "Groups' ID", "Groups' member count",
                                                   glob_info['name'] + "'s in group role ID",
                                                   glob_info['name'] + "'s in group role name",
                                                   glob_info['name'] + "'s rank in group"])
        groupsForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'
    UserInfoPostEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj", description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
    UserInfoPostEmbed.add_field(name="Имя", value=nameForPost, inline=False)
    UserInfoPostEmbed.add_field(name="Отображаемое имя", value=displayNameForPost, inline=False)
    UserInfoPostEmbed.add_field(name="ID", value=idForPost, inline=False)
    UserInfoPostEmbed.add_field(name="Дата создания", value=createdDateForPost, inline=False)
    UserInfoPostEmbed.add_field(name="externalAppDisplayName", value=externalAppDisplayNameForPost, inline=False)
    UserInfoPostEmbed.add_field(name="Забанен", value=bannedForPost, inline=False)
    UserInfoPostEmbed.add_field(name="Предыдущие имена", value=prevUsernamesForPost, inline=False)
    UserInfoPostEmbed.add_field(name="Друзья", value=friendsForPost, inline=False)
    UserInfoPostEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")

    UserInfoPostEmbed.add_field(name="Активы пользоваетеля", value=usedAssetsForPost, inline=False)
    UserInfoPostEmbed.add_field(name="Пользователи, за которыми следует " + nameForPost, value=followersTableForPost,
                    inline=False)
    UserInfoPostEmbed.add_field(name="Группы в которых участвует пользователь", value=groupsForPost, inline=False)

    with io.open("request.txt", "w", encoding="utf-8") as reqfile:
        reqfile.write('Предыдущие имена:\n' + prevUsernamesForPost_PTABLE + '\n \nДрузья:\n' + friendsForPost_PTABLE + '\n \nАктивы:\n' + usedAssetsFor_PTABLE + '\n \nПользователи, за которыми следует ' + glob_info['name'] + '\n' + followersTableForPost_PTABLE + '\n \nГруппы, в которых участвует пользователь:\n' + groupsForPost_PTABLE)

    await ctx.send(embed=UserInfoPostEmbed)
    await ctx.send(file=discord.File('request.txt'))
    await ctx.send("https://www.roblox.com/Thumbs/Avatar.ashx?x=700&y=700&username=" + glob_info["name"])

    os.remove("request.txt")

    #print('Предыдущие имена:\n' + prevUsernamesForPost_PTABLE + '\n \nДрузья:\n' + friendsForPost_PTABLE + '\n \nАктивы:\n' + usedAssetsFor_PTABLE + '\n \nПользователи, за которыми следует ' + glob_info['name'] + '\n' + followersTableForPost_PTABLE + '\n \nГруппы, в которых участвует пользователь:\n' + groupsForPost_PTABLE)

@bot.command()
async def getid(ctx, username):
    name_please = requests.get('https://api.roblox.com/users/get-by-username',
                                  params={'username': username}).json()
    embedForGetIdByUsername = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                          description="Запрос пользователя <@" + str(ctx.author.id) + '>', color=0x00fbff)
    embedForGetIdByUsername.add_field(name="`Имя:" + str(name_please['Username']) + "`", value="`ID:" + str(name_please['Id']) + "`", inline=True)
    embedForGetIdByUsername.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
    await ctx.send(embed=embedForGetIdByUsername)


bot.run(TOKEN)
