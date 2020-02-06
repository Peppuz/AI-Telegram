import json
import cfg
from telethon import TelegramClient, events, sync

"""
This module should save all Messages from a telegram chat, to an array of arrays like [[ question, answer ], ...]

It sounds easy like that, but in order to get a single message of the two talking, we have to check who is speaking,
so that a single string of messages, splitted by a \n, can be a single input, making the bot much smarter

"""

api_id = 33528
api_hash = '8039a0d97409386574e7c73919906924'

conversations = {"conversations": []}
a, b, prev_speaking = False, False, False
mess = []


def enc(stringa):
    print("String:", stringa, type(stringa))
    return str(stringa)

with TelegramClient('name', api_id, api_hash) as client:
    with open('./convos/fabio.json', 'w') as targ:
        # Salva tutta la conversazione in un array di messaggi
        for message in client.iter_messages(cfg.id['fabio']):
            mess.append(message)

        # Inverto l'ordine dei messaggi, dal piu vecchio al piu nuovo.
        mess.reverse()

        for message in mess:
            # caso base, primo elemento
            print(prev_speaking, "|", "A", a, "|", "B", b, "|", message.text)
            if not prev_speaking:
                a = enc(message.text)
                prev_speaking = message.from_id
                continue

            if message.text == "" or message.text == None:
                continue

            # A sta parlando - quindi lo lascio finire di parlare
            if a is not False and \
                    not b and \
                    prev_speaking == message.from_id:
                a += "\n" + enc(message.text)
                continue

            # A ha finito di parlare - B ha iniziato
            if a and not b and \
                    prev_speaking != message.from_id:
                prev_speaking = message.from_id
                b = enc(message.text)
                continue

            if a is not False and \
                b is not False and \
                prev_speaking == message.from_id:
                b += "\n" + enc(message.text)
                continue

            # A e B hanno concluso la botta e risposta, dovrebbe ripartire A a parlare
            if a != False and b != False and message.from_id != prev_speaking:
                conversations["conversations"].append([a, b])
                a, b, prev_speaking=False, False, False

        # Export the whole conversation as standard Corpus Conversation
        print(conversations)

        json.dump(conversations, targ)
