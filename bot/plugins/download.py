import os
import lk21
import requests, cfscrape
from lk21.extractors.bypasser import Bypass
from time import sleep
from js2py import EvalJs
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl
from bot.helpers.gdrive_utils import GoogleDrive 
from bot.config import Config
from bot import LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError

def is_gdtot_link(url: str):
    url = re.match(r'https?://.*\.gdtot\.\S+', url)
    return bool(url)

cookies = {"PHPSESSID": PHPSESSID, "crypt": CRYPT}


@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
  user_id = message.from_user.id
  if not message.media:
    sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
    if message.command:
      link = message.command[1]
    else:
      link = message.text
    if 'drive.google.com' in link:
      sent_message.edit(Messages.CLONING.format(link))
      LOGGER.info(f'Copy:{user_id}: {link}')
      msg = GoogleDrive(user_id).clone(link)
      sent_message.edit(msg)
    elif 'mediafire.com' in link:
      """ MediaFire """
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{Config.DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = Config.DOWNLOAD_DIRECTORY
      try:
         link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
      except IndexError:
         return sent_message.edit("No MediaFire links found\nMight Be File/Files Deleted. \nOpen The Link And Check")
      page = BeautifulSoup(requests.get(link).content, 'lxml')
      info = page.find('a', {'aria-label': 'Download file'})
      link = info.get('href')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        # LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
    elif 'zippyshare.com' in link:
      """ ZippyShare """
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{Config.DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = Config.DOWNLOAD_DIRECTORY
      try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
      except IndexError:
        raise DirectDownloadLinkException("No Zippyshare links found")
      try:
        base_url = re.search('http.+.zippyshare.com', link).group()
        response = requests.get(link).content
        pages = BeautifulSoup(response, "lxml")
        try:
            js_script = pages.find("div", {"class": "center"}).find_all("script")[1]
        except IndexError:
            js_script = pages.find("div", {"class": "right"}).find_all("script")[0]
        js_content = re.findall(r'\.href.=."/(.*?)";', str(js_script))
        js_content = 'var x = "/' + js_content[0] + '"'
        evaljs = EvalJs()
        setattr(evaljs, "x", None)
        evaljs.execute(js_content)
        js_content = getattr(evaljs, "x")
        link = base_url + js_content
      except IndexError:
        raise sent_message.edit("ERROR: Can't find download button")
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        # LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
    elif 'anonfiles.com' in link:
      """ Anonfiles """
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{Config.DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = Config.DOWNLOAD_DIRECTORY
      bypasser = lk21.Bypass()
      link = bypasser.bypass_anonfiles(link)
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        # LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
    elif 'bayfiles.com' in link:
      """ Bayfiles """
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{Config.DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = Config.DOWNLOAD_DIRECTORY
      bypasser = lk21.Bypass()
      link = bypasser.bypass_anonfiles(link)
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        # LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
    elif 'racaty.net' in link:
      """ Racaty """
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{Config.DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = Config.DOWNLOAD_DIRECTORY
      dl_url = ''
      try:
         link = re.findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
      except IndexError:
        raise ("No Racaty links found\n")
      scraper = cfscrape.create_scraper()
      r = scraper.get(url)
      soup = BeautifulSoup(r.text, "lxml")
      op = soup.find("input", {"name": "op"})["value"]
      ids = soup.find("input", {"name": "id"})["value"]
      rpost = scraper.post(url, data = {"op": op, "id": ids})
      rsoup = BeautifulSoup(rpost.text, "lxml")
      dl_url = rsoup.find("a", {"id": "uniqueExpirylink"})["href"].replace(" ", "%20")
      link =  dl_url
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))

    # elif '1fichier.com' in link:
    elif 'ouo.press' in link or 'ouo.io' in link:
      """ Ouo Bypass """
      bypasser = lk21.Bypass()
      link = bypasser.bypass_ouo(link)
      sent_message.edit(f"Bypassed The Ouo Link That U Provided.\n\nLink = `{link}`")

    # elif is_gdtot_link(link):
      
    else:
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{Config.DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = Config.DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))


@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video | filters.photo) & CustomFilters.auth_users)
def _telegram_file(client, message):
  user_id = message.from_user.id
  sent_message = message.reply_text('🕵️**Checking File...**', quote=True)
  if message.document:
    file = message.document
  elif message.video:
    file = message.video
  elif message.audio:
    file = message.audio
  elif message.photo:
  	file = message.photo
  	file.mime_type = "images/png"
  	file.file_name = f"IMG-{user_id}-{message.message_id}.png"
  sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))
  LOGGER.info(f'Download:{user_id}: {file.file_id}')
  try:
    file_path = message.download(file_name=Config.DOWNLOAD_DIRECTORY)
    sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
    msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
    sent_message.edit(msg)
  except RPCError:
    sent_message.edit(Messages.WENT_WRONG)
  LOGGER.info(f'Deleteing: {file_path}')
  os.remove(file_path)

@Client.on_message(filters.incoming & filters.private & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
def _ytdl(client, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    sent_message = message.reply_text('🕵️**Checking Link...**', quote=True)
    link = message.command[1]
    LOGGER.info(f'YTDL:{user_id}: {link}')
    sent_message.edit(Messages.DOWNLOADING.format(link))
    result, file_path = utube_dl(link)
    if result:
      sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
      msg = GoogleDrive(user_id).upload_file(file_path)
      sent_message.edit(msg)
      LOGGER.info(f'Deleteing: {file_path}')
      os.remove(file_path)
    else:
      sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
  else:
    message.reply_text(Messages.PROVIDE_YTDL_LINK, quote=True)
