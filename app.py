from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from telegram.error import BadRequest
from datetime import datetime, timedelta
import json

# Bot Token (Replace with your actual bot token)
BOT_TOKEN = '7725382947:AAGpLJhSaD7KCi1-zPpvIqduArpic_hPEJI'

# Channel and group IDs
CHANNEL_ID1 = "@binarytradinghouse"
CHANNEL_ID2 = "@RefergEarnofflcial"
CHANNEL_ID3 = "@yourmt4guru"
CHANNEL_ID4 = "@S_S_GURU"
CHANNEL_ID5 = "@INDICATOR_GURU1"
CHANNEL_ID6 = "@SOURCECODEGURU"
CHANNEL_ID7 = "@SABROTHERTRADER"
CHANNEL_ID8 = "@annaziyyahfoundation"



WITHDRAW_GROUP_ID = "@IGWithdrawal"

# File for storing user data
USER_DATA_FILE = "user_data.json"

# Load and save functions
def load_users():
    """Load user data from a JSON file."""
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users():
    """Save user data to a JSON file."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)


# Global in-memory data
users = load_users()


def get_user(user_id):
    """Retrieve or create a user entry."""
    if user_id not in users:
        users[user_id] = {"balance": 5, "referrals": 0, "wallet": None, "joined_at": datetime.now().isoformat()}
        save_users()
    return users[user_id]



# Bonus data
user_bonuses = {}
BONUS_AMOUNT = 1  # Tokens per claim
BONUS_COOLDOWN = timedelta(hours=12)  # Cooldown time for claiming bonus


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    
    # Store referrer in user data for later verification
    if context.args and context.args[0].isdigit() and context.args[0] != str(user_id):
        user_data = get_user(user_id)
        user_data["pending_referrer"] = context.args[0]
        save_users()

    # Initialize user
    get_user(user_id)

    # Welcome message
    message = (
        "Hi! 😊 Welcome to the Refer & Earn Bot.\n\n"
        "🎉 5 BDT for completing tasks\n"
        "🎉 5 BDT for each referral\n\n"
        "By participating, you agree to the Terms and Conditions."
    )
    keyboard = [[InlineKeyboardButton("💸 Earn", callback_data="join_airdrop")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


# Handle join airdrop
async def join_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    message = (
        "📋 Join Refer & Earn Bot Channel:\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "1. Join Channel [Click Here](https://t.me/binarytradinghouse)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "2. Join Channel [Click Here](https://t.me/INDICATOR_GURU1)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "3. Join Channel [Click Here](https://t.me/S_S_GURU)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "4. Join Channel [Click Here](https://t.me/SABROTHERTRADER)\n"
        "━━━━━━━━━━━━━━━━━\n"

        "5. Join Channel [Click Here](https://t.me/SOURCECODEGURU)\n"
        "━━━━━━━━━━━━━━━━━\n"


        
        "6. Join Channel [Click Here](https://t.me/yourmt4guru)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "7. Join Channel [Click Here](https://t.me/annaziyyahfoundation)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "8. Join Channel [Click Here](https://t.me/RefergEarnofflcial)\n"
        "━━━━━━━━━━━━━━━━━\n"
        
        "9. Subscribe [Click Here](https://www.youtube.com/@INDICATOR_GURU)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "10. Subscribe [Click Here](https://www.youtube.com/@SOURCE_CODE_GURU)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "11. Subscribe [Click Here](https://www.youtube.com/@YOURMT4GURU)\n"
        "━━━━━━━━━━━━━━━━━\n"
        "12. Subscribe [Click Here](https://www.youtube.com/@S_SGURU)\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "After completing the tasks, click ✅ Check."
    )
    keyboard = [[InlineKeyboardButton("✅ Check", callback_data="check_tasks")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode="Markdown")


# Validate tasks
async def check_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = str(query.from_user.id)
    user_data = get_user(user_id)

    try:
        # Check membership in all 8 channels
        statuses = []
        for channel in [CHANNEL_ID1, CHANNEL_ID2, CHANNEL_ID3, CHANNEL_ID4, CHANNEL_ID5, CHANNEL_ID6, CHANNEL_ID7, CHANNEL_ID8]:
            status = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            statuses.append(status.status in ["member", "administrator", "creator"])

        if all(statuses):
            # Process pending referral if exists
            user_data = get_user(user_id)
            if "pending_referrer" in user_data:
                referrer = user_data["pending_referrer"]
                referrer_data = get_user(referrer)
                referrer_data["referrals"] += 1
                referrer_data["balance"] += 5  # Reward for referral
                del user_data["pending_referrer"]
                save_users()
                await context.bot.send_message(
                    chat_id=referrer,
                    text="🎉 Congratulations! You got 5 BDT for a new referral!"
                )
            
            # Verified tasks
            await query.edit_message_text("🚀 Tasks verified! Thank you for joining.")

            # Display menu
            menu_keyboard = [
                ["🏆 Balance", "🏧 Withdrawal"],
                ["🏅 Refer & Earn", "📊 Leaderboard"],
                ["📞 Contacts", "🎁 Bonus"]
            ]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
            await context.bot.send_message(chat_id=user_id, text="✅ Menu loaded.", reply_markup=menu_markup)
        else:
            await query.edit_message_text("❌ Please join the channel and click the ✅ Check button. /start")

    except BadRequest:
        await query.edit_message_text("❌ Please join the channel and click the ✅ Check button. /start")


# Handle balance
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    user_data = get_user(user_id)
    await update.message.reply_text(
        f"🎉 Your Current Balance: {user_data['balance']} ৳BDT  \n\n"
        f"👥 Total Referrals: {user_data['referrals']}"
    )


# Handle withdrawal
async def withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    user_data = get_user(user_id)

    if user_data["balance"] < 20:
        await update.message.reply_text("❌ Minimum withdrawal is 20 BDT.")
        return

    # Request wallet address and amount for withdrawal
    await update.message.reply_text("✅ Please send your bKash number followed by the withdrawal amount, e.g., 'number 20'.")

    return


# Handle wallet address and amount input for withdrawal
async def handle_wallet_address_and_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    user_data = get_user(user_id)
    user_input = update.message.text.strip()

    # Split input into wallet address and amount
    parts = user_input.split()

    if len(parts) != 2:
        await update.message.reply_text("❌ Please send your bKash number and the amount, e.g., 'number 20'.")
        return

    wallet_address = parts[0]
    try:
        amount = float(parts[1])  # Convert the second part to float (amount)
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid amount (numeric).")
        return

    if amount <= 0:
        await update.message.reply_text("❌ Withdrawal amount must be greater than 20.")
        return

    # Check if the user has sufficient balance
    if user_data["balance"] < amount:
        await update.message.reply_text(f"❌ You do not have enough balance for this withdrawal. Your current balance is {user_data['balance']} BDT.")
        return

    # Deduct the withdrawal amount
    user_data["balance"] -= amount
    save_users()  # Persist changes

    # Send withdrawal request to the admin group
    request_time = datetime.now().strftime("%d.%m.%y - %I:%M%p")
    await context.bot.send_message(
    chat_id=WITHDRAW_GROUP_ID,
    text=f"┏━━━━━━━━❰💰❱━━━━━━━━┓\n"
         f"         𝚆𝚒𝚝𝚑𝚍𝚛𝚊𝚠𝚊𝚕 𝚁𝚎𝚚𝚞𝚎𝚜𝚝\n"
         f"┗━━━━━━━━❰💰❱━━━━━━━━┛\n\n"
         f"🧑‍💻 𝚄𝚜𝚎𝚛𝚗𝚊𝚖𝚎 -» @{update.effective_user.username}\n\n"
         f"💼 𝚆𝚊𝚕𝚕𝚎𝚝 -» {wallet_address}\n\n"
         f"⏰ 𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝚃𝚒𝚖𝚎 -» {request_time}\n\n"
         f"💸 𝙰𝚖𝚘𝚞𝚗𝚝 -» {amount} IG 𝚃𝚘𝚔𝚎𝚗𝚜\n\n"
         f"┏━━━━━━━━❰✅❱━━━━━━━━┓\n"
         f"        𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕\n"
         f"┗━━━━━━━━❰✅❱━━━━━━━━┛"
)




    # Confirm the withdrawal
    await update.message.reply_text(f"✅ Withdrawal request of {amount} BDT sent successfully to {wallet_address}!")


# Handle referral link
async def refer_and_earn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    referral_link = f"https://t.me/Refer_to_Earn_Bkash_Bot?start={update.effective_user.id}"
    await update.message.reply_text(
        f"You Can Earn More 5 BDT Through Our Referral System. You Will Earn 5 BDT For Each Valid Referral.\n\n"
        f"🔗 Referral Link: {referral_link})\n\n"
        f"💸 Share This Link To Earn BDT:"
    )



# Leaderboard
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Sort users by referrals in descending order
    sorted_users = sorted(users.items(), key=lambda x: x[1]["referrals"], reverse=True)

    # Format leaderboard with proper escaping
    leaderboard_text = (
        "🏆 *BDT Member Leaderboard*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    )

    if sorted_users:
        medals = ["🥇", "🥈", "🥉"]  # Top 3 medals
        for rank, (user_id, data) in enumerate(sorted_users[:10], start=1):
            medal = medals[rank-1] if rank <= 3 else "🎖️"  # Assign medals
            leaderboard_text += f"{medal} *{user_id}* → `{data['referrals']}` Referrals\n"

        leaderboard_text += "━━━━━━━━━━━━━━━━━━━━━━\n"
        leaderboard_text += "🔥 Keep referring to climb the ranks\\! 🔥"
    else:
        leaderboard_text += "No Referrals yet\\. Be the first to refer\\! 🚀"

    # Send formatted message
    await update.message.reply_text(leaderboard_text, parse_mode="MarkdownV2")




# Contacts
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("For personal issues, bugs, mistakes - contact us: @INDICATORGURU2")



# Bonus command
async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    current_time = datetime.now()

    # Check if the user has claimed a bonus today
    if user_id in user_bonuses and current_time - user_bonuses[user_id] < BONUS_COOLDOWN:
        remaining_time = BONUS_COOLDOWN - (current_time - user_bonuses[user_id])
        hours, minutes = divmod(remaining_time.seconds // 60, 60)
        await update.message.reply_text(
            f"⏳ You have already claimed your bonus today!\n"
            f"Come back in {hours}h {minutes}m to claim again. 🚀"
        )
    else:
        # Update last claim time
        user_bonuses[user_id] = current_time

        # Add bonus tokens to the user's account
        user_data = get_user(user_id)
        user_data["balance"] += BONUS_AMOUNT
        save_users()

    await update.message.reply_text(
    f"*🎉 Congratulations\\! You received {BONUS_AMOUNT} BDT\\!*\\"
    "*🔥 Keep earning by referring your friends\\!*",
    parse_mode="MarkdownV2"
)




# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(join_airdrop, pattern="join_airdrop"))
    app.add_handler(CallbackQueryHandler(check_tasks, pattern="check_tasks"))

    app.add_handler(MessageHandler(filters.Regex("^🏆 Balance$"), balance))
    app.add_handler(MessageHandler(filters.Regex("^🏧 Withdrawal$"), withdrawal))

    app.add_handler(MessageHandler(filters.Regex("^🏅 Refer & Earn$"), refer_and_earn))
    app.add_handler(MessageHandler(filters.Regex("^📞 Contacts$"), contacts))
    app.add_handler(MessageHandler(filters.Regex("^📊 Leaderboard$"), leaderboard))
    app.add_handler(MessageHandler(filters.Regex("^🎁 Bonus$"), bonus))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_address_and_amount))  # Handle wallet 

    app.run_polling()


if __name__ == "__main__":
    main()
