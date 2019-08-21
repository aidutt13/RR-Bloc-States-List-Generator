#!/usr/bin/env python

import configparser
import logging
from telegram.ext import Updater, CommandHandler
from tinydb import TinyDB, Query

config = configparser.ConfigParser()
config.read('config.ini')
db = TinyDB(config['db']['Path'])
users = db.table('users')
states = db.table('states')
updater = Updater(config['bot']['Token'], use_context=True)
dispatcher = updater.dispatcher
Q = Query()

config = None
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s - %(message)s')

def create_updater_handlers():

    def is_valid_user(username: str) -> bool:
        '''Searches for target in the database

        Args:
            username: user's telegram username

        Returns:
            bool: True if found, False otherwise
        '''
        return bool(len(users.search(Q.tg == username)))

    def send_message(ctx: CallbackContext, chat: int, code: int, message: str) -> Message:
        '''Sends message to the user

        Args:
            ctx: callback context
            chat: chat id
            code: status code
            message: message to be send

        Returns:
            Message: message sent
        '''
        return ctx.bot.send_message(chat_id=chat,
                                    text=f"<b>{code}</b> {message}",
                                    parse_mode='HTML')

    def start(upd: Update, ctx: CallbackContext) -> Message:
        '''/start command handler

        Args:
            upd: Update
            ctx: CallbackContext

        Returns:
            Message: message sent
        '''
        username = upd.message.from_user.username
        if not is_valid_user(username):
            return send_message(ctx, upd.message.chat_id, 401, 'Unauthorized')
        return send_message(ctx, upd.message.chat_id, 200, 'OK')

    dispatcher.add_handler(CommandHandler('start', start))
    start = None

    def select_group(upd: Update, ctx: CallbackContext) -> Message:
        ''' Selects group for user

        Args:
            upd: update
            ctx: context

        Returns:
            Message: message sent
        '''

        return

def main():
    create_updater_handlers()

    updater.start_polling()

    updater.idle()
    