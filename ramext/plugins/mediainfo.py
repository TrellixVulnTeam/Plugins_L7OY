import os

from . import *


@ram_cmd(pattern="mediainfo$")
async def mediainfo(event):
    RAM_MEDIA = None
    reply = await event.get_reply_message()
    logo = "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg"
    if not reply:
        return await eod(event, "Reply to a media to fetch info...")
    if not reply.media:
        return await eod(event, "Reply to a media file to fetch info...")
    zzy = await eor(event, "`Fetching media info...`")
    RAM_MEDIA = reply.file.mime_type
    if not RAM_MEDIA:
        return await zzy.edit("Reply to a media file to fetch info...")
    elif RAM_MEDIA.startswith(("text")):
        return await zzy.edit("Reply to a media file to fetch info ...")
    hel_ = await mediadata(reply)
    file_path = await reply.download_media(Config.TMP_DOWNLOAD_DIRECTORY)
    out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
    if not out:
        out = "Unknown Format !!"
    paster = f"""
<h2>📃 MEDIA INFO 📃</h2>
<code>
{hel_}
</code>
<h2>🧐 MORE DETAILS 🧐</h2>
<code>
{out} 
</code>
<img src='{logo}'/>"""
    paste = await telegraph_paste(f"{RAM_MEDIA}", paster)
    await zzy.edit(f"📌 Fetched  Media Info Successfully !! \n\n**Check Here :** [{RAM_MEDIA}]({paste})")
    os.remove(file_path)

CmdHelp("mediainfo").add_command(
  "mediainfo", "<reply to a media>", "Fetches the detailed information of replied media."
).add_info(
  "Everything About That Media."
).add_warning(
  "✅ Harmless Module."
).add()
