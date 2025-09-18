import pyrogram
import logging, asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid
import time
from time import sleep, strftime, gmtime, time
import os
import threading
import json
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty
from pyrogram.types import Message
from subprocess import getstatusoutput
import subprocess
import random
from os.path import join
from random import randint
from os import remove

# Load configuration from config.json
with open('config.json', 'r') as f: 
    DATA = json.load(f)

def getenv(var): 
    return os.environ.get(var) or DATA.get(var, None)

bot_token = ""
api_hash = ""
api_id = 
auth_users = []
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = "BQA_rUO3DjMTu9HACOmxVoC9KyN135J_ntXaIHHKquGDN2xEUKTnntmfaREfYR2kIrD8slFNEs8q4dGC3WAx8A2GNRg0maSRira0VHY2DibmtyUCCFjdriaQXUUAhpZ_ew8YG4WK8xrAPG8Nwq_Rm_gFwKQAEBTSictNVuzhrrZWITs56oJB8QRfVB3Jb3BdgWEVgSHpuvvvXzNNjSHFeFYu0lLnYjHZJzFmWkY8Kqs9RoUEEXGVPHynvcLHusT33Fr4DPO_ob-aNio8WOghyb2BnX0Q8znwDSBQtPLNhbBtz6kBtXx_NyjKBQ7U0dajaXEd3REkj9MftKm4bQfnwLVGAAAAAaXpIloA"
if ss is not None:
    acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else: 
    acc = None

channel_id = 

@bot.on_message(filters.command("channel_id"))
async def set_channel_id(client: Client, message: Message):
    global channel_id
    channel_id = int(message.text.split(maxsplit=1)[1])
    await message.reply(f"Channel ID set to: {channel_id}")


async def msg_info(msg):
    media_type = ""

    if msg.photo:
        media_type = "photo"
    elif msg.video:
        media_type = "video"
    elif msg.document:
        media_type = "document"
    elif msg.audio:
        media_type = "audio"
    elif msg.voice:
        media_type = "voice"
    elif msg.animation:
        media_type = "animation"

    full_name = msg.from_user.first_name or ''
    if msg.from_user.last_name:
        full_name += f' {msg.from_user.last_name}'
    if not full_name and msg.from_user.username:
        full_name = msg.from_user.username

    sender = f"[{full_name}](tg://user?id={msg.from_user.id})"
    return sender, media_type

async def save_media(msg, sender, media_type):
    global channel_id
    try:
        mes = await acc.send_message(channel_id, f"{sender} sent {media_type}\n__Uploading...__")
        file_ext = ""
        if media_type == "photo":
            file_ext = "jpg"
        elif media_type == "video":
            file_ext = "mp4"
        elif media_type == "document":
            file_ext = msg.document.file_name.split(".")[-1].lower() if msg.document.file_name else "dat"
        elif media_type == "audio":
            file_ext = msg.audio.file_name.split(".")[-1].lower() if msg.audio.file_name else "mp3"
        elif media_type == "voice":
            file_ext = "ogg"
        elif media_type == "animation":
            file_ext = "mp4"
        else:
            file_ext = "dat"

        file_name = f"{msg.from_user.id}_{int(time() * 10000000)}_{randint(1, 10000000)}.{file_ext}"
        await acc.download_media(msg, file_name)
        mention = sender
        with open(join("downloads", file_name), "rb") as att:
            if media_type == "photo":
                await acc.send_photo(channel_id, att, mention)
            elif media_type == "video":
                await acc.send_video(channel_id, att, mention)
            elif media_type == "document":
                await acc.send_document(channel_id, att, caption=mention)
            elif media_type == "audio":
                await acc.send_audio(channel_id, att, caption=mention)
            elif media_type == "voice":
                await acc.send_voice(channel_id, att, caption=mention)
            elif media_type == "animation":
                await acc.send_animation(channel_id, att, caption=mention)
        remove(join("downloads", file_name))
        await mes.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)
        print(f"Flood wait: {e}")
    except MessageIdInvalid:
        print("Message ID invalid.")
    except PeerIdInvalid:
        print("Peer ID invalid.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        

animated_stickers = [
    "CAACAgUAAxkDAAEBOrJmgheC_fWJCCsB7OONOt5-ducS6wACJg0AAkbwaVZc7Q0OPZbiAx4E",  # Replace with your sticker file_id
    "CAACAgUAAxkDAAEBOrVmgheTS4hukiuH7264ecw01RbaxQAC6Q8AAqCZ-Fbtiwp4DLOwXx4E",
    "CAACAgUAAxkDAAEBOrhmghfVCw4p7a086abOjAa-cmCg7wACBgwAAlGZeVYCjKZ5VFgb2h4E"
]

@acc.on_message(filters.command(["animate_stickers"], prefixes="!") & (filters.private | filters.channel))
async def start_sticker_animation(client, message):
    for sticker in animated_stickers:
        await client.send_sticker(message.chat.id, sticker)
        await asyncio.sleep(1)

@acc.on_message(filters.command(["animate"], prefixes="!") & filters.private)
async def start_animation(client, message):
    animation_frames = [
        "Loading.",
        "Loading..",
        "Loading...",
        "Loading....",
        "Loading....."
    ]

    for frame in animation_frames:
        await message.reply(frame)
        await asyncio.sleep(1)
        


@acc.on_message(filters.command(["file_id"], prefixes="/") & filters.reply & filters.me)
async def get_sticker_file_id(client, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker = message.reply_to_message.sticker
        file_id = sticker.file_id
        await message.reply(f"Sticker File ID: {file_id}")
    else:
        await message.reply("Please reply to a sticker message with /file_id to get the sticker's file ID.")
        

@acc.on_message(filters.text & filters.private)
async def reply_to_greetings(client, message):
    text = message.text.lower()
    if any(word in text.split() for word in ["hi", "hello", "hey", "hlo"]):
        await message.reply("Hello! How can I assist you today?")
	    
@acc.on_message(filters.private & filters.me & (filters.photo | filters.video | filters.document | filters.audio | filters.voice | filters.animation))
async def in_background(_, msg):
    try:
        sender, media_type = await msg_info(msg)
        if sender:
            await save_media(msg, sender, media_type)
    except Exception as e:
        print(f"Error in processing media: {e}")

@acc.on_message(filters.command(["hmm", "nice", "wow"], prefixes="!") & filters.reply & filters.me)
async def on_command(_, msg):
    global channel_id
    try:
        if msg.reply_to_message.media:
            sender, media_type = await msg_info(msg.reply_to_message)
            if sender:
                await save_media(msg.reply_to_message, sender, media_type)
                await acc.send_message(channel_id, f"**Media saved!**")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        print(f"Flood wait: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        await acc.send_message(channel_id, f"An error occurred: {e}")

# Delete messages in a specified range command
@bot.on_message(filters.command(["delete"]))
async def delete_messages_in_range(client, message):
    # Split the command arguments
    args = message.text.split()[1:]  # Exclude the command itself

    if len(args) != 2:
        await message.reply("Please provide the chat ID and the message range.")
        return

    try:
        chatid = int(args[0])
        fromID, toID = map(int, args[1].split("-"))
    except ValueError:
        await message.reply("Invalid chat ID or message range.")
        return

    status = await message.reply(f"Trying to delete messages from {fromID} to {toID}...")

    deleted_msgs_count = 0
    for msgid in range(fromID, toID + 1):
        try:
            await bot.delete_messages(message.chat.id, msgid)
            deleted_msgs_count += 1
        except Exception as e:
            await message.reply(f"An error occurred: {str(e)}")

    await status.delete()

    await message.reply(f"Successfully deleted {deleted_msgs_count} messages.")


# Define global variables
words_to_remove_from_filename = []
given_thumbnail = "not_set"
url_count = 0
# Default replacements
words_to_replace_in_caption = {}
# Global variables to store the watermark paths
watermark_url_remove = None
watermark_url_add = None
watermark_text = None
# Global variable to track whether the approval process should continue
approval_process_running = False



@acc.on_message(filters.command("approve", [".", "/"]) & filters.me)
async def approve_specific_requests(client, message):
    global approval_process_running
    Id = message.chat.id
    await message.delete(True)
    
    num_approvals = 0  # Counter to track the number of approvals
    approval_process_running = True  # Start the approval process
    
    # Parse the command to check if a specific number of approvals is requested
    command_parts = message.text.split()
    if len(command_parts) != 2:
        error_msg = await client.send_message(Id, "Invalid command format. Please use: `/approve <number>`")
        await asyncio.sleep(5)
        await error_msg.delete()
        return

    try:
        num_requested = int(command_parts[1])
    except ValueError:
        error_msg = await client.send_message(Id, "Invalid command format. Please use: `/approve <number>`")
        await asyncio.sleep(5)
        await error_msg.delete()
        return
    
    try:
        while approval_process_running:
            try:
                await client.approve_all_chat_join_requests(Id)
                num_approvals += 1  # Increment the counter after each approval
                
                # Check if the requested number of approvals is achieved
                if num_approvals == num_requested:
                    approval_process_running = False
                    break
            except FloodWait as t:
                await asyncio.sleep(t.value)
            except Exception as e:
                logging.error(str(e))
                break  # Exit the loop if an error occurs
    
    except FloodWait as s:
        await asyncio.sleep(s.value)
    
    msg = await client.send_message(Id, f"**Task Completed** ✓ **approved {num_approvals} Pending Join Requests**")
    await asyncio.sleep(5)  # Sleep for 5 seconds to allow the message to be read
    await msg.delete()


@acc.on_message(filters.command("run_approval", [".", "/"]) & filters.me)
async def run_approval(client, message):
    global approval_process_running
    Id = message.chat.id
    await message.delete(True)
    
    num_approvals = 0  # Counter to track the number of approvals
    approval_process_running = True  # Start the approval process
    
    try:
        while approval_process_running:  # Loop until the approval process is stopped
            try:
                await client.approve_all_chat_join_requests(Id)
                num_approvals += 1  # Increment the counter after each approval
            except FloodWait as t:
                await asyncio.sleep(t)
            except Exception as e:
                logging.error(str(e))
                break  # Exit the loop if an error occurs
    except FloodWait as s:
        await asyncio.sleep(s)
    
    msg = await client.send_message(Id, f"**Task Completed** ✓ **approved {num_approvals} Pending Join Requests**")
    await asyncio.sleep(5)  # Sleep for 5 seconds to allow the message to be read
    await msg.delete()

@acc.on_message(filters.command("stop_approval", [".", "/"]) & filters.me)
async def stop_approval(client, message):
    global approval_process_running
    Id = message.chat.id
    approval_process_running = False  # Stop the approval process
    await client.send_message(Id, "approval process stopped.")

# download status
def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"╭──⌈📥Downloading📥⌋──╮\n├ 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨 📈-: **{txt}**\n╰────⌈ ✨❤️ 𝐊𝐔𝐍𝐀𝐋 ❤️✨ ⌋────╯")
            time.sleep(10)
        except:
            time.sleep(5)

# upload status
def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"╭──⌈📤 𝙐𝙥𝙡𝙤𝙖𝙙𝙞𝙣𝙜 📤⌋──╮\n├ 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨 📈: **{txt}**\n╰────⌈ ✨❤️ 𝐊𝐔𝐍𝐀𝐋 ❤️✨ ⌋────╯")
            time.sleep(10)
        except:
            time.sleep(5)

# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bot.send_message(message.chat.id, "Yes I am Active")
        

@bot.on_message(filters.command(["replace"]))
def replace_command_handler(client, message):
    global words_to_replace_in_caption
    try:
        # Extract the replacement pairs from the command
        replace_data = message.text.split("/replace ")[1]
        # Split the replacement pairs by comma
        replace_pairs = replace_data.split(',')
        replace_dict = {}
        for pair in replace_pairs:
            # Split each pair by colon to separate key and value
            key, value = pair.split(':')
            # Remove leading/trailing whitespaces
            key = key.strip()
            value = value.strip()
            # Add the pair to the replacement dictionary
            replace_dict[key] = value
        # Update the global words_to_replace_in_caption dictionary with the new replacement pairs
        words_to_replace_in_caption.update(replace_dict)
        # Inform the user about the successful update
        bot.send_message(message.chat.id, "Replacement dictionary updated successfully.")
    except:
        bot.send_message(message.chat.id, "Invalid replace command syntax.")

@bot.on_message(filters.command("remove"))
def handle_remove_command(client: pyrogram.Client, message: pyrogram.types.Message):
    global words_to_remove_from_filename
    # Get the text after the command
    text_after_command = message.text.split(maxsplit=1)[1].strip()
    
    # Check if text is empty
    if not text_after_command:
        bot.send_message(message.chat.id, "Please provide words to remove after the command.")
        return
    
    # Update words to remove from filename
    words_to_remove_from_filename = text_after_command.split(",")
    words_to_remove_from_filename = [word.strip() for word in words_to_remove_from_filename]
    
    # Send a message indicating the set words
    bot.send_message(message.chat.id, f"You have set these words to be removed from the filename and Caption: {', '.join(words_to_remove_from_filename)}")

def remove_watermark(video_path, overlay_path, output_path):
    cmd = f'ffmpeg -i "{video_path}" -i "{overlay_path}" -filter_complex "overlay=(main_w-overlay_w-10):(main_h-overlay_h-10)" -c:a copy -preset ultrafast "{output_path}"'
    subprocess.run(cmd, shell=True)

def add_watermark(video_path, overlay_path, output_path, duration=30):
    cmd = (
        f'ffmpeg -i "{video_path}" -i "{overlay_path}" '
        f'-filter_complex "[0:v][1:v] overlay=(main_w-overlay_w-10):(main_h-overlay_h-10):enable=\'lte(t,{duration})\'" '
        f'-c:a copy -preset ultrafast "{output_path}"'
    )
    subprocess.run(cmd, shell=True)

def add_text_watermark_for_initial_duration(video_path, text, output_path, duration=30):
    cmd = (
        f'ffmpeg -i "{video_path}" '
        f'-vf "drawtext=text=\'{text}\':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=48:fontcolor=gray@0.75:enable=\'lte(t,{duration})\'" '
        f'-c:a copy -preset ultrafast "{output_path}"'
    )
    subprocess.run(cmd, shell=True)


# Function to extract a random frame from a video
def extract_random_frame(video_path, output_path):
    # Get video duration
    cmd_duration = f'ffprobe -v error -show_entries format=duration -of default=noprint_wraccers=1:nokey=1 "{video_path}"'
    duration_output = subprocess.check_output(cmd_duration, shell=True)
    duration = float(duration_output)

    # Generate a random time within the video duration
    random_time = random.uniform(0, duration)

    # Extract frame at the random time
    cmd_extract = f'ffmpeg -ss {random_time} -i "{video_path}" -vframes 1 "{output_path}"'
    subprocess.run(cmd_extract, shell=True)

    return output_path

@bot.on_message(filters.command("remove_watermark"))
def handle_remove_watermark_command(client: pyrogram.Client, message: pyrogram.types.Message):
    global watermark_url_remove
    remove_watermark = message.text.split(' ', 1)[1]  # Get the URL from the message
    if remove_watermark.startswith("http://") or remove_watermark.startswith("https://"):
        getstatusoutput(f"wget '{remove_watermark}' -O 'remove_watermark.jpg'")
        watermark_url_remove = "remove_watermark.jpg"
        bot.send_message(message.chat.id, "Watermark URL for removal has been set successfully.")
    else:
        watermark_url_remove = None
        bot.send_message(message.chat.id, "Invalid URL. Please provide a valid URL.")

@bot.on_message(filters.command("set_watermark"))
def handle_set_watermark_command(client: pyrogram.Client, message: pyrogram.types.Message):
    global watermark_url_add
    set_watermark = message.text.split(' ', 1)[1]  # Get the URL from the message
    if set_watermark.startswith("http://") or set_watermark.startswith("https://"):
        getstatusoutput(f"wget '{set_watermark}' -O 'set_watermark.jpg'")
        watermark_url_add = "set_watermark.jpg"
        bot.send_message(message.chat.id, "Watermark URL for addition has been set successfully.")
    else:
        watermark_url_add = None
        bot.send_message(message.chat.id, "Invalid URL. Please provide a valid URL.")

@bot.on_message(filters.command("set_watermark_text"))
def handle_set_watermark_text_command(client: pyrogram.Client, message: pyrogram.types.Message):
    global watermark_text
    watermark_text = message.text.split(' ', 1)[1]  # Get the text from the message
    bot.send_message(message.chat.id, "Watermark text has been set successfully.")

@bot.on_message(filters.command("reset_watermark"))
def handle_reset_watermark_command(client: pyrogram.Client, message: pyrogram.types.Message):
    global watermark_url_remove, watermark_url_add, watermark_text
    watermark_url_remove = None
    watermark_url_add = None
    watermark_text = None
    bot.send_message(message.chat.id, "Watermark settings have been reset to none.")


import random

@bot.on_message(filters.command("set_thumbnail"))
def handle_set_thumbnail_command(client: pyrogram.Client, message: pyrogram.types.Message):
    global given_thumbnail
    command_parts = message.text.split(' ', 2)
    if len(command_parts) < 2:
        bot.send_message(message.chat.id, "Please provide a valid command.")
        return

    thumbnail_option = command_parts[1].lower()

    if thumbnail_option == "reset":
        # Reset the thumbnail setting to none
        given_thumbnail = "not_set"
        bot.send_message(message.chat.id, "Thumbnail setting has been reset to none.")
    elif thumbnail_option == "random":
        # Set thumbnail to random frame
        given_thumbnail = "random"
        bot.send_message(message.chat.id, "Thumbnail set to random frame.")
    elif thumbnail_option.startswith("http://") or thumbnail_option.startswith("https://"):
        # Set thumbnail to URL
        getstatusoutput(f"wget '{thumbnail_option}' -O 'thumbnail.jpg'")
        given_thumbnail = "thumbnail.jpg"
        bot.send_message(message.chat.id, "Thumbnail URL has been set successfully.")
    else:
        bot.send_message(message.chat.id, "Invalid command option. Please provide a valid URL or specify 'random' or 'reset'.")


@bot.on_message(filters.text)
async def save(client: pyrogram.Client, message: pyrogram.types.Message):
    print(message.text)

    # joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

        if acc is None:
            await bot.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
            return

        try:
            try: 
                await acc.join_chat(message.text)
            except Exception as e: 
                await bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)
                return
            await bot.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await bot.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
        except InviteHashExpired:
            await bot.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)

    # getting message
    elif "https://t.me/" in message.text:

        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try: 
            toID = int(temp[1].strip())
        except: 
            toID = fromID

        for msgid in range(fromID, toID+1):

            # private
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])

                if acc is None:
                    await bot.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                    return

                try:
                    await handle_private(message, chatid, msgid)
                    await asyncio.sleep(3)  # Pause for 5 seconds after each message or file
                except Exception as e:
                    await bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # bot
            elif "https://t.me/b/" in message.text:
                username = datas[4]

                if acc is None:
                    await bot.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                    return

                try: 
                    await handle_private(message, username, msgid)
                    await asyncio.sleep(3)  # Pause for 5 seconds after each message or file
                except Exception as e: 
                    await bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # public
            else:
                username = datas[3]

                try: 
                    msg = await bot.get_messages(username, msgid)
                except pyrogram.errors.UsernameNotOccupied: 
                    await bot.send_message(message.chat.id, f"**The username is not occupied by anyone**", reply_to_message_id=message.id)
                    return

                try: 
                    await bot.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                    await asyncio.sleep(3)  # Pause for 5 seconds after each message or file
                except Exception as e:
                    if acc is None:
                        await bot.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                        return
                    try: 
                        await handle_private(message, username, msgid)
                        await asyncio.sleep(3)  # Pause for 5 seconds after each message or file
                    except Exception as e: 
                        await bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)



# Function to handle private messages
def handle_private(message: pyrogram.types.messages_and_media.message.Message, chatid: int, msgid: int):
    global given_thumbnail, words_to_remove_from_filename, url_count
    global words_to_replace_in_caption, watermark_url_remove, watermark_url_add, watermark_text
    
    try:
        msg: pyrogram.types.messages_and_media.message.Message = acc.get_messages(chatid, msgid)
        msg_type = get_message_type(msg)

        if given_thumbnail == "random":
            # If the message type is video, extract a random frame and use it as thumbnail
            if "Video" == msg_type:
                file = acc.download_media(msg, progress=progress, progress_args=[message, "down"])
                random_frame_path = extract_random_frame(file, "random_frame.jpg")
                thumb = random_frame_path
                os.remove(file)  # Remove the downloaded video file after extracting the frame
            else:
                thumb = None
        elif given_thumbnail != "not_set":
            thumb = given_thumbnail
        else:
            thumb = "https://te.legra.ph/file/f27cb5bf52c22aed11984.jpg"
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb = "thumb.jpg"

        modified_filename = None  # Initialize modified_filename variable

        if "Text" == msg_type:
            bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
            return

        smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
        dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
        dosta.start()
        file = acc.download_media(msg, progress=progress, progress_args=[message, "down"])
        os.remove(f'{message.id}downstatus.txt')

        upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
        upsta.start()

        # Modify the file name before sending
        filename, file_extension = os.path.splitext(file)
        modified_filename = f"{filename}Kunal{file_extension}"

        # Remove specific words from the file name
        words_to_remove = words_to_remove_from_filename  # Add the words you want to remove
        for word in words_to_remove:
            modified_filename = modified_filename.replace(word, "")

        os.rename(file, modified_filename)
        
        # Replace specific words in the caption
        caption = msg.caption if msg.caption else ""
        for word, replacement in words_to_replace_in_caption.items():
            caption = caption.replace(word, replacement)

        # Remove specific words from the caption
        for word in words_to_remove_from_filename:
            caption = caption.replace(word, "")

        # Set URL count limit based on media type
        if "Document" == msg_type or "Photo" == msg_type or "Audio" == msg_type:
            url_limit = 10
        elif "Video" == msg_type:
            url_limit = 50

        # Increment URL count
        url_count += 1
        # Check if URL count is divisible by the limit
        if url_count % url_limit == 0:
            # Initiate flood wait (5 minutes)
            time.sleep(300)

        # Send the media
        if "Document" == msg_type:
            bot.send_document(message.chat.id, modified_filename, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        elif "Video" == msg_type:
            if watermark_text:
                # Add text watermark for initial 30 seconds
                output_path = f"{os.path.splitext(modified_filename)[0]}_with_text_watermark.mp4"
                add_text_watermark_for_initial_duration(modified_filename, watermark_text, output_path)

                # Send the video back
                bot.send_video(message.chat.id, output_path, thumb=thumb, caption=caption, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

                # Cleanup
                os.remove(output_path)
                watermark_text = None  # Reset the watermark text
            elif watermark_url_remove:
                # Remove watermark
                output_path = f"{os.path.splitext(modified_filename)[0]}_no_watermark.mp4"
                remove_watermark(modified_filename, watermark_url_remove, output_path)

                # Send the video back
                bot.send_video(message.chat.id, output_path, thumb=thumb, caption="Watermark removed!", duration=msg.video.duration, width=msg.video.width, height=msg.video.height, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

                # Cleanup
                os.remove(watermark_url_remove)
                os.remove(output_path)
                watermark_url_remove = None  # Reset the watermark URL
            elif watermark_url_add:
                # Add image watermark for initial 30 seconds
                output_path = f"{os.path.splitext(modified_filename)[0]}_with_watermark.mp4"
                add_watermark(modified_filename, watermark_url_add, output_path)

                # Send the video back
                bot.send_video(message.chat.id, output_path, thumb=thumb, caption=caption, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

                # Cleanup
                os.remove(watermark_url_add)
                os.remove(output_path)
                watermark_url_add = None  # Reset the watermark URL
            else:
                bot.send_video(message.chat.id, modified_filename, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        elif "Audio" == msg_type:
            bot.send_audio(message.chat.id, modified_filename, duration=msg.audio.duration, performer=msg.audio.performer, title=msg.audio.title, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        elif "Photo" == msg_type:
            bot.send_photo(message.chat.id, modified_filename, thumb=thumb, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        # Add more elif conditions for other message types here...

        # Cleanup
        if os.path.exists(file):  # Check if the original file exists before removal
            os.remove(file)  # Remove the original file
        if os.path.exists(modified_filename):
            os.remove(modified_filename)  # Remove the modified file if it exists
        if os.path.exists(f'{message.id}upstatus.txt'):
            os.remove(f'{message.id}upstatus.txt')
        bot.delete_messages(message.chat.id, [smsg.id])
        
    except MessageEmpty:
        pass


# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
	try:
		msg.document.file_id
		return "Document"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

	try:
		msg.animation.file_id
		return "Animation"
	except: pass

	try:
		msg.sticker.file_id
		return "Sticker"
	except: pass

	try:
		msg.voice.file_id
		return "Voice"
	except: pass

	try:
		msg.audio.file_id
		return "Audio"
	except: pass

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.text
		return "Text"
	except: pass

# infinty polling
bot.run()
