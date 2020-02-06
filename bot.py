import cfg
import json
import time
import random
from telethon import TelegramClient, events, sync
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# TODO ChatNet Bot
# 2 - train on Fabio, Thomas, with auto training function
#	that saves people whose history has already  been trained.
# 	so it wont retrain the Net

# Chat bot instance
chatbot = ChatBot('Majra')
trainer = ChatterBotCorpusTrainer(chatbot)
# For Training easy, array of strings, dialogs & conversations

start = time.time()
trainer.train('./convos/fabio.json')
end = time.time()
print("Trainer completed in {}".format(end-start))


# Una funzione interessante è
# Non rispondere subito, come faccio di solito,
# markare as read, il messaggio appena viene arrivato
# time sleep per 3 minuti,
# se entro 3 minuti l'ultimo messaggio non è da parte mia
# allora parte un messaggio di: ti rispondo alle XX:YY
# con XX l'ora prossima +1, e YY a 00
# cosi che ogni Ora io debba controllare e rispondere a tutti i messaggi,
# e inviare a me stesso l'ultimo task piu importante da fare a quell'ora

with TelegramClient('name', cfg.api_id, cfg.api_hash) as client:
    client.send_message('me', "AI online")

    # Global handler
    @client.on(events.NewMessage())
    async def handle(event):
        m = event.message
        # print Example: Message(id, to_id=user_id=135605474), out=True, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, from_id=135605474, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[], views=None, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[])
        # print("{} -from {} -to {} -reply_to {} -date: {}".format(m.message, m.from_id, m.to_id.user_id, m.reply_to_msg_id, m.date))

        # reply to me only (Saved Messages Chat)
        # Abilitate list of users
        if m.from_id == ''
        if m.from_id == m.to_id.user_id or m.from_id in cfg.test_users.values():
            response = chatbot.get_response(m.message)
            print("Message:", m.message, "Response:",
                  response.text, m.from_id, response.confidence)
            text = "{} {} {} {} {} {}".format(
                "Message:", m.message, "Response:", response.text, m.from_id, response.confidence)
            await client.send_message('me', text)
            # Give a human feel of reply time
            # time.sleep(random.choice([3,6,9,12,24,48]))
            if 0.4 < response.confidence:
                await client.send_message(m.from_id, response.text)

        else:
            print("Response:")
            response = chatbot.get_response(m.message)
            if 0.5 < response.confidence:
                print(response, type(response))
                await client.send_message('me', "Response to: {}\n\nAI: {}".format(m.message, response.text))

        trainer.export_for_training('./last_export.json')

    ''' *** Production Handlers *** '''

    ''' AI Off shortcut '''
    @client.on(events.NewMessage(pattern='/off'))
    async def off(event):
        if event.message.from_id == cfg.id['my']:
            await client.disconnect()

    ''' Shortcut per chiedere ai coinqui se sono a casa '''
    @client.on(events.NewMessage(pattern='/seiacasa'))
    async def seiacasa(event):
        if event.message.from_id == cfg.id['my']:
            await client.send_message(cfg.id['ludo'], "Sei a casa?")
            await client.send_message(cfg.id['fabio'], "Sei a casa?")

    ''' Handler for audio from utubebot '''
    @client.on(events.NewMessage())
    async def utubebot(event):
        m = event.message
        # Ho aggiunto
        if m.from_id == cfg.id['utubebot'] and m.to_id == cfg.id['my'] and m.media != None:
            await m.forward_to(-1001305351596)
            return

    # END of the cycle
    client.run_until_disconnected()
