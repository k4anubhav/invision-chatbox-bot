# INVISON CHATBOX BOT

A Simple wrapper to make bots for Invision [Chatbox](https://invisioncommunity.com/files/file/7465-chatbox-free/) / [Chatbox+](https://invisioncommunity.com/files/file/9342-chatbox/)


### Installations
    pip install git+https://github.com/k4anubhav/invision-chatbox-bot
or

    pip3 install git+https://github.com/k4anubhav/invision-chatbox-bot

### EXAMPLE

```python
import re

from invisionChatbox.clients import BasicClient
from invisionChatbox.context import Context
from invisionChatbox.utils.validators import RegexValidator
from invisionChatbox.utils.decorators import run_in_thread

bot = BasicClient(
    username="someone",
    bot_id=1,
    cookie="cookie here",
    room_id=1,
    csrf_key="csrf key",
    room_name="room name",
    file_room="file_room",
    plp_upload="plp upload key",
    site_domain="example.com",
)


# print message when user use command hello or hi # /hello and /hi if activator is `/`
@bot.command(['hello', 'hi'])
def hello(ctx: Context, data: dict):
    print(ctx.content)


# Reply Thanks, when someone says welcome
@bot.command(is_command=False, validators=[RegexValidator(re.compile(r'welcome', re.IGNORECASE))])
def welcome(ctx: Context, data: dict):
    ctx.reply('Thanks')


# run when someone uses test command, /test if activator is `/`
# using run in threads command sometimes can run twice
@bot.command()
@run_in_thread
def test(ctx: Context, data: dict):
    print(ctx.content)
    print(ctx.clean_content)
    ctx.reply("test passed")
    ctx.reply("test passed", dm=True)


bot.run()
```

### All Contributions are welcome! 

### Fell free to open issue for any query
