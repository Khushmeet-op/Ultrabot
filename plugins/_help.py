# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from pyUltroid.dB.database import Var
from support import *
from telethon.errors.rpcerrorlist import BotInlineDisabledError as dis
from telethon.errors.rpcerrorlist import BotMethodInvalidError as bmi
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as rep

from . import *


@ultroid_cmd(
    pattern="help ?(.*)",
)
async def ult(ult):
    plug = ult.pattern_match.group(1)
    tgbot = Var.BOT_USERNAME
    if plug:
        try:
            if plug in HELP:
                output = "**Plugin** - `{}`\n".format(plug)
                for i in HELP[plug]:
                    output += i
                output += "\n© @TheUltroid"
                await eor(ult, output)
            elif plug in CMD_HELP:
                kk = f"Plugin Name-{plug}\n\n✘ Commands Available-\n\n"
                kk += str(CMD_HELP[plug])
                await eor(ult, kk)
            else:
                try:
                    x = f"Plugin Name-{plug}\n\n✘ Commands Available-\n\n"
                    for d in LIST[plug]:
                        x += Var.HNDLR + d
                        x += "\n"
                    await eor(ult, x)
                except BaseException:
                    await eod(ult, f"`{plug}` is not a valid plugin!", time=5)
        except BaseException:
            await eor(ult, "Error 🤔 occured.")
    else:
        try:
            results = await ultroid_bot.inline_query(tgbot, "ultd")
        except rep:
            return await eor(
                ult,
                "`The bot did not respond to the inline query.\nConsider using {}restart`".format(
                    Var.HNDLR
                ),
            )
        except dis:
            return await eor(
                ult, "`Please turn on inline mode for your bot from` @Botfather."
            )
        except bmi:
            return await eor(
                ult,
                f"Hey, \nYou are on Bot Mode. \nBot Mode Users Cant Get Help Directly ... \nInstead Copy Paste The Following in The Chat and Click The Pop Up \n\n `@{tgbot} ultd`",
            )
        await results[0].click(ult.chat_id, reply_to=ult.reply_to_msg_id, hide_via=True)
        await ult.delete()
