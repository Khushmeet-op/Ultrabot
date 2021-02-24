# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ Commands Available -

• `{i}superfban <reply to user/userid/username>`
    FBan the person across all feds in which you are admin.

• `{i}superunfban <reply to user/userid/username>`
    Un-FBan the person across all feds in which you are admin.

Specify FBan Group and Feds to exclude in the assistant.
"""

import asyncio
import os

from . import *


@ultroid_cmd(pattern="superfban ?(.*)")
async def _(event):
    msg = await eor(event, "Starting a Mass-FedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await ultroid_bot.download_media(
                previous_message, "fedlist"
            )
            file = open(downloaded_file_name, encoding="utf8")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except BaseException:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            if len(arg) > 2:
                FBAN = arg[1]
                REASON = arg[2]
            else:
                FBAN = arg[1]
                REASON = " #TBMassBanned "
        else:
            FBAN = previous_message.sender_id
            try:
                REASON = event.text.split(" ", maxsplit=1)[1]
            except BaseException:
                REASON = ""
            if REASON.strip() == "":
                REASON = " #TBMassBanned "
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            try:
                FBAN = arg[1]
                REASON = arg[2]
            except BaseException:
                return await msg.edit("`No user designated!`")
        else:
            try:
                FBAN = arg[1]
                REASON = " #TBMassBanned "
            except BaseException:
                return await msg.edit("`No user designated!`")
    try:
        if str(FBAN) in DEVLIST:
            await msg.edit("You can't ban my dev you noob!!")
            return
        elif FBAN.startswith("@"):
            try:
                x = await ultroid_bot(GetFullUserRequest(FBAN))
                uid = x.user.id
                if str(uid) in DEVLIST:
                    await msg.edit("You can't ban my dev you noob!!")
                    return
            except Exception as e:
                print(str(e))
                return await msg.edit(str(e))
    except Exception as e:
        print(str(e))
        return await msg.edit(str(e))
    if udB.get("FBAN_GROUP_ID"):
        chat = int(udB.get("FBAN_GROUP_ID"))
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with ultroid_bot.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await asyncio.sleep(3)
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                try:
                    response = await bot_conv.get_response()
                except asyncio.exceptions.TimeoutError:
                    return await msg.edit(
                        "`Seems like rose isn't responding, or, the plugin is misbehaving`"
                    )
                await asyncio.sleep(3)
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await asyncio.sleep(3)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await ultroid_bot.download_media(
                            fedfile, "fedlist"
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, "r", errors="ignore")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    elif "You can only use fed commands once every 5 minutes" in (
                        await bot_conv.get_edit
                    ):
                        await msg.edit("Try again after 5 mins.")
                        return
                if len(fedList) == 0:
                    await msg.edit(
                        f"Unable to collect FedAdminList. Retrying ({a+1}/3)..."
                    )
                else:
                    break
        else:
            await msg.edit("Error")
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True
            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await msg.edit("Unable to collect FedAdminList.")
            return
    await msg.edit(f"FBaning in {len(fedList)} feds.")
    try:
        await ultroid_bot.send_message(chat, f"/start")
    except BaseException:
        await msg.edit("Specified FBan Group ID is incorrect.")
        return
    await asyncio.sleep(3)
    if udB.get("EXCLUDE_FED"):
        excludeFed = udB.get("EXCLUDE_FED").split(" ")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if udB.get("EXCLUDE_FED") and fed in excludeFed:
            await ultroid_bot.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await ultroid_bot.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await ultroid_bot.send_message(chat, f"/fban {FBAN} {REASON}")
        await asyncio.sleep(3)
    try:
        os.remove("fedlist")
    except Exception as e:
        print(f"Error in removing FedAdmin file.\n{str(e)}")
    await msg.edit(
        f"SuperFBan Completed.\nTotal Feds - {len(fedlist)}.\nExcluded - {exCount}.\n Affected {len(fedList) - exCount} feds.\n#TB"
    )


@ultroid_cmd(pattern="superunfban ?(.*)")
async def _(event):
    msg = await eor(event, "Starting a Mass-UnFedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await ultroid_bot.download_media(
                previous_message, "fedlist"
            )
            file = open(downloaded_file_name, encoding="utf8")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except BaseException:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            if len(arg) > 2:
                FBAN = arg[1]
                REASON = arg[2]  # rose unbans now can have reasons
            else:
                FBAN = arg[1]
                REASON = ""
        else:
            FBAN = previous_message.sender_id
            try:
                REASON = event.text.split(" ", maxsplit=1)[1]
            except BaseException:
                REASON = ""
            if REASON.strip() == "":
                REASON = ""
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            try:
                FBAN = arg[1]
                REASON = arg[2]
            except BaseException:
                return await msg.edit("`No user designated!`")
        else:
            try:
                FBAN = arg[1]
                REASON = " #TBMassUnBanned "
            except BaseException:
                return await msg.edit("`No user designated!`")
    try:
        if str(FBAN) in DEVLIST:
            await msg.edit("You can't ban my dev you noob!!")
            return
    except Exception as e:
        print(str(e))
        return await msg.edit(str(e))
    if udB.get("FBAN_GROUP_ID"):
        chat = int(udB.get("FBAN_GROUP_ID"))
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with ultroid_bot.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await asyncio.sleep(3)
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                try:
                    response = await bot_conv.get_response()
                except asyncio.exceptions.TimeoutError:
                    return await msg.edit(
                        "`Seems like rose isn't responding, or, the plugin is misbehaving`"
                    )
                await asyncio.sleep(3)
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await asyncio.sleep(3)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await ultroid_bot.download_media(
                            fedfile, "fedlist"
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, "r", errors="ignore")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    elif "You can only use fed commands once every 5 minutes" in (
                        await bot_conv.get_edit
                    ):
                        await msg.edit("Try again after 5 mins.")
                        return
                if len(fedList) == 0:
                    await msg.edit(
                        f"Unable to collect FedAdminList. Retrying ({a+1}/3)..."
                    )
                else:
                    break
        else:
            await msg.edit("Error")
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True
            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await msg.edit("Unable to collect FedAdminList.")
            return
    await msg.edit(f"UnFBaning in {len(fedList)} feds.")
    try:
        await ultroid_bot.send_message(chat, f"/start")
    except BaseException:
        await msg.edit("Specified FBan Group ID is incorrect.")
        return
    await asyncio.sleep(3)
    if udB.get("EXCLUDE_FED"):
        excludeFed = udB.get("EXCLUDE_FED").split(" ")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if udB.get("EXCLUDE_FED") and fed in excludeFed:
            await ultroid_bot.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await ultroid_bot.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await ultroid_bot.send_message(chat, f"/unfban {FBAN} {REASON}")
        await asyncio.sleep(3)
    try:
        os.remove("fedlist")
    except Exception as e:
        print(f"Error in removing FedAdmin file.\n{str(e)}")
    await msg.edit(
        f"SuperUnFBan Completed.\nTotal Feds - {len(fedlist)}.\nExcluded - {exCount}.\n Affected {len(fedList) - exCount} feds.\n#TB"
    )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=Var.HNDLR)}"})
