import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states
CHOOSING, ENGLISH, WEBSITE, TELEGRAM_BOT, GET_CONTACT = range(5)

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['English Classes', 'Website Development', 'Telegram Bot Development']]
    
    await update.message.reply_text(
        'Hi! I am Dilmurod Nurkhonov. How can I help you today?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    
    return CHOOSING

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data['choice'] = text
    
    if text == 'English Classes':
        reply_keyboard = [['Beginner', 'Intermediate', 'Advanced']]
        await update.message.reply_text(
            'Please choose your level:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return ENGLISH
    elif text == 'Website Development':
        await update.message.reply_text('Please provide a description of the website you want:')
        return WEBSITE
    elif text == 'Telegram Bot Development':
        await update.message.reply_text('Please provide a description of the bot you want:')
        return TELEGRAM_BOT

async def english(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    level = update.message.text
    context.user_data['level'] = level
    contact_button = KeyboardButton(text="Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
    await update.message.reply_text('Please share your contact information by clicking the button below.', reply_markup=reply_markup)
    return GET_CONTACT

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    description = update.message.text
    context.user_data['description'] = description
    contact_button = KeyboardButton(text="Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
    await update.message.reply_text('Please share your contact information by clicking the button below.', reply_markup=reply_markup)
    return GET_CONTACT

async def telegram_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    description = update.message.text
    context.user_data['description'] = description
    contact_button = KeyboardButton(text="Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
    await update.message.reply_text('Please share your contact information by clicking the button below.', reply_markup=reply_markup)
    return GET_CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.contact
    user = update.message.from_user
    choice = context.user_data.get('choice')
    level = context.user_data.get('level', 'N/A')
    description = context.user_data.get('description', 'N/A')
    
    # Message to be sent to your Telegram account
    message = f"New request from {contact.first_name} {contact.last_name} (@{user.username}):\n"
    message += f"Phone Number: {contact.phone_number}\n"
    message += f"Choice: {choice}\n"
    if choice == 'English Classes':
        message += f"Level: {level}\n"
    else:
        message += f"Description: {description}\n"
    
    bot_token = "6800446505:AAFOblJ44b0mAxNGDWO0nHS0YsTrx64keZI"
    chat_id = "837447398"  # Replace with your chat ID
    
    await context.bot.send_message(chat_id=chat_id, text=message)
    
    await update.message.reply_text('Thank you! I will contact you soon.')
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Goodbye! Feel free to reach out if you need any help.')
    return ConversationHandler.END

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6800446505:AAFOblJ44b0mAxNGDWO0nHS0YsTrx64keZI").build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(filters.Regex('^(English Classes|Website Development|Telegram Bot Development)$'), choice)],
            ENGLISH: [MessageHandler(filters.Regex('^(Beginner|Intermediate|Advanced)$'), english)],
            WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, website)],
            TELEGRAM_BOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_bot)],
            GET_CONTACT: [MessageHandler(filters.CONTACT, get_contact)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until you press Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
