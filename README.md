# INVISON CHATBOX BOT

A Simple wrapper to make bots for Invision [Chatbox](https://invisioncommunity.com/files/file/7465-chatbox-free/) / [Chatbox+](https://invisioncommunity.com/files/file/9342-chatbox/)


### Installations
    pip install git+https://github.com/k4anubhav/invision-chatbox-bot
or

    pip3 install git+https://github.com/k4anubhav/invision-chatbox-bot

### EXAMPLE
```python
import json
import re

from invisionChatbox.bot import Bot
from invisionChatbox.context import Context
from invisionChatbox.utils.validators import RegexValidator

with open('conf.json', 'r') as f:
    conf = json.load(f)

bot = Bot(**conf)


# print message when user use command hello or hi # /hello and /hi if activator is `/`
@bot.command(['hello', 'hi'])
def hello(message: Context, data: dict):
    print(message.content)


# Reply Thanks, when someone says welcome 
@bot.command(is_command=False, validators=[RegexValidator(re.compile(r'welcome', re.IGNORECASE))])
def welcome(message: Context, data: dict):
    bot.send_message('Thanks')


@bot.command()
def test(message: Context, data: dict):
    print(message.content)
    print(message.clean_content)
    message.reply("test passed")
    message.reply("test passed", dm=True)


bot.run()
```
Config
```json
{
    "cookie": "Cookie here",
    "csrf_key": "csrf_key",
    "file_room": "file_room",
    "plp_upload": "plp_upload",
    "room_id": 1,
    "room_name": "room_name",
    "site_domain": "example.com",
    "username": "SOMEONE"
}
```

### All Contributions are welcome! 
