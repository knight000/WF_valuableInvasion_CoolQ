# WF_valuableInvasion_CoolQ
> Warframe高价值入侵提醒机器人

基于NoneBot的QQ机器人

## 开始之前

请先阅读[NoneBot](https://nonebot.cqp.moe/)和[CoolQ HTTP API](https://cqhttp.cc/)的说明文档。

## 安装好HTTP-API之后

请确保好已成功安装NoneBot所需要库后，修改`config.py`，把`SUPERUSERS = {}`这一栏填上你的QQ号，就像这样

```python
SUPERUSERS = {123456}
```

然后打开`QQ.txt`，也在里面填上你的Q号

做完这些后，确保HTTP-API已配置完成，正确配置后应显示

```
[20xx-xx-xx xx:xx:xx.xxx] [I] [反向WS] 开启反向 WebSocket 客户端（API）成功，开
始连接 ws://127.0.0.1:[你设置的端口]/ws/api/
[20xx-xx-xx xx:xx:xx.xxx] [I] [反向WS] 开启反向 WebSocket 客户端（Event）成功，
开始连接 ws://127.0.0.1:[你设置的端口]/ws/event/
```

请参考NoneBot的文档，懒人可以直接复制这里给的配置文件。

一切准备就绪后，运行`bot.py`，就完成了。

## 使用

高价值入侵提醒会自动发送到QQ.txt里填写的QQ号里（私聊，仅限一个号），请确保你填写的QQ号和机器人是**QQ好友**。

添加进已获取物品列表的物品会在入侵来的时候有提示，如果两个奖励都是已获取的，则本次入侵不提醒

指令的前缀是**#**，请用**空格**隔开，例如`#添加物品 狙击特昂 破坏者 蓝图`  

| 指令               | 效果                     |
| ------------------ | ------------------------ |
| 'add', '添加物品'  | 把物品添加进已获取物品   |
| 'del', '删除物品'  | 把物品从已获取物品中删除 |
| 'item', '查看列表' | 查看已添加物品           |
| 'invasion', '入侵' | 查看当前全部入侵         |

### 提醒示例

>发现高价值入侵：
>节点:Despina (Neptune)，奖励是:[希芙 刀刃]和[德拉 破坏者 枪机]当前进度：50%
>其中[德拉 破坏者 枪机]已拥有

### 文件说明

这里是在`awesome/plugins`里的文件说明  

| 文件                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| WFInvasionforNoneBot.py    | 获取高价值入侵并5分钟推送一次                                |
| WFIsaveforNoneBot.py       | 储存/更改已获得列表                                          |
| WFGetInvasionforNoneBot.py | 输入查看当前全部入侵，可单独使用                             |
| WF_Dict.json               | 翻译文件，来自[WFA_Lexicon](https://github.com/Richasy/WFA_Lexicon) |
| data.list                  | 储存已获得物品的文件                                         |

