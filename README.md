![微信截图_20240827235558](https://github.com/user-attachments/assets/49ae6eec-91a2-4000-92d7-e4219f779579)# SSR抽卡QQ群机器人
边缘骇客编程实验室订单项目。SSR抽卡QQ群机器人基于llonebot协议端框架搭建。通过sqlite3数据库进行用户卡牌数据持久化存储。

## 机器人QQ截图

![微信截图_20240827235558](https://github.com/user-attachments/assets/b9e842a8-dce7-41d3-b500-987d7d7c5ce7)

## NTQQ架构协议端
![image](https://github.com/user-attachments/assets/4b886ca2-32fa-4bf0-aee5-08a16723f8ad)


## 配置文件
```python
F:\上海预醒网络科技有限公司\边缘骇客实验室（完结订单）\QQ机器人SSR抽卡系统\qq机器人排队端\SSR\
```
插件源码
```python
from datetime import datetime
import os
import random

from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment, bot

import sqlite3

# 连接到SQLite数据库（如果不存在，则会自动创建）
# 数据库文件是test.db
# 如果数据库文件与你的Python脚本在同一目录下，你可以直接写文件名，否则需要写绝对路径
conn = sqlite3.connect('data.db')

# 创建一个Cursor
c = conn.cursor()


def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    return result is not None


SSR = []

for filename in os.listdir("SSR"):
    if os.path.isfile(os.path.join("SSR", filename)):
        filename = filename.replace(".png", "")
        SSR.append(filename)

if table_exists(conn, 'users'):
    print("表 'users' 存在。")
else:
    print("表 'users' 不存在。")
    c.execute('''CREATE TABLE IF NOT EXISTS users  
                 (user_id INTEGER, 
                 signtime TEXT NOT NULL,
                 stone INTEGER NOT NULL,
                 active INTEGER NOT NULL,
                 food INTEGER NOT NULL)''')

if table_exists(conn, 'cards'):
    print("表 'cards' 存在。")
else:
    print("表 'cards' 不存在。")
    c.execute('''CREATE TABLE IF NOT EXISTS cards  
                 (user_id INTEGER, 
                 card TEXT NOT NULL,  
                 level INTEGER NOT NULL,
                 number INTEGER NOT NULL)''')

chat = on_message()


def random_card(number):
    cards = []
    for i in range(number):
        if random.random() <= 0.04:
            card = random.choice(SSR)
            cards.append(card)
        else:
            cards.append("五星狗粮")
    return cards


def get_user_data(user_id):
    # now_time = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT * from users where user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        return {"user_id": result[0], "signtime": result[1], "stone": result[2], "active": result[3], "food": result[4]}
    else:
        return False


def get_user_card_data(user_id, card_name):
    c.execute("SELECT * from cards where user_id = ? and card = ?", (user_id, card_name))
    result = c.fetchone()
    if result:
        return {"user_id": result[0], "card": result[1], "level": result[2], "number": result[3]}
    else:
        return False


# 使用 'with' 语句可以确保文件在使用完毕后被正确关闭
with open('config.txt', 'r', encoding='utf-8') as file:
    DIR = file.read()  # 读取整个文件


@chat.handle()
async def test(msg: GroupMessageEvent):
    if msg.group_id != 935149421:
        return
    if msg.is_tome():
        message = str(msg.get_message())
        if message == "帮助":
            result = """大家好，我是ALTER抽卡养成机器人，请@我发送：\n【注册】【激活】【签到】【帮助】\n【抽卡】【成就】【卡包】【数据】\n【喂养 + 卡片名】【查看 + 卡片名】\n即可开始进行运气预测跟仆人养成吧！"""
            await chat.send(MessageSegment.at(user_id=msg.user_id) + result)
        if message == "注册":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                c.execute("INSERT INTO users (user_id, signtime, stone, active, food) VALUES (?, ?, ?, ?, ?)",
                          (msg.user_id, "", 0, 0, 0))
                # 提交事务
                conn.commit()
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "注册成功！")
            else:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "你已经注册了！")

        if message == "激活":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                if user['active'] == 0:
                    c.execute("UPDATE users SET active = ?, stone = ? WHERE user_id = ?",
                              (1, (user['stone'] + 5000), msg.user_id))
                    conn.commit()
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "恭喜你激活成功！得到5000圣晶石！")
                else:
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "你已经激活了！")
        if message == "签到":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                now_time = datetime.now().strftime('%Y-%m-%d')
                if user['signtime'] == now_time:
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "你已经签到了！")
                else:
                    c.execute("UPDATE users SET signtime = ?, stone = ? WHERE user_id = ?",
                              (now_time, (user['stone'] + 300), msg.user_id))
                    conn.commit()
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "签到成功！得到300圣晶石！")

        if message == "数据":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                now_time = datetime.now().strftime('%Y-%m-%d')
                if user['signtime'] == now_time:
                    sign_in = "已签到"
                else:
                    sign_in = "未签到"

                result = MessageSegment.at(
                    user_id=msg.user_id) + f"\n【ID】{user['user_id']}\n【圣晶石】{user['stone']}\n【五星狗粮】{user['food']}\n【签到】{sign_in}"
                await chat.send(result)

        if message == "抽卡":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                if user['stone'] < 10:
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "圣晶石不足！")
                    return
                cards = random_card(10)
                result = MessageSegment.at(user_id=msg.user_id) + "\n"
                food = 0
                for card in cards:
                    if card != "五星狗粮":
                        current_card = get_user_card_data(user_id=msg.user_id, card_name=card)
                        if current_card:
                            c.execute("UPDATE cards SET number = ? WHERE user_id = ? and card = ?",
                                      (current_card["number"] + 1, msg.user_id, card))
                            conn.commit()
                        else:
                            c.execute("INSERT INTO cards (user_id, card, level, number) VALUES (?, ?, ?, ?)",
                                      (msg.user_id, card, 0, 1))
                            conn.commit()
                        result = result + MessageSegment.image(file=f"file:///{DIR}{card}.png")
                    else:
                        food = food + 1
                c.execute("UPDATE users SET stone = ?, food = ? WHERE user_id = ?",
                          (user['stone'] - 10, (food + user['food']), msg.user_id))
                conn.commit()
                result = result + MessageSegment.text(f"【附赠】：五星狗粮 x {food}\n\n【消耗】圣晶石 x 10")
                await chat.send(result)

        # 喂养
        if message.startswith("喂养"):
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                card_name = message.replace("喂养", "").replace("+", "").strip()
                food = user['food']
                current_card = get_user_card_data(user_id=msg.user_id, card_name=card_name)
                if current_card:
                    # 设置增加等级
                    if (current_card['level'] + int(food / 10)) > 120:
                        final_level = 120
                    else:
                        final_level = current_card['level'] + int(food / 10)

                    c.execute("UPDATE cards SET level = ? WHERE user_id = ? and card = ?",
                              (final_level, msg.user_id, current_card['card']))
                    c.execute("UPDATE users SET food = 0 WHERE user_id = ?", (msg.user_id,))
                    conn.commit()
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "喂养成功")
                else:
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "所选卡片未获得或不存在！")

        # 查看
        if message.startswith("查看"):
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                card_name = message.replace("查看", "").replace("+", "").strip()
                current_card = get_user_card_data(user_id=msg.user_id, card_name=card_name)
                if current_card:
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + MessageSegment.image(
                        file=f"file:///{DIR}{current_card['card']}.png") + f"\n【宝具】{current_card['number']} 【等级】{current_card['level']}")
                else:
                    await chat.send(MessageSegment.at(user_id=msg.user_id) + "所选卡片未获得或不存在！")

        if message == "卡包":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                c.execute("SELECT * from cards where user_id = ?", (msg.user_id,))
                cards = c.fetchall()
                result = MessageSegment.at(user_id=msg.user_id) + "当前卡包数据"
                for row in cards:
                    result = result + f"\n{row[1]}({str(row[2])}级) X {str(row[3])}张"
                await chat.send(result)

        if message == "成就":
            user = get_user_data(user_id=msg.user_id)
            if not user:
                await chat.send(MessageSegment.at(user_id=msg.user_id) + "请先进行注册了！")
                return
            else:
                c.execute("SELECT * from cards where user_id = ?", (msg.user_id,))
                cards = c.fetchall()
                full_count = 0
                total_count = 0
                for row in cards:
                    if row[2] == 120:
                        full_count = full_count + 1
                    total_count = total_count + 1
                c.execute("SELECT COUNT(*) FROM cards WHERE user_id = ?", (msg.user_id,))
                count = c.fetchone()[0]
                result = MessageSegment.at(
                    user_id=msg.user_id) + f"\n【ID】{user['user_id']}\n【SSR种类】已集齐{count}种\n【SSR满级】满级{full_count}种\n【SSR全部】总计{total_count}张"
                await chat.send(result)

```
