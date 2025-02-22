
```python
if message.startswith("抽卡"):
    user = get_user_data(user_id=msg.user_id)
    if not user:
        await chat.send(Message("请先进行注册了！"))
        return
    else:
        number_temp = message.replace("抽卡", "").strip()
        if number_temp and number_temp == "10":
            if user['stone'] < 10:
                await chat.send("圣晶石不足！")
                return
            number = int(number_temp)
        else:
            return
        cards = random_card(number)
        result = MessageSegment.at(user_id=msg.user_id) + "\n"
        feed = 0
        for card in cards:
            if card != "五星狗粮":
                c.execute("SELECT * from cards where user_id = ? and card = ?", (msg.user_id, card))
                current_card = c.fetchone()
                if current_card:
                    c.execute("UPDATE cards SET number = ? WHERE user_id = ?",
                              (current_card[3] + 1, msg.user_id))
                else:
                    c.execute("INSERT INTO cards (user_id, card, level, number) VALUES (?, ?, ?, ?)",
                              (msg.user_id, card, 0, 1))
                result = result + MessageSegment.image(file=f"file:///{DIR}{card}.png")
            else:
                feed = feed + 1
        c.execute("UPDATE users SET stone = ? WHERE user_id = ?", (user['stone'] - 10, msg.user_id))
        conn.commit()
        result = result + MessageSegment.text(f"附赠：五星狗粮 x {feed}\n\n消耗：圣晶石 x 10")
        await chat.send(result)
```