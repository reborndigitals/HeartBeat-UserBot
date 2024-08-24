from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import *
from pytgcalls.types.calls import Call

from ... import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues
from ...modules.utilities.streams import *



import os
import glob
import random
import logging

def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Choosen File : {cookie_txt_file}\n')
    return f"""cookies/{str(cookie_txt_file).split("/")[-1]}"""



async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_txt_file(),
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

    def parse_size(formats):
        total_size = 0
        for format in formats:
            if 'filesize' in format:
                total_size += format['filesize']
        return total_size

    info = await get_format_info(link)
    if info is None:
        return None

    formats = info.get('formats', [])
    if not formats:
        print("No formats found.")
        return None

    total_size = parse_size(formats)
    return total_size



# Audio Player

@app.on_message(cdz(["ply", "play"]) & ~filters.private)
@sudo_users_only
async def audio_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing ...**")
    calls = await call.calls
    chat_call = calls.get(chat_id)
    audio = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message else None
    )
    type = "Audio"

    try:
        if audio:
            await aux.edit("Downloading ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            file = results[0]

        if chat_call:
            status = chat_call.status
            if status == Call.Status.IDLE:
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            elif (
                status == Call.Status.PLAYING
                or status == Call.Status.PAUSED
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"Queued At {position}")
        else:
            stream = await run_stream(file, type)
            try:
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            except NoActiveGroupCall:
                return await aux.edit("No Active VC!")
    except Exception as e:
        print(e)
        pass


# Video Player

@app.on_message(cdz(["vply", "vplay"]) & ~filters.private)
@sudo_users_only
async def video_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing ...**")
    calls = await call.calls
    chat_call = calls.get(chat_id)
    video = (
        (
            message.reply_to_message.video
            or message.reply_to_message.document
        )
        if message.reply_to_message else None
    )
    type = "Video"
    try:
        if video:
            await aux.edit("Downloading ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            file = results[0]

        if chat_call:
            status = chat_call.status
            if status == Call.Status.IDLE:
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            elif (
                status == Call.Status.PLAYING
                or status == Call.Status.PAUSED
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"Queued At {position}")
        else:
            stream = await run_stream(file, type)
            try:
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            except NoActiveGroupCall:
                return await aux.edit("No Active VC!")
    except Exception as e:
        print(e)
        pass
  




# Audio Player (Play From Anywhere)

@app.on_message(cdz(["cply", "cplay"]))
@sudo_users_only
async def audio_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    calls = await call.calls
    chat_call = calls.get(chat_id)
    if chat_id == 0:
        return await eor(message,
            "**🥀 Please Set A Chat To Start Stream❗**"
    )
    aux = await eor(message, "**Processing ...**")
    audio = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message
        else None
    )
    type = "Audio"
    try:
        if audio:
            await aux.edit("Downloading ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            file = results[0]
        if chat_call:
            status = chat_call.status
            if status == Call.Status.IDLE:
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            elif (
                status == Call.Status.PLAYING
                or status == Call.Status.PAUSED
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"Queued At {position}")
        else:
            stream = await run_stream(file, type)
            try:
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            except NoActiveGroupCall:
                return await aux.edit("No Active VC!")
    except Exception as e:
        print(e)
        pass


# Video Player

@app.on_message(cdz(["cvply", "cvplay"]))
@sudo_users_only
async def video_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    calls = await call.calls
    chat_call = calls.get(chat_id)
    if chat_id == 0:
        return await eor(message,
            "**🥀 Please Set A Chat To Start Stream❗**"
    )
    aux = await eor(message, "**Processing ...**")
    video = (
        (
            message.reply_to_message.video
            or message.reply_to_message.document
        )
        if message.reply_to_message
        else None
    )
    type = "Video"
    try:
        if video:
            await aux.edit("Downloading ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            file = results[0]
        if chat_call:
            status = chat_call.status
            if status == Call.Status.IDLE:
                stream = await run_stream(file, type)
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            elif (
                status == Call.Status.PLAYING
                or status == Call.Status.PAUSED
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"Queued At {position}")
        else:
            stream = await run_stream(file, type)
            try:
                await call.play(chat_id, stream)
                await aux.edit("Playing!")
            except NoActiveGroupCall:
                return await aux.edit("No Active VC!")
    except Exception as e:
        print(e)
        pass

  
