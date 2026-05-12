import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY, GROQ_API_KEY, WELCOME_MESSAGE, HELP_MESSAGE, ERROR_MESSAGES
from user_manager import UserManager
from story_manager import StoryManager
from ai_provider import AIProvider

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize managers
user_manager = UserManager()
story_manager = StoryManager("stories.json")
ai_provider = AIProvider(ANTHROPIC_API_KEY, GROQ_API_KEY)

# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    user_manager.get_user(user_id)
    await update.message.reply_text(WELCOME_MESSAGE)
    logger.info(f"User {user_id} started bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(HELP_MESSAGE)


async def stories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stories command - Show available stories"""
    stories = story_manager.get_all_stories()
    keyboard = [
        [InlineKeyboardButton(story["name"], callback_data=f"story_{story['id']}")]
        for story in stories
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "အဖြစ်အပျက်များကို ရွေးချယ်ပါ (Select a story):",
        reply_markup=reply_markup
    )


async def story_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle story selection"""
    query = update.callback_query
    user_id = query.from_user.id
    story_id = query.data.replace("story_", "")
    
    # Get story details
    story = story_manager.get_story(story_id)
    if not story:
        await query.answer(ERROR_MESSAGES["invalid_story"], show_alert=True)
        return
    
    # Set user's story
    user_manager.set_story(user_id, story_id)
    
    # Send initial message
    await query.answer()
    await query.edit_message_text(
        text=f"✅ {story['name']} ကိုရွေးချယ်ပြီးပါပြီ။\n\n{story_manager.get_initial_message(story_id)}"
    )
    
    logger.info(f"User {user_id} selected story: {story_id}")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    user_id = update.effective_user.id
    nsfw_status = user_manager.get_nsfw_mode(user_id)
    
    keyboard = [
        [InlineKeyboardButton(
            f"NSFW Mode: {'✅ ON' if nsfw_status else '❌ OFF'}",
            callback_data="toggle_nsfw"
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "ကွယ်မြုံချက်များ (Settings):",
        reply_markup=reply_markup
    )


async def nsfw_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle NSFW toggle"""
    query = update.callback_query
    user_id = query.from_user.id
    
    new_status = user_manager.toggle_nsfw(user_id)
    
    await query.answer()
    await query.edit_message_text(
        text=f"NSFW Mode: {'✅ ON' if new_status else '❌ OFF'}"
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command - Reset memory and story"""
    user_id = update.effective_user.id
    user_manager.clear_user_session(user_id)
    await update.message.reply_text(
        "✅ သည်စုံ ရှင်းလင်းပြီးပါပြီ။\n/stories မှ သုံးသူမ အဖြစ်အပျက် ရွေးချယ်ပါ။"
    )
    logger.info(f"User {user_id} cleared session")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # Check if user has selected a story
    current_story = user_manager.get_story(user_id)
    if not current_story:
        await update.message.reply_text(
            "အရင်သုံးသူမ အဖြစ်အပျက် ရွေးချယ်ပါ။ /stories ကိုအသုံးပြုပါ။"
        )
        return
    
    # Get story system prompt
    system_prompt = story_manager.get_system_prompt(current_story)
    
    # Add user message to history
    user_manager.add_message(user_id, "user", user_text)
    
    # Get conversation history
    history = user_manager.get_conversation_history(user_id)
    
    # Get AI response
    try:
        response = ai_provider.get_response(
            system_prompt=system_prompt,
            conversation_history=history,
            max_tokens=1024,
            temperature=0.7
        )
        
        # Add assistant message to history
        user_manager.add_message(user_id, "assistant", response)
        
        # Send response
        await update.message.reply_text(response)
        logger.info(f"Response sent to user {user_id}")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(ERROR_MESSAGES["api_error"])


def main():
    """Main function to start the bot"""
    
    # Check for required tokens
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in .env")
        return
    
    if not ANTHROPIC_API_KEY and not GROQ_API_KEY:
        logger.error("❌ No API keys found. Need either ANTHROPIC_API_KEY or GROQ_API_KEY")
        return
    
    # Test AI connections
    if not ai_provider.test_connection():
        logger.warning("⚠️ Warning: Could not connect to any AI provider")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stories", stories_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("clear", clear_command))
    
    # Add callback query handlers
    application.add_handler(CallbackQueryHandler(story_callback, pattern="^story_"))
    application.add_handler(CallbackQueryHandler(nsfw_callback, pattern="^toggle_nsfw$"))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("🤖 Burmese AI Roleplay Bot Started...")
    logger.info("📱 Bot is running. Send /start to begin")
    
    application.run_polling()


if __name__ == '__main__':
    main()
