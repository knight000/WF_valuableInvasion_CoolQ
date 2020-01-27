from nonebot import on_command, CommandSession


def SaveList(data):
    f = open("awesome\\plugins\\data.list", "w")
    for w in data:
        f.write(w+"\n")
    f.close()


def ReadList():
    data = []
    f = open("awesome\\plugins\\data.list", "r")
    data = f.read()
    data = data.splitlines()
    f.close()
    return data


@on_command('Add', aliases=('add', 'WFI添加'))
async def Add(session: CommandSession):
    list1 = ReadList()
    # 从会话状态（session.state）中获取物品名称（item），如果当前不存在，则询问用户
    item = session.get('item', prompt='请输入你要添加的物品')
    if item not in list1:
        list1.append(item)
        SaveList(list1)
        await session.send("已储存")
    else:
        await session.send("此物品已在列表里")


# @Add.args_parser
# async def _(session: CommandSession):
#     # 去掉消息首尾的空白符
#     stripped_arg = session.current_arg_text.strip()

#     if not stripped_arg:
#         # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
#         # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
#         session.pause('物品错误，请重新输入')

#     # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
#     session.state[session.current_key] = stripped_arg


@on_command('Inquire', aliases=('inquire', '查看列表'))
async def Inquire(session: CommandSession):
    f = open("awesome\\plugins\\data.list", "r")
    message = "当前已获取列表：\n"+f.read()
    await session.send(message)
