import requests
import tabulate
import discord
import os
import io
from discord.ext import commands
from discord_slash import SlashCommand

TOKEN = 'ODg2NjAxNzYwNDIzMTc4MjUy.YT3-Ow.hryNyl2xGGsJ8zJHyB4UTj9UN1s'
bot = commands.Bot(command_prefix='/')
slash = SlashCommand(bot, sync_commands=True)

ver_info = """
```
[v0.4.3a]

[!] Обновлено
[*] Добавлена команда /question для справки
[*] Добавлена команда /changelog, которая показывает нововведения и версию
[*] Добаалены команды для модерирования пользователей (скоро появятся модераторы)
[*] Добавлена полная интеграция /слэш/ команд в Discord
[!] Пожалуйста, сообщайте о всех ошибках и недочётах, которые вы найдёте
```
"""

blacklisted_ids = []


# @bot.command(pass_context=True)  # разрешаем передавать агрументы
# async def test(ctx, arg):  # создаем асинхронную фунцию бота
#    await ctx.send(arg)  # отправляем обратно аргумент


@slash.slash(description="Выводит список доступных команд")
async def commandlist(ctx):
    helpEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                              description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
    helpEmbed.add_field(name="`/commandlist`", value="Показывает этот список", inline=False)
    helpEmbed.add_field(name="`/user [ID]`", value="Показывает информацию про пользователя", inline=False)
    helpEmbed.add_field(name="`/getid [username]`", value="Показывает ID пользователя по его имени", inline=False)
    helpEmbed.add_field(name="`/changelog`", value="Показывает информацию о версии и список изменений", inline=False)
    helpEmbed.add_field(name="`/question`", value="Встроенный справочник, показывает ответы на некоторые вопросы",
                        inline=False)
    helpEmbed.add_field(name="`/blacklist`", value="Показывает все ID в черном списке", inline=False)
    helpEmbed.add_field(name="`/add_blacklist`", value="Добавляет новый ID в черный список", inline=False)
    helpEmbed.add_field(name="`/remove_blacklist`", value="Уберает ID из черного списка", inline=False)
    helpEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
    await ctx.send(embed=helpEmbed)


@slash.slash(description="Выводит всю полученную информацию о зарегистрированном пользователе в Roblox")
async def user(ctx, id):
    # TODO: Add send exception messages while bad request.

    RequestedUserId = id

    print('Processing request of author: ' + str(ctx.author.id) + '; SearchedRobloxID: ' + str(id))

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
        prevUsernamesForPost_PTABLE = tabulate.tabulate(prn_usrnms, headers=['#', 'Имя'])
        prevUsernamesForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'
    if not fr_table:
        friendsForPost = "`Этот пользователь не имеет друзей.`"
        friendsForPost_PTABLE = 'Этот пользователь не имеет друзей.'
    else:
        friendsForPost_PTABLE = tabulate.tabulate(fr_table, headers=["#", "Имя", "ID"])
        friendsForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'

    usedAssetsFor_PTABLE = tabulate.tabulate(usedAssets_list,
                                             headers=["#", "Имя актива", "ID актива", "ID типа актива", "Тип актива"])
    usedAssetsForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'

    if not followersTable_list:
        followersTableForPost = "`Этот пользователь не следует ни за одним другим пользователем.`"
        followersTableForPost_PTABLE = 'Этот пользователь не следует ни за одним другим пользователем.'
    else:
        followersTableForPost_PTABLE = tabulate.tabulate(followersTable_list, headers=["#", "Имя", "ID"])
        followersTableForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'
    if not detailedGroupInfo_table:
        groupsForPost = "`Этот пользователь не участвует ни в одной группе.`"
        groupsForPost_PTABLE = "Этот пользователь не участвует ни в одной группе."
    else:
        groupsForPost_PTABLE = tabulate.tabulate(detailedGroupInfo_table,
                                                 headers=["#", "Название группы", "ID группы",
                                                          "Кол-во участников в группе",
                                                          "ID роли " + glob_info['name'],
                                                          "Роль " + glob_info['name'],
                                                          "Значимость " + glob_info['name']])
        groupsForPost = '`Текст слишком большой. Используйте прикрепленный файл для просмотра.`'
    UserInfoPostEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                      description="По запросу пользователя <@" + str(ctx.author.id) + '>',
                                      color=0x00e1ff)
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
        reqfile.write(
            'Предыдущие имена:\n' + prevUsernamesForPost_PTABLE + '\n \nДрузья:\n' + friendsForPost_PTABLE + '\n \nАктивы:\n' + usedAssetsFor_PTABLE + '\n \nПользователи, за которыми следует ' +
            glob_info[
                'name'] + '\n' + followersTableForPost_PTABLE + '\n \nГруппы, в которых участвует пользователь:\n' + groupsForPost_PTABLE)

    if int(id) in blacklisted_ids:
        errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                 description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
        errEmbed.add_field(name="Ошибка", value="Вы не можете искать информацию об этом пользователе", inline=False)
        errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
        await ctx.send(embed=errEmbed)
    else:
        await ctx.send(embed=UserInfoPostEmbed)
        await ctx.send(file=discord.File('request.txt'))
        await ctx.send("https://www.roblox.com/Thumbs/Avatar.ashx?x=700&y=700&username=" + glob_info["name"])

    os.remove("request.txt")

    # print('Предыдущие имена:\n' + prevUsernamesForPost_PTABLE + '\n \nДрузья:\n' + friendsForPost_PTABLE + '\n \nАктивы:\n' + usedAssetsFor_PTABLE + '\n \nПользователи, за которыми следует ' + glob_info['name'] + '\n' + followersTableForPost_PTABLE + '\n \nГруппы, в которых участвует пользователь:\n' + groupsForPost_PTABLE)


@slash.slash(description="Выводит ID пользователя Roblox по его имени")
async def getid(ctx, username):
    name_please = requests.get('https://api.roblox.com/users/get-by-username',
                               params={'username': username}).json()
    embedForGetIdByUsername = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                            description="Запрос пользователя <@" + str(ctx.author.id) + '>',
                                            color=0x00e1ff)
    embedForGetIdByUsername.add_field(name="`Имя:" + str(name_please['Username']) + "`",
                                      value="`ID:" + str(name_please['Id']) + "`", inline=True)
    embedForGetIdByUsername.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")

    if int(name_please['Id']) in blacklisted_ids:
        errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                 description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
        errEmbed.add_field(name="Ошибка", value="Вы не можете искать информацию об этом пользователе", inline=False)
        errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
        await ctx.send(embed=errEmbed)
    else:
        await ctx.send(embed=embedForGetIdByUsername)


@slash.slash(description="Выводит ответ на один из выбранных вопросов")
async def question(ctx, question):
    if str(question) == '1':
        await ctx.send('''
        **Способ I**
            Шаг 1. Перейдите к желаемому профилю на сайте roblox.com
            Шаг 2. Нажмите на строку поиска в вашем браузере, чтобы полностью посмотреть URL 
            Шаг 3. Найдите цифры между users/ и /profile.
            *Пример:*```
            https://roblox.com/users/1/profile/
                                     ^
                                     ID

            ID пользователя из примера: 1 (это профиль Roblox)```
        **Способ II**
            Шаг 1. Напишите в этот канал /getid [Имя профиля]
            Шаг 2. Скопируйте ID, который отослал StibiumBot
        ''')
    elif str(question) == '2':
        await ctx.send(
            'Discord не позволяет отсылать слишком много текста в одном сообщении, чтобы оставаться быстрым, удобным и бесплатным. Пришлось разделить ответ на несколько сообщений и файлов')
    elif str(question) == '3':
        await ctx.send(
            'Скорее всего, это связано с тем, что ваш запрос неправильный. Убедитесь, что вы ввели правильную команду, ID или имя')
    elif str(question) == '4':
        await ctx.send(
            'Да. StibiumBot использует информацию в открытом доступе и собирает в одном месте специально для вас.')
    elif str(question) == '5':
        await ctx.send(
            'Игрок нарушал правила, вел себя непристойно, мешал работе StibiumBot, из за чего был добавлен в черный список. В черный список добавляются игроки, которые мешают работе бота, а не нарушили правила Roblox.')
    else:
        await ctx.send(
            'Такого вопроса не существует :(\n**Варианты вопросов:**\n```[1] Как получить ID игрока?\n[2] Почему информация отсылается в файле?\n[3] Почему бот не отвечает?\n[4] Легальный ли бот?\n[5] Почему я не могу искать игрока?\n\nПишите не вопрос, а его номер: /question 1```')


# TODO: Add group info
# TODO: Add place info

@slash.slash(description="Выводит информацию о версии и список изменений")
async def changelog(ctx):
    clEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                            description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
    clEmbed.add_field(name="Нововведения", value=ver_info, inline=False)
    clEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
    await ctx.send(embed=clEmbed)


@slash.slash(description="Команда для операторов. Добавить пользователя в черный список")
async def add_blacklist(ctx, id):
    if str(ctx.author.id) == "735801783120560159":
        if int(id) in blacklisted_ids:
            errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                     description="По запросу пользователя <@" + str(ctx.author.id) + '>',
                                     color=0x00e1ff)
            errEmbed.add_field(name="Ошибка", value="Этот ID уже находится в черном списке, ничего не было изменено",
                               inline=False)
            errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
            await ctx.send(embed=errEmbed)
        else:
            blacklisted_ids.append(int(id))
            scsEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                     description="По запросу пользователя <@" + str(ctx.author.id) + '>',
                                     color=0x00e1ff)
            scsEmbed.add_field(name="Успех", value="Этот игрок Roblox успешно был добавлен в черный список",
                               inline=False)
            scsEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
            await ctx.send(embed=scsEmbed)
    else:
        errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                 description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
        errEmbed.add_field(name="Ошибка", value="У вас недотаточно прав для использования этой команды!", inline=False)
        errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
        await ctx.send(embed=errEmbed)


@slash.slash(description="Команда для операторов. Посмотреть пользователей в черном списке")
async def blacklist(ctx):
    if str(ctx.author.id) == "735801783120560159":
        scsEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                 description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
        scsEmbed.add_field(name="Успех", value="```" + str(blacklisted_ids) + "```", inline=False)
        scsEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
        await ctx.send(embed=scsEmbed)
    else:
        errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                 description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
        errEmbed.add_field(name="Ошибка", value="У вас недотаточно прав для использования этой команды!", inline=False)
        errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
        await ctx.send(embed=errEmbed)


@slash.slash(description="Команда для операторов. Удалить пользователя из черного списка")
async def remove_blacklist(ctx, id):
    if str(ctx.author.id) == "735801783120560159":
        if not int(id) in blacklisted_ids:
            errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                     description="По запросу пользователя <@" + str(ctx.author.id) + '>',
                                     color=0x00e1ff)
            errEmbed.add_field(name="Ошибка",
                               value="ID, который вы хотели удалить не находится в черном списке, ничего не было изменено",
                               inline=False)
            errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
            await ctx.send(embed=errEmbed)
        else:
            blacklisted_ids.remove(int(id))
            scsEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                     description="По запросу пользователя <@" + str(ctx.author.id) + '>',
                                     color=0x00e1ff)
            scsEmbed.add_field(name="Успех", value="Этот игрок Roblox успешно был удален из черного списка",
                               inline=False)
            scsEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
            await ctx.send(embed=scsEmbed)
    else:
        errEmbed = discord.Embed(title="StibiumBot [A]", url="https://discord.gg/nqkAeaWGcj",
                                 description="По запросу пользователя <@" + str(ctx.author.id) + '>', color=0x00e1ff)
        errEmbed.add_field(name="Ошибка", value="У вас недотаточно прав для использования этой команды!", inline=False)
        errEmbed.set_footer(text="StibiumBot 2021, alpha test, made by KorzForcanyt")
        await ctx.send(embed=errEmbed)


bot.run(TOKEN)
