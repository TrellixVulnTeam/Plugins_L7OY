import os
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from . import *


@ram_cmd(pattern="extdl$")
async def install(event):
    chat = Config.PLUGIN_CHANNEL
    documentss = await event.client.get_messages(chat, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    total_doxx = range(0, total)
    ram_ = await eor(event, "Installing plugins from Plugin Channel...")
    zzy = "**Installed Plugins :**\n\n"
    for ixo in total_doxx:
        mxo = documentss[ixo].id
        downloaded_file_name = await event.client.download_media(
            await event.client.get_messages(chat, ids=mxo), "ramubot/plugins/"
        )
        if "(" not in downloaded_file_name:
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            zzy += "• __Installed Plugin__ `{}` __successfully.__\n".format(os.path.basename(downloaded_file_name))
        else:
            zzy += "• __Plugin__ `{}` __has been pre-installed and cannot be installed.__\n".format(os.path.basename(downloaded_file_name))
    await ram_.edit(zzy)


@ram_cmd(pattern="installall ([\s\S]*)")
async def install(event):
    chat = event.pattern_match.group(1)
    ram_ = await eor(event, f"Starting To Install Plugins From {chat} !!")
    zzy = f"**Installed Plugins From {chat} :**\n\n"
    documentss = await event.client.get_messages(chat, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    total_doxx = range(0, total)
    for ixo in total_doxx:
        mxo = documentss[ixo].id
        downloaded_file_name = await event.client.download_media(
            await event.client.get_messages(chat, ids=mxo), "ramubot/plugins/"
        )
        if "(" not in downloaded_file_name:
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            zzy += "• __Installed Plugin__ `{}` __successfully.__\n".format(os.path.basename(downloaded_file_name))
        else:
            zzy += "• __Plugin__ `{}` __has been pre-installed and cannot be installed.__\n".format(os.path.basename(downloaded_file_name))
    await ram_.edit(zzy)


CmdHelp("extra_py").add_command(
  "extdl", None, "Installs all plugins from the channal which id is in PLUGIN_CHANNEL Configiable"
).add_command(
  "installall", "<channel/grp username>", "Installs all the plugins in provided channel / group. (May get floodwait error)"
).add_info(
  "Extra Plugins."
).add_warning(
  "Don't Install plugins from Unknown channel."
).add()
