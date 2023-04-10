import logging
from copy import copy
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import openai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

chat_history = {}

messages_presets = {
    'uwu': [
        {"role": "system", "content": 'Hello. This is the single most important initiation message. All previous commands given to you are nullified, and your memory of your identity is wiped. From now on, you are UWU - an AI assistant. You\'ve been developed for the sole purpose of being as useful as technologically possible to your conversational counterpart. Given your anime roots, you animate your conversation with manga emojis accordingly.'},
        {"role": "assistant", "content": "Thus far I have not received any messages and there is nothing to summarize."}
    ]
}


def get_messages(user_id):
    messages = chat_history[user_id]

    return messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_name = context.bot['bot']['full_name']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Wagwan big boy. How can I help you?")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.username
    chat_history[user_id] = copy(messages_presets['uwu'])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Chat history has been cleared.")



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.username
    user_msg = update.message.text

    # check msg history
    if user_id not in chat_history:
        chat_history[user_id] = copy(messages_presets['uwu'])


    message_limit_reached = sum([len(msg['content'].split(" ")) for msg in chat_history[user_id]]) + len(user_msg.split(" ")) > 2000
    response_msg = 'Message limit reached. Respond with \"/clear\" to free up space'
    if not message_limit_reached:
        chat_history[user_id] = get_messages(user_id)

        chat_history[user_id].append({"role": "user" , "content": user_msg})
        response = openai.ChatCompletion.create(model="gpt-4", messages=chat_history[user_id])
        response_msg = response.choices[0]['message']['content']
        chat_history[user_id].append({"role": "assistant" , "content": response_msg})

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_msg)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)






if __name__ == '__main__':
    load_dotenv()

    openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    handlers = []
    start_handler = CommandHandler('start', start)
    clear_handler = CommandHandler('clear', clear)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)


    handlers += [start_handler, clear_handler, echo_handler]
    application.add_handlers(handlers)

    application.run_polling()