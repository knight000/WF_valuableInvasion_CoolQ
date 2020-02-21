from nonebot import on_command, CommandSession, permission


@on_command('Add', aliases=('add', '添加物品'), permission=permission.SUPERUSER)
async def Add(session: CommandSession):
    data = []
    f = open("awesome\\plugins\\data.list", "r")
    data = f.read()
    ItemList = data.splitlines()
    f.close()
    # 从会话状态（session.state）中获取物品名称（item），如果当前不存在，则询问用户
    session.state['item'] = session.current_arg_text.strip()
    item = session.get('item', prompt='请输入你要添加的物品')
    if item not in ItemList:
        ItemList.append(item)
        ItemList.sort()
        f = open("awesome\\plugins\\data.list", "w")
        for w in ItemList:
            f.write(w+"\n")
        f.close()
        await session.send("已添加["+item+"]")
    else:
        await session.send("此物品已在列表里")
    session.finish()


@on_command('Delete', aliases=('del', '删除物品'), permission=permission.SUPERUSER)
async def Delete(session: CommandSession):
    data = []
    f = open("awesome\\plugins\\data.list", "r")
    data = f.read()
    ItemList = data.splitlines()
    f.close()
    session.state['item'] = session.current_arg_text.strip()
    item = session.get('item', prompt='请输入你要添加的物品')
    if item in ItemList:
        ItemList.remove(item)
        f = open("awesome\\plugins\\data.list", "w")
        for w in ItemList:
            f.write(w+"\n")
        f.close()
        await session.send("已删除["+item+"]")
    else:
        await session.send("此物品不在列表里")
    session.finish()


@on_command('SendItemList', aliases=('item', '查看列表'), permission=permission.SUPERUSER)
async def SendItemList(session: CommandSession):
    f = open("awesome\\plugins\\data.list", "r")
    message = "当前已获取列表：\n"+f.read()
    await session.send(message)
    session.finish()
