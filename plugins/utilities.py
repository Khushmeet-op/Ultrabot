# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ Commands Available -

• `{i}kickme`
    Leaves the group in which it is used.

• `{i}calc <equation>`
    A simple calculator.

• `{i}date`
    Show Calender.

• `{i}chatinfo`
    Get full info about the group/chat.

• `{i}listreserved`
    List all usernames (channels/groups) you own.

• `{i}stats`
    See your profile stats.

• `{i}paste`
    Include long text / Reply to text file.

• `{i}hastebin`
    Include long text / Reply to text file.

• `{i}info <username/userid>`
    Reply to someone's msg.

• `{i}invite <username/userid>`
    Add user to the chat.

• `{i}rmbg <reply to pic>`
    Remove background from that picture.

• `{i}telegraph <reply to media/text>`
    Upload media/text to telegraph.

• `{i}json <reply to msg>`
    Get the json encoding of the message.
"""
import asyncio
import calendar
import html
import io
import os
import sys
import time
import traceback
from datetime import datetime as dt

import pytz
import requests
from telegraph import Telegraph
from telegraph import upload_file as uf
from telethon import functions
from telethon.errors.rpcerrorlist import BotInlineDisabledError, BotResponseTimeoutError
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, User
from telethon.utils import get_input_location

# =================================================================#
from . import *

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

# Telegraph Things
telegraph = Telegraph()
telegraph.create_account(short_name="Ultroid")
# ================================================================#


@ultroid_cmd(
    pattern="kickme$",
    groups_only=True,
)
async def leave(ult):
    x = ultroid_bot.me
    name = x.first_name
    await eor(ult, f"`{name} has left this group, bye!!.`")
    await ultroid_bot(LeaveChannelRequest(ult.chat_id))


@ultroid_cmd(
    pattern="date$",
)
async def date(event):
    k = pytz.timezone("Asia/Kolkata")
    m = dt.now(k).month
    y = dt.now(k).year
    d = dt.now(k).strftime("Date - %B %d, %Y\nTime- %H:%M:%S")
    k = calendar.month(y, m)
    ultroid = await eor(event, f"`{k}\n\n{d}`")


@ultroid_cmd(
    pattern="calc",
)
async def _(event):
    x = await eor(event, "...")
    cmd = event.text.split(" ", maxsplit=1)[1]
    event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    wtf = f"print({cmd})"
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(wtf, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "`Something went wrong`"

    final_output = """
**EQUATION**:
`{}`
**SOLUTION**:
`{}`
""".format(
        cmd, evaluation
    )
    await x.edit(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


@ultroid_cmd(
    pattern="chatinfo(?: |$)(.*)",
)
async def info(event):
    ok = await eor(event, "`...`")
    chat = await get_chatinfo(event)
    caption = await fetch_info(chat, event)
    try:
        await ok.edit(caption, parse_mode="html")
    except Exception as e:
        print("Exception:", e)
        await ok.edit(f"`An unexpected error has occurred. {e}`")
        await asyncio.sleep(5)
        await ok.delete()
    return


@ultroid_cmd(
    pattern="listreserved$",
)
async def _(event):
    result = await ultroid_bot(functions.channels.GetAdminedPublicChannelsRequest())
    output_str = ""
    r = result.chats
    for channel_obj in r:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    if not r:
        await eor(event, "`Not username Reserved`")
    else:
        await eor(event, output_str)


@ultroid_cmd(
    pattern="stats$",
)
async def stats(
    event: NewMessage.Event,
) -> None:
    ok = await eor(event, "`Collecting stats...`")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in ultroid_bot.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1

            elif entity.megagroup:
                groups += 1
                if entity.creator or entity.admin_rights:
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1

        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1

        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1

        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time

    full_name = inline_mention(await ultroid_bot.get_me())
    response = f"🔸 **Stats for {full_name}** \n\n"
    response += f"**Private Chats:** {private_chats} \n"
    response += f"**  •• **`Users: {private_chats - bots}` \n"
    response += f"**  •• **`Bots: {bots}` \n"
    response += f"**Groups:** {groups} \n"
    response += f"**Channels:** {broadcast_channels} \n"
    response += f"**Admin in Groups:** {admin_in_groups} \n"
    response += f"**  •• **`Creator: {creator_in_groups}` \n"
    response += f"**  •• **`Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    response += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    response += f"**  •• **`Creator: {creator_in_channels}` \n"
    response += f"**  •• **`Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    response += f"**Unread:** {unread} \n"
    response += f"**Unread Mentions:** {unread_mentions} \n\n"
    response += f"**__It Took:__** {stop_time:.02f}s \n"
    await ok.edit(response)


@ultroid_cmd(
    pattern="paste( (.*)|$)",
)
async def _(event):
    xx = await eor(event, "`...`")
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    if input_str:
        message = input_str
        downloaded_file_name = None
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                "./resources/downloads",
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            try:
                for m in m_list:
                    message += m.decode("UTF-8")
            except BaseException:
                message = "`Include long text / Reply to text file`"
            os.remove(downloaded_file_name)
        else:
            downloaded_file_name = None
            message = previous_message.message
    else:
        downloaded_file_name = None
        message = "`Include long text / Reply to text file`"
    if downloaded_file_name and downloaded_file_name.endswith(".py"):
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
    else:
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
    q = f"paste-{key}"
    try:
        ok = await ultroid_bot.inline_query(Var.BOT_USERNAME, q)
        await ok[0].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
        await xx.delete()
    except BotInlineDisabledError or BotResponseTimeoutError:  # incase the bot doesnt respond
        await xx.edit(reply_text)


@ultroid_cmd(
    pattern="hastebin ?(.*)",
)
async def _(event):
    input_str = event.pattern_match.group(1)
    xx = await eor(event, "`Pasting...`")
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                "./resources/downloads",
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.hastebin <long text to include>`"
    url = "https://hastebin.com/documents"
    r = requests.post(url, data=message).json()
    url = f"https://hastebin.com/{r['key']}"
    await xx.edit("**Pasted to Hastebin** : [Link]({})".format(url))


@ultroid_cmd(
    pattern="info ?(.*)",
)
async def _(event):
    xx = await eor(event, "`Processing...`")
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await xx.edit("Please repl to a user.\nError - " + str(error_i_a))
        return False
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("Last Name not found")
    )
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Need a Profile Picture to check this"
        str(e)
    caption = """<b>Exᴛʀᴀᴄᴛᴇᴅ Dᴀᴛᴀʙᴀsᴇ Fʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ's Dᴀᴛᴀʙᴀsᴇ<b>
    <b>••Tᴇʟᴇɢʀᴀᴍ ID</b>: <code>{}</code>
    <b>••Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ</b>: <a href='tg://user?id={}'>Click Here</a>
    <b>••Fɪʀsᴛ Nᴀᴍᴇ</b>: <code>{}</code>
    <b>••Sᴇᴄᴏɴᴅ Nᴀᴍᴇ</b>: <code>{}</code>
    <b>••Bɪᴏ</b>: <code>{}</code>
    <b>••Dᴄ ID</b>: <code>{}</code>
    <b>••Nᴏ. Oғ PғPs</b> : <code>{}</code>
    <b>••Is Rᴇsᴛʀɪᴄᴛᴇᴅ</b>: <code>{}</code>
    <b>••Vᴇʀɪғɪᴇᴅ</b>: <code>{}</code>
    <b>••Is A Bᴏᴛ</b>: <code>{}</code>
    <b>••Gʀᴏᴜᴘs Iɴ Cᴏᴍᴍᴏɴ</b>: <code>{}</code>
    """.format(
        user_id,
        user_id,
        first_name,
        last_name,
        user_bio,
        dc_id,
        replied_user_profile_photos_count,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats,
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await event.client.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
    )
    await xx.delete()


@ultroid_cmd(
    pattern="invite ?(.*)",
    groups_only=True,
)
async def _(ult):
    xx = await eor(ult, "`Processing...`")
    to_add_users = ult.pattern_match.group(1)
    if not ult.is_channel and ult.is_group:
        for user_id in to_add_users.split(" "):
            try:
                await ultroid_bot(
                    functions.messages.AddChatUserRequest(
                        chat_id=ult.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
                await xx.edit(f"Successfully invited `{user_id}` to `{ult.chat_id}`")
            except Exception as e:
                await xx.edit(str(e))
    else:
        for user_id in to_add_users.split(" "):
            try:
                await ultroid_bot(
                    functions.channels.InviteToChannelRequest(
                        channel=ult.chat_id, users=[user_id]
                    )
                )
                await xx.edit(f"Successfully invited `{user_id}` to `{ult.chat_id}`")
            except Exception as e:
                await xx.edit(str(e))


@ultroid_cmd(
    pattern=r"rmbg ?(.*)",
)
async def rmbg(event):
    RMBG_API = udB.get("RMBG_API")
    xx = await eor(event, "`Processing...`")
    if not RMBG_API:
        return await xx.edit(
            "Get your API key from [here](https://www.remove.bg/) for this plugin to work.",
        )
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        try:
            dl_file = await ultroid_bot.download_media(
                reply_message, TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            return await xx.edit("**ERROR:**\n`{}`".format(str(e)))
        else:
            await xx.edit("`Sending to remove.bg`")
            output_file_name = ReTrieveFile(dl_file)
            os.remove(dl_file)
    elif input_str:
        await xx.edit("`Sending to remove.bg`")
        output_file_name = ReTrieveURL(input_str)
    else:
        await xx.edit(
            f"Use `{Var.HNDLR}rmbg` as reply to a pic to remove its background."
        )
        await asyncio.sleep(5)
        await xx.delete()
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "rmbg-ult.png"
            await ultroid_bot.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
        await xx.edit("`Done.`")
    else:
        await xx.edit(
            "RemoveBG returned an error - \n`{}`".format(
                output_file_name.content.decode("UTF-8")
            ),
        )


@ultroid_cmd(
    pattern="telegraph ?(.*)",
)
async def telegraphcmd(event):
    input_str = event.pattern_match.group(1)
    xx = await eor(event, "`Processing...`")
    if event.reply_to_msg_id:
        getmsg = await event.get_reply_message()
        if getmsg.photo or getmsg.video or getmsg.gif:
            getit = await ultroid_bot.download_media(getmsg)
            try:
                variable = uf(getit)
                os.remove(getit)
                nn = "https://telegra.ph" + variable[0]
                amsg = f"Uploaded to [Telegraph]({nn}) !"
            except Exception as e:
                amsg = f"Error - {e}"
            await xx.edit(amsg)
        elif getmsg.document:
            getit = await ultroid_bot.download_media(getmsg)
            ab = open(getit, "r")
            cd = ab.read()
            ab.close()
            if input_str:
                tcom = input_str
            else:
                tcom = "Ultroid"
            makeit = telegraph.create_page(title=tcom, content=[f"{cd}"])
            war = makeit["url"]
            os.remove(getit)
            await xx.edit(f"Pasted to Telegraph : [Telegraph]({war})")
        elif getmsg.text:
            if input_str:
                tcom = input_str
            else:
                tcom = "Ultroid"
            makeit = telegraph.create_page(title=tcom, content=[f"{getmsg.text}"])
            war = makeit["url"]
            await xx.edit(f"Pasted to Telegraph : [Telegraph]({war})")
        else:
            await xx.edit("Reply to a Media or Text !")
    else:
        await xx.edit("Reply to a Message !")


@ultroid_cmd(pattern="json")
async def _(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    if len(the_real_message) > 4096:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json-ult.txt"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await eor(event, f"```{the_real_message}```")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=Var.HNDLR)}"})
