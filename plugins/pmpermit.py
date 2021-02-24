# Ultra - UserBot
# Copyright (C) 2020 Ultra
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from pyUltroid.functions.pmpermit_db import *
from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest

from . import *

# ========================= CONSTANTS =============================
COUNT_PM = {}
LASTMSG = {}
PMPIC = "https://telegra.ph/file/40a9824c3ba55ccfae9a0.jpg"
UNAPPROVED_MSG = """
**PMSecurity of {}!**
Please wait for me to respnd or you will be blocked and reported as spam!!

You have {}/{} warnings!"""
WARNS = 3
NO_REPLY = "Reply to someone's msg or try this commmand in private."
PMCMDS = [
    f"{hndlr}a",
    f"{hndlr}approve",
    f"{hndlr}da",
    f"{hndlr}disapprove",
    f"{hndlr}block",
    f"{hndlr}unblock",
]
# =================================================================

sett = udB.get("PMSETTING")
if sett is None:
    sett = True
if sett == "True" and sett != "False":

    @ultroid_bot.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
    async def autoappr(event):
        chat = await event.get_chat()
        mssg = event.text
        if mssg in PMCMDS:  # do not approve if outgoing is a command.
            return
        if not is_approved(chat.id) and chat.id not in COUNT_PM:
            approve_user(chat.id)
            if Var.LOG_CHANNEL:
                name = await event.client.get_entity(chat.id)
                name0 = str(name.first_name)
                await event.client.send_message(
                    Var.LOG_CHANNEL,
                    f"#AutoApproved\nUser - [{name0}](tg://user?id={chat.id})",
                )

    @ultroid_bot.on(events.NewMessage(incoming=True))
    async def permitpm(event):
        if event.is_private:
            user = await event.get_chat()
            if user.bot:
                return
            apprv = is_approved(user.id)
            if not apprv and event.text != UNAPPROVED_MSG:
                try:
                    wrn = COUNT_PM[user.id]
                except KeyError:
                    wrn = 0
                if user.id in LASTMSG:
                    prevmsg = LASTMSG[user.id]
                    if event.text != prevmsg:
                        async for message in event.client.iter_messages(
                            user.id, from_user="me", search=UNAPPROVED_MSG
                        ):
                            await message.delete()
                        await event.client.send_file(
                            user.id,
                            PMPIC,
                            caption=UNAPPROVED_MSG.format(OWNER_NAME, wrn, WARNS),
                        )
                    elif event.text == prevmsg:
                        async for message in event.client.iter_messages(
                            user.id, from_user="me", search=UNAPPROVED_MSG
                        ):
                            await message.delete()
                        await event.client.send_file(
                            user.id,
                            PMPIC,
                            caption=UNAPPROVED_MSG.format(OWNER_NAME, wrn, WARNS),
                        )
                    LASTMSG.update({user.id: event.text})
                else:
                    await event.client.send_file(
                        user.id,
                        PMPIC,
                        caption=UNAPPROVED_MSG.format(OWNER_NAME, wrn, WARNS),
                    )
                    LASTMSG.update({user.id: event.text})
                if user.id not in COUNT_PM:
                    COUNT_PM.update({user.id: 1})
                else:
                    COUNT_PM[user.id] = COUNT_PM[user.id] + 1
                if COUNT_PM[user.id] > WARNS:
                    await event.respond(
                        "`You were spamming my Master's PM, which I didn't like.`\n`You have been BLOCKED and reported as SPAM, until further notice.`"
                    )
                    try:
                        del COUNT_PM[user.id]
                        del LASTMSG[user.id]
                    except KeyError:
                        if Var.LOG_CHANNEL:
                            await event.client.send_message(
                                Var.LOG_CHANNEL,
                                "PMPermit is messed! Pls restart the bot!!",
                            )
                            return LOGS.info("COUNT_PM is messed.")
                    await event.client(BlockRequest(user.id))
                    await event.client(ReportSpamRequest(peer=user.id))
                    if Var.LOG_CHANNEL:
                        name = await event.client.get_entity(user.id)
                        name0 = str(name.first_name)
                        await event.client.send_message(
                            Var.LOG_CHANNEL,
                            f"[{name0}](tg://user?id={user.id}) was blocked for spamming.",
                        )

    @ultroid_cmd(pattern="(a|approve)(?: |$)")
    async def approvepm(apprvpm):
        if apprvpm.reply_to_msg_id:
            reply = await apprvpm.get_reply_message()
            replied_user = await apprvpm.client.get_entity(reply.sender_id)
            aname = replied_user.id
            name0 = str(replied_user.first_name)
            uid = replied_user.id
            if not is_approved(uid):
                approve_user(uid)
                await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `approved to PM!`")
                await asyncio.sleep(3)
                await apprvpm.delete()
            else:
                await apprvpm.edit("`User may already be approved.`")
                await asyncio.sleep(5)
                await apprvpm.delete()
        elif apprvpm.is_private:
            user = await apprvpm.get_chat()
            aname = await apprvpm.client.get_entity(user.id)
            name0 = str(aname.first_name)
            uid = user.id
            if not is_approved(uid):
                approve_user(uid)
                await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `approved to PM!`")
                async for message in apprvpm.client.iter_messages(
                    user.id, from_user="me", search=UNAPPROVED_MSG
                ):
                    await message.delete()
                await asyncio.sleep(3)
                await apprvpm.delete()
                if Var.LOG_CHANNEL:
                    await apprvpm.client.send_message(
                        Var.LOG_CHANNEL,
                        f"#APPROVED\nUser: [{name0}](tg://user?id={uid})",
                    )
            else:
                await apprvpm.edit("`User may already be approved.`")
                await asyncio.sleep(5)
                await apprvpm.delete()
                if Var.LOG_CHANNEL:
                    await apprvpm.client.send_message(
                        Var.LOG_CHANNEL,
                        f"#APPROVED\nUser: [{name0}](tg://user?id={uid})",
                    )
        else:
            await apprvpm.edit(NO_REPLY)

    @ultroid_cmd(pattern="(da|disapprove)(?: |$)")
    async def disapprovepm(e):
        if e.reply_to_msg_id:
            reply = await e.get_reply_message()
            replied_user = await e.client.get_entity(reply.sender_id)
            aname = replied_user.id
            name0 = str(replied_user.first_name)
            if is_approved(replied_user.id):
                disapprove_user(replied_user.id)
                await e.edit(
                    f"[{name0}](tg://user?id={replied_user.id}) `Disaproved to PM!`"
                )
                await asyncio.sleep(5)
                await e.delete()
            else:
                await e.edit(
                    f"[{name0}](tg://user?id={replied_user.id}) was never approved!"
                )
                await asyncio.sleep(5)
                await e.delete()
        elif e.is_private:
            bbb = await e.get_chat()
            aname = await e.client.get_entity(bbb.id)
            name0 = str(aname.first_name)
            if is_approved(bbb.id):
                disapprove_user(bbb.id)
                await e.edit(f"[{name0}](tg://user?id={bbb.id}) `Disaproved to PM!`")
                await asyncio.sleep(5)
                await e.delete()
                if Var.LOG_CHANNEL:
                    await e.client.send_message(
                        Var.LOG_CHANNEL,
                        f"[{name0}](tg://user?id={bbb.id}) was disapproved to PM you.",
                    )
            else:
                await e.edit(f"[{name0}](tg://user?id={bbb.id}) was never approved!")
                await asyncio.sleep(5)
                await e.delete()
        else:
            await e.edit(NO_REPLY)

    @ultroid_cmd(pattern="block$")
    async def blockpm(block):
        if block.reply_to_msg_id:
            reply = await block.get_reply_message()
            replied_user = await block.client.get_entity(reply.sender_id)
            aname = replied_user.id
            name0 = str(replied_user.first_name)
            await block.client(BlockRequest(replied_user.id))
            await block.edit("`You've been blocked!`")
            uid = replied_user.id
        elif block.is_private:
            bbb = await block.get_chat()
            await block.client(BlockRequest(bbb.id))
            aname = await block.client.get_entity(bbb.id)
            await block.edit("`You've been blocked!`")
            name0 = str(aname.first_name)
            uid = bbb.id
        else:
            await block.edit(NO_REPLY)
        try:
            disapprove_user(uid)
        except AttributeError:
            pass
        if Var.LOG_CHANNEL:
            await block.client.send_message(
                Var.LOG_CHANNEL, f"#BLOCKED\nUser: [{name0}](tg://user?id={uid})"
            )

    @ultroid_cmd(pattern="unblock$")
    async def unblockpm(unblock):
        if unblock.reply_to_msg_id:
            reply = await unblock.get_reply_message()
            replied_user = await unblock.client.get_entity(reply.sender_id)
            name0 = str(replied_user.first_name)
            await unblock.client(UnblockRequest(replied_user.id))
            await unblock.edit("`You have been unblocked.`")
        else:
            await unblock.edit(NO_REPLY)
        if Var.LOG_CHANNEL:
            await unblock.client.send_message(
                Var.LOG_CHANNEL,
                f"[{name0}](tg://user?id={replied_user.id}) was unblocked!.",
            )
