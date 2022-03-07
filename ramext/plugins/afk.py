import asyncio
import datetime

from telethon import events
from telethon.tl import functions, types

from ramext.sql.gvar_sql import addgvar, gvarstat, delgvar
from . import *


global afk_time
global last_afk_message
global afk_start
global afk_end
afk_time = None
last_afk_message = {}
afk_start = {}


@H1.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    came_back = datetime.datetime.now()
    afk_end = came_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if "#" not in current_message and gvarstat("AFK") == "YES":
        ramubot = await event.client.send_message(
            event.chat_id,
            "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
            + total_afk_time
            + "`", file=rampic
        )
        try:
            await unsave_gif(event, ramubot)
        except:
            pass
        try:
            delgvar("AFK")
        except:
            pass
        try:
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
            )
        except Exception as e:
            await event.client.send_message(
                event.chat_id,
                "Please set `LOGGER_ID` "
                + "for the proper functioning of afk."
                + f" Ask in {ram_grp} to get help!",
                reply_to=event.message.id,
                link_preview=False,
                silent=True,
            )
        await asyncio.sleep(5)
        await ramubot.delete()
        afk_time = None


@H1.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
async def on_afk(event):
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    cum_back = datetime.datetime.now()
    afk_end = cum_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        return False
    if gvarstat("AFK") == "YES" and not (await event.get_sender()).bot:
        msg = None
        if reason == "":
            message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
        else:
            message_to_reply = (
                f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                + f"\n**💬 Reason :** {reason}"
                )
        msg = await event.reply(message_to_reply, file=rampic)
        try:
            await unsave_gif(event, msg)
        except:
            pass
        await asyncio.sleep(2)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg


@H1.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
async def _(event):
    if event.fwd_from:
        return
    krakenop = await event.get_reply_message()
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    global rampic
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.datetime.now()
    afk_start = start_1.replace(microsecond=0)
    owo = event.text[5:]
    reason = owo
    rampic = await event.client.download_media(krakenop)
    if gvarstat("AFK") != "YES":
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()
        if owo == "":
            addgvar("AFK", "YES")
            x = await event.client.send_message(
                event.chat_id, f"**I'm going afk🚶**", file=rampic)
            try:
                await unsave_gif(event, x)
            except:
                pass
            await asyncio.sleep(0.001)
            await event.delete()
            try:
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=rampic
                    )
                try:
                    await unsave_gif(event, xy)
                except:
                    pass
            except Exception as e:
                logger.warn(str(e))
        else:
            addgvar("AFK", "YES")
            x = await event.client.send_message(
                event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason}`", file=rampic)
            try:
                await unsave_gif(event, x)
            except:
                pass
            await asyncio.sleep(0.001)
            await event.delete()
            try:
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason}`",file=rampic
                    )
                try:
                    await unsave_gif(event, xy)
                except:
                    pass
            except Exception as e:
                logger.warn(str(e))


if RAM2:
    @RAM2.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        came_back = datetime.datetime.now()
        afk_end = came_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK2") == "YES":
            ramubot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=rampic
            )
            try:
                await unsave_gif(event, ramubot)
            except:
                pass
            try:
                delgvar("AFK2")
            except:
                pass
            try:
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {ram_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await ramubot.delete()
            afk_time = None


    @RAM2.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        cum_back = datetime.datetime.now()
        afk_end = cum_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK2") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason}"
                    )
            msg = await event.reply(message_to_reply, file=rampic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message:
                await last_afk_message[event.chat_id].delete()
            last_afk_message[event.chat_id] = msg


    @RAM2.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        krakenop = await event.get_reply_message()
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        global reason
        global rampic
        afk_time = None
        last_afk_message = {}
        afk_end = {}
        start_1 = datetime.datetime.now()
        afk_start = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason = owo
        rampic = await event.client.download_media(krakenop)
        if not gvarstat("AFK2"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time = datetime.datetime.now()
            if owo == "":
                addgvar("AFK2", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK2", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason}`", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason}`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


if RAM3:
    @RAM3.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        came_back = datetime.datetime.now()
        afk_end = came_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK3") == "YES":
            ramubot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=rampic
            )
            try:
                await unsave_gif(event, ramubot)
            except:
                pass
            try:
                delgvar("AFK3")
            except:
                pass
            try:
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {ram_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await ramubot.delete()
            afk_time = None


    @RAM3.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        cum_back = datetime.datetime.now()
        afk_end = cum_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK3") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason}"
                    )
            msg = await event.reply(message_to_reply, file=rampic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message:
                await last_afk_message[event.chat_id].delete()
            last_afk_message[event.chat_id] = msg


    @RAM3.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        krakenop = await event.get_reply_message()
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        global reason
        global rampic
        afk_time = None
        last_afk_message = {}
        afk_end = {}
        start_1 = datetime.datetime.now()
        afk_start = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason = owo
        rampic = await event.client.download_media(krakenop)
        if not gvarstat("AFK3"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time = datetime.datetime.now()
            if owo == "":
                addgvar("AFK3", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK3", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason}`", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason}`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


if RAM4:
    @RAM4.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        came_back = datetime.datetime.now()
        afk_end = came_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK4") == "YES":
            ramubot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=rampic
            )
            try:
                await unsave_gif(event, ramubot)
            except:
                pass
            try:
                delgvar("AFK4")
            except:
                pass
            try:
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {ram_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await ramubot.delete()
            afk_time = None


    @RAM4.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        cum_back = datetime.datetime.now()
        afk_end = cum_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK4") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason}"
                    )
            msg = await event.reply(message_to_reply, file=rampic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message:
                await last_afk_message[event.chat_id].delete()
            last_afk_message[event.chat_id] = msg


    @RAM4.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        krakenop = await event.get_reply_message()
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        global reason
        global rampic
        afk_time = None
        last_afk_message = {}
        afk_end = {}
        start_1 = datetime.datetime.now()
        afk_start = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason = owo
        rampic = await event.client.download_media(krakenop)
        if not gvarstat("AFK4"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time = datetime.datetime.now()
            if owo == "":
                addgvar("AFK4", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK4", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason}`", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason}`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


if RAM5:
    @RAM5.on(events.NewMessage(outgoing=True))
    async def set_not_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        came_back = datetime.datetime.now()
        afk_end = came_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK5") == "YES":
            ramubot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`", file=rampic
            )
            try:
                await unsave_gif(event, ramubot)
            except:
                pass
            try:
                delgvar("AFK5")
            except:
                pass
            try:
                await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`"
                )
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    "Please set `LOGGER_ID` "
                    + "for the proper functioning of afk."
                    + f" Ask in {ram_grp} to get help!",
                    reply_to=event.message.id,
                    link_preview=False,
                    silent=True,
                )
            await asyncio.sleep(5)
            await ramubot.delete()
            afk_time = None


    @RAM5.on(events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk(event):
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        cum_back = datetime.datetime.now()
        afk_end = cum_back.replace(microsecond=0)
        if afk_start != {}:
            total_afk_time = str((afk_end - afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK5") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if reason == "":
                message_to_reply = f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {reason}"
                    )
            msg = await event.reply(message_to_reply, file=rampic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in last_afk_message:
                await last_afk_message[event.chat_id].delete()
            last_afk_message[event.chat_id] = msg


    @RAM5.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def _(event):
        if event.fwd_from:
            return
        krakenop = await event.get_reply_message()
        global afk_time
        global last_afk_message
        global afk_start
        global afk_end
        global reason
        global rampic
        afk_time = None
        last_afk_message = {}
        afk_end = {}
        start_1 = datetime.datetime.now()
        afk_start = start_1.replace(microsecond=0)
        owo = event.text[5:]
        reason = owo
        rampic = await event.client.download_media(krakenop)
        if not gvarstat("AFK5"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk_time = datetime.datetime.now()
            if owo == "":
                addgvar("AFK5", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))
            else:
                addgvar("AFK5", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**\n\n**Because :** `{reason}`", file=rampic)
                try:
                    await unsave_gif(event, x)
                except:
                    pass
                await asyncio.sleep(0.001)
                await event.delete()
                try:
                    xy = await event.client.send_message(
                        Config.LOGGER_ID,
                        f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{reason}`",file=rampic
                        )
                    try:
                        await unsave_gif(event, xy)
                    except:
                        pass
                except Exception as e:
                    logger.warn(str(e))


CmdHelp("afk").add_command(
  'afk', '<reply to media>/<reason>', 'Marks you AFK with reason also shows afk time. Media also supported.', "afk <reason>`"
).add_extra(
  "📌 Exception", "Use # in a msg to stay in afk mode while chatting."
).add_info(
  "Away From Keyboard"
).add_warning(
  "✅ Harmless Module."
).add()
