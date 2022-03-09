import asyncio
import heroku3
import json
import os
import requests
import sys
import urllib3
from ramext.config import Config
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from . import *

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
UPSTREAM_REPO_BRANCH = "master"
UPSTREAM_REPO_URL = "https://github.com/izzy-adeeva/Plugins"
REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "No Heroku App Found!"
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "Restarting Heroku App..."
IS_SELECTED_DIFFERENT_BRANCH = "Looks like a custom branch {branch_name} is being used!\nIn this case, updater is unable to identify the branch to be updated. Please check out to an official branch, and re-start the updater."
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt")


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**New UPDATE available for [{ac_br}]:\n\n CHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await eor(event, "`Changelog is too big, view the file to see it.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
            thumb=ram_logo,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await eor(event, "✅ Successfully updated RAM-UBOT!\n\nBot is restarting please wait for a minute.")
    args = [sys.executable, "-m", "ramext"]
    os.execle(sys.executable, *args, os.environ)
    return


@ram_cmd(pattern="update(| now)$")
async def upstream(event):
    conf = event.pattern_match.group(1).strip()
    event = await eor(event, "`Checking for new updates...`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await eod(event, "Set  `HEROKU_APP_NAME`  and  `HEROKU_API_KEY`  to update your bot 🥴")
    txt = "😕 `Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error}  not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`The directory {error} "
                "does not seem to be a git repository.\n"
                "Fix that by force updating! Using "
                f"`{ii}update now.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            f"`Looks like you are using your own custom git branch ( {ac_br} ). "
            "Please checkout to official branch that is ( master )`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    cid = await client_id(event)
    ram_mention = cid[2]
   if changelog == "" and not force_update:
        await event.edit(
            "\n`RAM-UBOT_EXTENDED is`  **up-to-date**  `with`  "
            f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"do `{ii}update build` to update your **RAM-UBOT**!!"
        )
    if force_update:
        await event.edit(
            "`Force-Updating RAM-UBOT. Please wait...`"
        )
    if conf == "now":
        await event.edit("`Update In Progress! Please Wait....`")
        await update(event, repo, ups_rem, ac_br)
    return


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "**Please set up**  `HEROKU_APP_NAME`  **to update!"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "`Invalid Heroku vars for updating."
            )
            return repo.__del__()
    
        await event.edit(f"<b><i>RAM-UBOT Docker Build In Progress !!!</b></i> ", link_preview=False, parse_mode="HTML")
        ups_rem.fetch(ac_br)
        cid = await client_id(event)
        ram_mention = cid[2]
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n**Error log:**\n`{error}`")
            return repo.__del__()
        build_status = app.builds(order_by="created_at", sort="desc")[0]
        if build_status.status == "failed":
            await event.edit(
                "`Build failed ⚠️`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit(f"**Your RAM-UBOT Is UpToDate**\n\n**Version :**  __{ram_version}__\n**Owner :**  {ram_mention}")
    else:
        await event.edit("**Please set up**  `HEROKU_API_KEY`  **from heroku to update!**")
    return


@ram_cmd(pattern="update build$")
async def upstream(event):
    event = await eor(event, "`Hard-Update In Progress... \nPlease wait until docker build is finished...`")
    off_repo = "https://github.com/hitokizzy/RAM-UBOT_EXTENDED"
    os.chdir("/app")
    ibels = f"rm -rf .git"
    try:
        await runcmd(ibels)
    except BaseException:
        pass
    txt = "😕 `Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error}  not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
   # _version, _release, _branch, _author, _auturl = await ram_info(ram_info)
    await event.edit(f"<b><i>RAM-UBOT Docker Build In Progress !!</b></i>", link_preview=False, parse_mode="HTML")
    await deploy(event, repo, ups_rem, ac_br, txt)


CmdHelp("update").add_command(
  "update", None, "Checks if any new update is available."
).add_command(
  "update now", None, "Soft-Update Your RAM-UBOT. Basically if you restart dyno it will go back to previous deploy."
).add_command(
  "update build", None, "Hard-Update Your RAM-UBOT. This won't take you back to your previous deploy. This will be triggered even if there is no changelog."
).add_info(
  "RAM-UBOT Updater."
).add_warning(
  "✅ Harmless Module."
).add()
