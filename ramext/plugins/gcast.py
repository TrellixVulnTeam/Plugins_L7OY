from . import *

@ram_cmd(pattern="gcast(?:\s|$)([\s\S]*)")
async def _(event):
    reply_msg = await event.get_reply_message()
    flag = event.text[-4:]
    if reply_msg:
        OwO = reply_msg.text
        file = reply_msg.media
    else:
        OwO = str(event.text[7:])
        file = None
    if OwO == "":
        return await eod(event, "I need something to Gcast.")
    hel_ = await eor(event, "`Gcasting message...`")
    sed = 0
    owo = 0
    if "-all" in flag:
        async for all in event.client.iter_dialogs():
            chat = all.id
            try:
                zzy = OwO.replace("-all", "")
            except:
                pass
            try:
                if chat != -1001496036895:
                    await event.client.send_message(chat, zzy, file=file)
                    owo += 1
                elif chat == -1001496036895:
                    pass
            except BaseException:
                sed += 1
    elif "-pvt" in flag:
        async for pvt in event.client.iter_dialogs():
            if pvt.is_user and not pvt.entity.bot:
                chat = pvt.id
                try:
                    zzy = OwO.replace("-pvt", "")
                except:
                    pass
                try:
                    await event.client.send_message(chat, zzy, file=file)
                    owo += 1
                except BaseException:
                    sed += 1
    elif "-grp" in flag:
        async for g in event.client.iter_dialogs():
            if g.is_group:
                chat = g.id
                try:
                    zzy = OwO.replace("-grp", "")
                except:
                    pass
                try:
                    if chat != -1001496036895:
                        await event.client.send_message(chat, zzy, file=file)
                        owo += 1
                    elif chat == -1001496036895:
                        pass
                except BaseException:
                    sed += 1
    else:
        return await hel_.edit("Please give a flag to Gcast message. \n\n**Available flags are :** \n• -all : To Gcast in all chats. \n• -pvt : To Gcast in private chats. \n• -grp : To Gcast in groups.")
    UwU = sed + owo
    if flag == "-all":
        omk = "Chats"
    elif flag == "-pvt":
        omk = "PM"
    elif flag == "-grp":
        omk = "Groups"
    await hel_.edit(f"**Gcast Executed Successfully !!** \n\n**📍 Sent in :** `{owo} {omk}`\n**📍 Failed in :** `{sed} {omk}`\n**📍 Total :** `{UwU} {omk}`")

# This is a bad way. but works just fine (*﹏*;)

CmdHelp("gcast").add_command(
  "gcast", "<text/reply> <flag>", "Globally Broadcast the replied or given message based on flag given.", f"gcast o -all / {ii}gcast o -grp / {ii}gcast o -pvt"
).add_info(
  "Global Broadcast."
).add_extra(
  "🚩 Flags", "-all, -pvt, -grp"
).add_warning(
  "✅ Harmless Module."
).add()
