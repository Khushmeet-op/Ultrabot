# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ Commands Available -

• `{i}promote <reply to user/userid/username>`
    Promote the user in the chat.

• `{i}demote <reply to user/userid/username>`
    Demote the user in the chat.

• `{i}ban <reply to user/userid/username> <reason>`
    Ban the user from the chat.

• `{i}unban <reply to user/userid/username> <reason>`
    Unban the user from the chat.

• `{i}kick <reply to user/userid/username> <reason>`
    Kick the user from the chat.

• `{i}pin <reply to message>`
    Pin the message in the chat.

• `{i}unpin (all) <reply to message>`
    Unpin the message(s) in the chat.

• `{i}dpin <reply to message>`
    Pin the message in the chat Silently.

• `{i}dunpin (all) <reply to message>`
    Unpin the message(s) in the chat Silently.

• `{i}purge <reply to message>`
    Purge all messages from the replied message.

• `{i}purgeall <reply to msg/input>`
    Delete all msgs of replied user.
    Delete all msgs of input user

• `{i}del <reply to message>`
    Delete the replied message.

• `{i}edit <new message>`
    Edit your last message.
"""

import asyncio

from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

from . import *


@ultroid_cmd(
    pattern="promote ?(.*)",
    groups_only=True,
)
async def prmte(ult):
    xx = await eor(ult, "`Processing...`")
    chat = await ult.get_chat()
    isAdmin = chat.admin_rights
    isCreator = chat.creator
    if not isAdmin and not isCreator:
        return await xx.edit("`Hmm, I'm not an admin here...`")
    await xx.edit("`Promoting...`")
    user, rank = await get_user_info(ult)
    if not rank:
        rank = "Admin"
    if not user:
        return await xx.edit("`Reply to a user to promote him!`")
    try:
        await ultroid_bot(
            EditAdminRequest(
                ult.chat_id,
                user.id,
                ChatAdminRights(
                    add_admins=False,
                    invite_users=True,
                    change_info=False,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True,
                ),
                rank,
            )
        )
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `is now an admin in {ult.chat.title} with title {rank}.`"
        )
    except BadRequestError:
        return await xx.edit("`I don't have the right to promote you.`")
    await asyncio.sleep(5)
    await xx.delete()


@ultroid_cmd(
    pattern="demote ?(.*)",
    groups_only=True,
)
async def dmote(ult):
    xx = await eor(ult, "`Processing...`")
    chat = await ult.get_chat()
    isAdmin = chat.admin_rights
    isCreator = chat.creator
    if not isAdmin and not isCreator:
        return await xx.edit("`Hmm, I'm not an admin here...`")
    await xx.edit("`Demoting...`")
    user, rank = await get_user_info(ult)
    if not rank:
        rank = "Not Admin"
    if not user:
        return await xx.edit("`Reply to a user to demote him!`")
    try:
        await ultroid_bot(
            EditAdminRequest(
                ult.chat_id,
                user.id,
                ChatAdminRights(
                    add_admins=None,
                    invite_users=None,
                    change_info=None,
                    ban_users=None,
                    delete_messages=None,
                    pin_messages=None,
                ),
                rank,
            )
        )
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `is no longer an admin in {ult.chat.title}`"
        )
    except BadRequestError:
        return await xx.edit("`I don't have the right to demote you.`")
    await asyncio.sleep(5)
    await xx.delete()


@ultroid_cmd(
    pattern="ban ?(.*)",
    groups_only=True,
)
async def bban(ult):
    xx = await eor(ult, "`Processing...`")
    chat = await ult.get_chat()
    isAdmin = chat.admin_rights
    isCreator = chat.creator
    if not isAdmin and not isCreator:
        return await xx.edit("`Hmm, I'm not an admin here...`")
    user, reason = await get_user_info(ult)
    if not user:
        return await xx.edit("`Reply to a user or give username to ban him!`")
    await xx.edit("`Getting user info...`")
    try:
        await ultroid_bot(
            EditBannedRequest(
                ult.chat_id,
                user.id,
                ChatBannedRights(
                    until_date=None,
                    view_messages=True,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    embed_links=True,
                ),
            )
        )
    except BadRequestError:
        return await xx.edit("`I don't have the right to ban a user.`")
    except UserIdInvalidError:
        await xx.edit("`I couldn't get who he is!`")
    try:
        reply = await ult.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **was banned by** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **in** `{ult.chat.title}`\n**Reason**: `{reason}`\n**Messages Deleted**: `False`"
        )
    if reason:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **was banned by** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **in** `{ult.chat.title}`\n**Reason**: `{reason}`"
        )
    else:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **was banned by** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **in** `{ult.chat.title}`"
        )


@ultroid_cmd(
    pattern="unban ?(.*)",
    groups_only=True,
)
async def uunban(ult):
    xx = await eor(ult, "`Processing...`")
    chat = await ult.get_chat()
    isAdmin = chat.admin_rights
    isCreator = chat.creator
    if not isAdmin and not isCreator:
        return await xx.edit("`Hmm, I'm not an admin here...`")
    user, reason = await get_user_info(ult)
    if not user:
        return await xx.edit("`Reply to a user or give username to unban him!`")
    await xx.edit("`Getting user info...`")
    try:
        await ultroid_bot(
            EditBannedRequest(
                ult.chat_id,
                user.id,
                ChatBannedRights(
                    until_date=None,
                    view_messages=None,
                    send_messages=None,
                    send_media=None,
                    send_stickers=None,
                    send_gifs=None,
                    send_games=None,
                    send_inline=None,
                    embed_links=None,
                ),
            )
        )
    except BadRequestError:
        return await xx.edit("`I don't have the right to unban a user.`")
    except UserIdInvalidError:
        await xx.edit("`I couldn't get who he is!`")
    if reason:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **was unbanned by** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **in** `{ult.chat.title}`\n**Reason**: `{reason}`"
        )
    else:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **was unbanned by** [{OWNER_NAME}](tg://user?id={OWNER_ID}) **in** `{ult.chat.title}`"
        )


@ultroid_cmd(
    pattern="kick ?(.*)",
    groups_only=True,
)
async def kck(ult):
    xx = await eor(ult, "`Processing...`")
    chat = await ult.get_chat()
    isAdmin = chat.admin_rights
    isCreator = chat.creator
    if not isAdmin and not isCreator:
        return await xx.edit("`Hmm, I'm not an admin here...`")
    user, reason = await get_user_info(ult)
    if not user:
        return await xx.edit("`Kick? Whom? I couldn't get his info...`")
    await xx.edit("`Kicking...`")
    try:
        await ultroid_bot.kick_participant(ult.chat_id, user.id)
        await asyncio.sleep(0.5)
    except BadRequestError:
        return await xx.edit("`I don't have the right to kick a user.`")
    except Exception as e:
        return await xx.edit(
            f"`I don't have the right to kick a user.`\n\n**ERROR**:\n`{str(e)}`"
        )
    if reason:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id})` was kicked by` [{OWNER_NAME}](tg://user?id={OWNER_ID}) `in {ult.chat.title}`\n**Reason**: `{reason}`"
        )
    else:
        await xx.edit(
            f"[{user.first_name}](tg://user?id={user.id})` was kicked by` [{OWNER_NAME}](tg://user?id={OWNER_ID}) `in {ult.chat.title}`"
        )


@ultroid_cmd(
    pattern="pin($| (.*))",
)
async def pin(msg):
    x = await eor(msg, "`Wait...`")
    if not msg.is_private:
        # for pin(s) in private messages
        await msg.get_chat()
    cht = await ultroid_bot.get_entity(msg.chat_id)
    xx = msg.reply_to_msg_id
    if not msg.is_reply:
        return await x.edit("`Reply to a message to pin it.`")
    ch = msg.pattern_match.group(1)
    slnt = False
    if ch == "loud":
        slnt = True
    try:
        await ultroid_bot.pin_message(msg.chat_id, xx, notify=slnt)
    except BadRequestError:
        return await x.edit("`Hmm, I'm have no rights here...`")
    except Exception as e:
        return await x.edit(f"**ERROR:**`{str(e)}`")
    await x.edit(f"`Pinned` [this message](https://t.me/c/{cht.id}/{xx})!")

@ultroid_cmd(
    pattern="dpin($| (.*))",
)
async def pin(msg):
    if not msg.is_private:
        # for pin(s) in private messages
        await msg.get_chat()
    cht = await ultroid_bot.get_entity(msg.chat_id)
    xx = msg.reply_to_msg_id
    if not msg.is_reply:
        return await msg.edit("Reply to a message to pin it.")
    ch = msg.pattern_match.group(1)
    slnt = False
    if ch == "loud":
        slnt = True
    try:
        await ultroid_bot.pin_message(msg.chat_id, xx, notify=slnt)
    except BadRequestError:
        return await msg.edit("Hmm, I'm have no rights here...")
    except Exception as e:
        return await msg.edit(f"**ERROR:**{str(e)}")
    await msg.delete()
    
@ultroid_cmd(
    pattern="unpin($| (.*))",
)
async def unp(ult):
    xx = await eor(ult, "`Processing...`")
    if not ult.is_private:
        # for (un)pin(s) in private messages
        await ult.get_chat()
    ch = (ult.pattern_match.group(1)).strip()
    msg = ult.reply_to_msg_id
    if msg and not ch:
        try:
            await ultroid_bot.unpin_message(ult.chat_id, msg)
        except BadRequestError:
            return await xx.edit("`Hmm, I'm have no rights here...`")
        except Exception as e:
            return await xx.edit(f"**ERROR:**\n`{str(e)}`")
    elif ch == "all":
        try:
            await ultroid_bot.unpin_message(ult.chat_id)
        except BadRequestError:
            return await xx.edit("`Hmm, I'm have no rights here...`")
        except Exception as e:
            return await xx.edit(f"**ERROR:**`{str(e)}`")
    else:
        return await xx.edit(f"Either reply to a message, or, use `{hndlr}unpin all`")
    if not msg and ch != "all":
        return await xx.edit(f"Either reply to a message, or, use `{hndlr}unpin all`")
    await xx.edit("`Unpinned!`")

@ultroid_cmd(
    pattern="dunpin($| (.*))",
)
async def unp(ult):
    if not ult.is_private:
        # for (un)pin(s) in private messages
        await ult.get_chat()
    ch = (ult.pattern_match.group(1)).strip()
    msg = ult.reply_to_msg_id
    if msg and not ch:
        try:
            await ultroid_bot.unpin_message(ult.chat_id, msg)
        except BadRequestError:
            return await ult.edit("`Hmm, I'm have no rights here...`")
        except Exception as e:
            return await ult.edit(f"**ERROR:**\n`{str(e)}`")
    elif ch == "all":
        try:
            await ultroid_bot.unpin_message(ult.chat_id)
        except BadRequestError:
            return await ult.edit("`Hmm, I'm have no rights here...`")
        except Exception as e:
            return await ult.edit(f"**ERROR:**`{str(e)}`")
    else:
        return await ult.edit(f"Either reply to a message, or, use `{hndlr}unpin all`")
    if not msg and ch != "all":
        return await ult.edit(f"Either reply to a message, or, use `{hndlr}unpin all`")
    await ult.delete()

@ultroid_cmd(
    pattern="purge$",
)
async def fastpurger(purg):
    chat = await purg.get_input_chat()
    msgs = []
    count = 0
    if not purg.reply_to_msg_id:
        return await eod(purg, "`Reply to a message to purge from.`", time=10)
    async for msg in ultroid_bot.iter_messages(chat, min_id=purg.reply_to_msg_id):
        msgs.append(msg)
        count = count + 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await ultroid_bot.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await ultroid_bot.delete_messages(chat, msgs)
    done = await ultroid_bot.send_message(
        purg.chat_id,
        "__Fast purge complete!__\n**Purged** `" + str(count) + "` **messages.**",
    )
    await asyncio.sleep(5)
    await done.delete()


@ultroid_cmd(
    pattern="purgeall ?(.*)",
)
async def _(e):
    input = e.pattern_match.group(1)
    xx = await eor(e, "`Processing...`")
    if e.reply_to_msg_id:
        input = (await e.get_reply_message()).sender_id
    if input:
        try:
            nos = 0
            async for x in e.client.iter_messages(e.chat_id, from_user=input):
                await e.client.delete_messages(e.chat_id, x)
                nos += 1
            await e.client.send_message(
                e.chat_id, f"**Purged {nos} msgs of {input} from here**"
            )
        except ValueError:
            return await eod(xx, str(er), time=5)
    else:
        return await eod(
            xx,
            "Reply to someone's msg or give their id to delete all msgs from this chat",
            time=10,
        )


@ultroid_cmd(
    pattern="del$",
)
async def delete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except BaseException:
            await eod(
                delme,
                f"Couldn't delete the message.\n\n**ERROR:**\n`{str(e)}`",
                time=10,
            )


@ultroid_cmd(
    pattern="edit",
)
async def editer(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await ultroid_bot.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in ultroid_bot.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=Var.HNDLR)}"})
