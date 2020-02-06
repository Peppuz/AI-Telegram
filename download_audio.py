import cfg
from telethon import TelegramClient, events, sync

with TelegramClient('name', cfg.api_id, cfg.api_hash) as client:
    client.send_message('me', "AI online")

    for message in client.iter_messages(311495487, limit=1):
        id = message.media.document.id
        client.download_file(open('here.ogg', 'w+'), id)