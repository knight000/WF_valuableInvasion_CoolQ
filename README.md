# WF_valuableInvasion_CoolQ
> Warframe高价值入侵提醒机器人(曾经)
>
> 现在多了各种各样的新功能

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

指令的前缀是#，指令之间请用**空格**隔开，例如`#添加物品 狙击特昂 破坏者 蓝图`  

| 指令                                   | 效果                                                         |
| -------------------------------------- | ------------------------------------------------------------ |
| 'add', '添加物品'                      | 把物品添加进已获取物品                                       |
| 'del', '删除物品'                      | 把物品从已获取物品中删除                                     |
| 'item', '查看列表'                     | 查看已添加物品                                               |
| 'check'                                | 检查当前有无高价值入侵，因为插件可能卡住                     |
| 'invasion', '入侵'                     | 查看当前全部入侵                                             |
| 'voidtrader', '虚空商人', 'baro'       | 查看当前虚空商人信息                                         |
| 'sortie', '突击'                       | 查看当前突击信息                                             |
| 'fissures', '裂隙', '裂缝', '虚空裂隙' | 查看当前虚空裂隙信息                                         |
| 'arbitration', '仲裁'                  | 查看当前仲裁信息                                             |
| 'sentientoutposts', 'S船', '前哨战'    | 查看S船前哨战信息                                            |
| 'cycle', 'wf时间'                      | 查看地球/希图斯/福尔图娜周期信息                             |
| 'riven', '倾向'                        | 查询紫卡倾向                                                 |
| 'wm', '市场'                           | 获取某样物品的[wm](warframe.market)链接和前五位出家最低的卖家 |

### 提醒示例

>发现高价值入侵：
>节点:Despina (Neptune)，奖励是:[希芙 刀刃]和[德拉 破坏者 枪机]当前进度：50%
>其中[德拉 破坏者 枪机]已拥有
>

### wm查询示例
>#wm ASH PRIME SET  
> ASH PRIME 一套的wm链接为:  
>warframe.market/items/ash_prime_set  
>以下是出价最低的前五位买家：  
>出售者[A1]62.0白金  
>/w A1 Hi! I want to buy: ASH PRIME SET for 62.0 platinum(warframe.market)  
>出售者[B2]64.0白金  
>/w B2 Hi! I want to buy: ASH PRIME SET for 64.0 platinum. (warframe.market)  
>出售者[C3]70.0白金  
>/w C3 Hi! I want to buy: ASH PRIME SET for 70.0 platinum. (warframe.market)  
>出售者[D5]70.0白金  
>/w D5 Hi! I want to buy: ASH PRIME SET for 70.0 platinum. (warframe.market)  
>出售者[E6]70.0白金  
>/w E6 Hi! I want to buy: ASH PRIME SET for 70.0 platinum. (warframe.market)   

### 文件说明

这里是在`awesome/plugins`里的文件说明，理论上可以直接放进其他已经配置好的nonebot使用  

| 文件                                                  | 说明                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| WFInvasionforNoneBot.py                               | 获取高价值入侵并5分钟推送一次                                |
| WFIsaveforNoneBot.py                                  | 储存/更改已获得列表                                          |
| WFAlertingforNoneBot.py                               | 实时信息模块，可单独使用                                     |
| WarframeMarketforNoneBot                              | wm查询模块，可单独使用                                       |
| WF_Dict/WF_Invasion/WF_Modifier/WF_Riven/WF_Sale.json | 翻译文件，来自[WFA_Lexicon](https://github.com/Richasy/WFA_Lexicon) |
| data.list                                             | 储存已获得物品的文件                                         |

### 备注

时不时会有插件卡住的情况…也没想到办法解决，不过仅仅是自动提醒高价值入侵的模块出问题，其他倒是正常能用..

其实已经有别人写好很完善的插件https://github.com/TRKS-Team/WFBot  

所以这个项目好像也没什么必要了，就想起什么的时候就更新一下吧:D

