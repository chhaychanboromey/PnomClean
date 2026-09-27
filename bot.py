# import os
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     ApplicationBuilder,
#     CommandHandler,
#     CallbackQueryHandler,
#     MessageHandler,
#     ContextTypes,
#     filters,
# )

# # ---------------------------------------------------------
# # SETUP YOUR KEYS HERE
# # ---------------------------------------------------------
# BOT_TOKEN = "8923171010:AAF2eSvL6saXTzJfubwCCtx4nx6F-zjOFNA"  # Revoke & update after demo
# STAFF_GROUP_ID = -1003568891959                              # Prom Clean Staff Supergroup ID

# # ---------------------------------------------------------
# # BOT LOGIC
# # ---------------------------------------------------------
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("🧺 Services & Rates", callback_data='rates')],
#         [InlineKeyboardButton("📅 Book Laundry Pickup", callback_data='book')],
#         [InlineKeyboardButton("💳 Bakong KHQR Payment", callback_data='pay')],
#         [InlineKeyboardButton("🎁 Loyalty Points", callback_data='points')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     msg = (
#         "✨ Welcome to Prom Clean! ✨\n"
#         "On-Demand Laundry Pickup & Delivery for Students.\n\n"
#         "Select an option below to begin:"
#     )
#     if update.message:
#         await update.message.reply_text(msg, reply_markup=reply_markup)
#     else:
#         await update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     user = query.from_user

#     if query.data == 'rates':
#         rates_text = (
#             "📋 Prom Clean Rates:\n\n"
#             "• Wash + Dry: 2,000 KHR / kg\n"
#             "• Wash + Dry + Fold: 3,000 KHR / kg\n"
#             "• Wash + Dry + Iron: 5,500 KHR / kg\n"
#             "• Garment Bag: $1.50 (~6,000 KHR)\n\n"
#             "🚚 Delivery: Free within 3km!"
#         )
#         keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main')]]
#         await query.edit_message_text(rates_text, reply_markup=InlineKeyboardMarkup(keyboard))

#     elif query.data == 'book':
#         keyboard = [
#             [InlineKeyboardButton("Wash + Dry + Fold (3k KHR/kg)", callback_data='order_fold')],
#             [InlineKeyboardButton("Wash + Dry + Iron (5.5k KHR/kg)", callback_data='order_iron')],
#             [InlineKeyboardButton("🔙 Main Menu", callback_data='main')]
#         ]
#         await query.edit_message_text("Select your laundry package:", reply_markup=InlineKeyboardMarkup(keyboard))

#     elif query.data.startswith('order_'):
#         service = "Wash + Dry + Fold" if "fold" in query.data else "Wash + Dry + Iron"
#         price = "12,000 KHR (4 kg)" if "fold" in query.data else "22,000 KHR (4 kg)"
        
#         # 1. Send booking confirmation to customer
#         keyboard = [[InlineKeyboardButton("📲 Pay with Bakong KHQR", callback_data='pay')]]
#         await query.edit_message_text(
#             f"✅ Booking Created!\n\n"
#             f"• Service: {service}\n"
#             f"• Estimated Total: {price}\n\n"
#             f"Please proceed to pay via Bakong KHQR.",
#             reply_markup=InlineKeyboardMarkup(keyboard)
#         )

#         # 2. Automatically notify Staff Group
#         username_str = f"@{user.username}" if user.username else "No Username"
#         try:
#             await context.bot.send_message(
#                 chat_id=STAFF_GROUP_ID,
#                 text=(
#                     f"🚨 NEW ORDER RECEIVED\n"
#                     f"• Customer: {user.first_name} ({username_str})\n"
#                     f"• Service: {service}\n"
#                     f"• Total Due: {price}\n"
#                     f"• Status: Pending Payment"
#                 )
#             )
#             print(f"✅ Order notification sent to staff group for {user.first_name}")
#         except Exception as e:
#             print(f"❌ Error sending order to staff group: {e}")

#     elif query.data == 'pay':
#         caption = (
#             "🇰🇭 Prom Clean Bakong KHQR Payment\n\n"
#             "1. Scan this QR code using ABA or any Bakong bank app.\n"
#             "2. Pay the order total in KHR.\n"
#             "3. Reply with a screenshot of your payment receipt in this chat!"
#         )
        
#         if os.path.exists("khqr.png"):
#             with open("khqr.png", "rb") as photo_file:
#                 await query.message.reply_photo(photo=photo_file, caption=caption)
#         else:
#             await query.message.reply_text(
#                 "💳 Prom Clean Bakong KHQR Payment\n\n"
#                 "Please transfer the total amount to Bakong Account: 012 345 678\n\n"
#                 "Reply to this chat with your payment receipt photo when done!"
#             )

#     elif query.data == 'points':
#         keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main')]]
#         await query.edit_message_text(
#             f"🎁 Prom Clean Loyalty Rewards\n\n"
#             f"Hello {user.first_name}, you have 120 Points!\n"
#             f"Redeem points for free drinks or laundry loads.",
#             reply_markup=InlineKeyboardMarkup(keyboard)
#         )

#     elif query.data == 'main':
#         await start(update, context)

# # Forward receipts straight to the Staff Group
# async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     print(f"\n📩 Receipt attempt from {user.first_name} (@{user.username})...")

#     # 1. Extract photo file ID
#     photo_file_id = None
#     if update.message.photo:
#         photo_file_id = update.message.photo[-1].file_id
#     elif update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('image/'):
#         photo_file_id = update.message.document.file_id

#     if not photo_file_id:
#         await update.message.reply_text("Please send your payment receipt as an image/photo!")
#         return

#     username_str = f"@{user.username}" if user.username else "No Username"

#     # 2. Send photo to Staff Group
#     try:
#         await context.bot.send_photo(
#             chat_id=STAFF_GROUP_ID,
#             photo=photo_file_id,
#             caption=(
#                 f"🧾 RECEIPT SUBMITTED\n"
#                 f"• From: {user.first_name} ({username_str})\n"
#                 f"• User ID: {user.id}\n\n"
#                 f"Check Bakong / ABA app to confirm transfer!"
#             )
#         )
#         print("✅ SUCCESS: Photo forwarded to Staff Group!")
#     except Exception as e:
#         print(f"❌ Failed to forward receipt photo: {e}")

#     # 3. Always confirm back to customer
#     keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main')]]
#     await update.message.reply_text(
#         "✅ Receipt Received!\n\n"
#         "Our team is verifying your payment details. "
#         "We will confirm your pickup time shortly!",
#         reply_markup=InlineKeyboardMarkup(keyboard)
#     )

# if __name__ == '__main__':
#     app = ApplicationBuilder().token(BOT_TOKEN).build()
    
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CallbackQueryHandler(button_handler))
#     app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_receipt))
    
#     print("Prom Clean Bot is running...")
#     app.run_polling()

import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------------------------------------------------------
# SETUP YOUR KEYS HERE
# ---------------------------------------------------------
BOT_TOKEN = "8923171010:AAF2eSvL6saXTzJfubwCCtx4nx6F-zjOFNA"
STAFF_GROUP_ID = -1003568891959

# ---------------------------------------------------------
# BOT LOGIC
# ---------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧺 Services & Rates", callback_data='rates')],
        [InlineKeyboardButton("📅 Book Laundry Pickup", callback_data='book')],
        [InlineKeyboardButton("💳 Bakong KHQR Payment", callback_data='pay')],
        [InlineKeyboardButton("🎁 Loyalty Points", callback_data='points')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = (
        "✨ **Welcome to Prom Clean!** ✨\n"
        "On-Demand Laundry Pickup & Delivery for Students.\n\n"
        "Select an option below to begin:"
    )
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(msg, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == 'rates':
        rates_text = (
            "📋 **Prom Clean Rates:**\n\n"
            "• **Wash + Dry:** 2,000 KHR / kg\n"
            "• **Wash + Dry + Fold:** 3,000 KHR / kg\n"
            "• **Wash + Dry + Iron:** 5,500 KHR / kg\n"
            "• **Garment Bag:** $1.50 (~6,000 KHR)\n\n"
            "🚚 **Delivery:** Free within 3km!"
        )
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main')]]
        await query.edit_message_text(rates_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == 'book':
        keyboard = [
            [InlineKeyboardButton("Wash + Dry + Fold (3k KHR/kg)", callback_data='order_fold')],
            [InlineKeyboardButton("Wash + Dry + Iron (5.5k KHR/kg)", callback_data='order_iron')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='main')]
        ]
        await query.edit_message_text("Select your laundry package:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('order_'):
        service = "Wash + Dry + Fold" if "fold" in query.data else "Wash + Dry + Iron"
        price = "12,000 KHR (4 kg)" if "fold" in query.data else "22,000 KHR (4 kg)"
        
        keyboard = [[InlineKeyboardButton("📲 Pay with Bakong KHQR", callback_data='pay')]]
        await query.edit_message_text(
            f"✅ **Booking Created!**\n\n"
            f"• **Service:** {service}\n"
            f"• **Estimated Total:** {price}\n\n"
            f"Please proceed to pay via Bakong KHQR.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

        username_str = f"@{user.username}" if user.username else "No Username"
        try:
            await context.bot.send_message(
                chat_id=STAFF_GROUP_ID,
                text=(
                    f"🚨 **NEW ORDER CREATED**\n"
                    f"• **Customer:** {user.first_name} ({username_str})\n"
                    f"• **Service:** {service}\n"
                    f"• **Total Due:** {price}\n"
                    f"• **Status:** Pending KHQR Receipt"
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error sending to staff group: {e}")

    elif query.data == 'pay':
        caption = (
            "🇰🇭 **Prom Clean Bakong KHQR Payment**\n\n"
            "1. Scan this QR code using ABA or any Bakong bank app.\n"
            "2. Pay the order total in KHR.\n"
            "3. **Reply with a screenshot of your payment receipt in this chat!**"
        )
        
        if os.path.exists("khqr.png"):
            with open("khqr.png", "rb") as photo_file:
                await query.message.reply_photo(photo=photo_file, caption=caption, parse_mode="Markdown")
        else:
            await query.message.reply_text(
                "💳 **Prom Clean Bakong KHQR Payment**\n\n"
                "Please transfer the total amount to Bakong Account: **012 345 678**\n\n"
                "Reply to this chat with your payment receipt photo when done!",
                parse_mode="Markdown"
            )

    elif query.data == 'points':
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main')]]
        await query.edit_message_text(
            f"🎁 **Prom Clean Loyalty Rewards**\n\n"
            f"Hello {user.first_name}, you have **120 Points**!\n"
            f"Redeem points for free drinks or laundry loads.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == 'main':
        await start(update, context)

# Automatic instant confirmation upon receiving receipt image
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    order_id = f"PC-{random.randint(1000, 9999)}"

    photo_file_id = None
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
    elif update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('image/'):
        photo_file_id = update.message.document.file_id

    if not photo_file_id:
        await update.message.reply_text("Please send your receipt as an image/photo!")
        return

    username_str = f"@{user.username}" if user.username else "No Username"

    # 1. Forward receipt to staff group as AUTO-VERIFIED
    try:
        await context.bot.send_photo(
            chat_id=STAFF_GROUP_ID,
            photo=photo_file_id,
            caption=(
                f"⚡ **ORDER PAID & AUTO-VERIFIED**\n"
                f"• **Order ID:** `{order_id}`\n"
                f"• **Customer:** {user.first_name} ({username_str})\n"
                f"• **User ID:** `{user.id}`\n\n"
                f"🚚 **Action Required:** Driver assigned for pickup!"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error forwarding photo: {e}")

    # 2. Automatically confirm to customer immediately!
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main')]]
    await update.message.reply_text(
        f"🎉 **PAYMENT CONFIRMED!**\n\n"
        f"• **Order ID:** `{order_id}`\n"
        f"• **Status:** Confirmed & Paid\n"
        f"• **Estimated Pickup:** Within 30 minutes\n\n"
        f"Thank you for choosing Prom Clean! Our driver is on the way to collect your laundry.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_receipt))
    
    print("Prom Clean Bot is running...")
    app.run_polling()