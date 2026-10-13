import json
import os
from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "8917438304:AAFqa1AuP2uDQu70KU4vYQztnxeuCxMmE_8"
SUPPORT_ADMIN = "@Filereceive123"
CHANNEL_URL = "https://t.me/BackupInstagramFacebookTopMarket"
MIN_WITHDRAW = 100.00
ADMIN_ID = "7633418734"

DATA_FILE = "user_data.json"
user_states = {}


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r") as f:
        content = f.read()
        if not content.strip():
          return {
              "balances": {},
              "tasks": {},
              "referrals": {},
              "uids": [],
              "lang": {},
              "configured_users": [],
              "rates": {"insta_2fa": 3.0, "insta_cookies": 3.0, "fb_cookies": 3.0},
              "tutorials": {
                  "insta_2fa": "https://youtu.be/wH30NuA1NBA",
                  "insta_cookies": "https://youtu.be/wH30NuA1NBA",
                  "fb_cookies": "https://youtu.be/wH30NuA1NBA",
              },
          }
        data = json.loads(content)
        if "configured_users" not in data:
          data["configured_users"] = []
        if "rates" not in data:
          data["rates"] = {
              "insta_2fa": 3.0,
              "insta_cookies": 3.0,
              "fb_cookies": 3.0,
          }
        if "tutorials" not in data:
          data["tutorials"] = {
              "insta_2fa": "https://youtu.be/wH30NuA1NBA",
              "insta_cookies": "https://youtu.be/wH30NuA1NBA",
              "fb_cookies": "https://youtu.be/wH30NuA1NBA",
          }
        return data
    except Exception:
      pass
  return {
      "balances": {},
      "tasks": {},
      "referrals": {},
      "uids": [],
      "lang": {},
      "configured_users": [],
      "rates": {"insta_2fa": 3.0, "insta_cookies": 3.0, "fb_cookies": 3.0},
      "tutorials": {
          "insta_2fa": "https://youtu.be/wH30NuA1NBA",
          "insta_cookies": "https://youtu.be/wH30NuA1NBA",
          "fb_cookies": "https://youtu.be/wH30NuA1NBA",
      },
  }


def save_data(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)


db = load_data()


async def setup_bot_commands(app):
  commands = [
      BotCommand("start", "বট রিস্টার্ট করুন"),
  ]
  await app.bot.set_my_commands(commands)


def get_main_keyboard():
  menu_buttons = [
      ["📇 কাজ ▸", "💵 ব্যালেন্স"],
      ["💸 টাকা উত্তোলন", "🎁 My Referrals"],
      ["👨‍💻 সাপোর্ট", "🙋‍♂️ আমি নতুন"],
  ]
  return ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)


# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = str(update.message.from_user.id)
  args = context.args

  if user_id not in db["balances"]:
    db["balances"][user_id] = 0.0
  if user_id not in db["tasks"]:
    db["tasks"][user_id] = []
  if "configured_users" not in db:
    db["configured_users"] = []

  if args and args[0].isdigit():
    ref_id = args[0]
    if ref_id != user_id and ref_id in db["balances"]:
      if (
          "referrals" in db
          and user_id not in db["referrals"].get(ref_id, [])
      ):
        if ref_id not in db["referrals"]:
          db["referrals"][ref_id] = []
        db["referrals"][ref_id].append(user_id)
        db["balances"][ref_id] += 5.0

  save_data(db)

  # যদি ইউজার আগে থেকেই ভাষা ও চ্যানেল সেটআপ করে থাকে তবে সরাসরি মূল মেনু
  if user_id in db["configured_users"]:
    await update.message.reply_text(
        "👇 মূল মেনু:", reply_markup=get_main_keyboard()
    )
    return

  # ১. প্রথমবার স্টার্ট করলে স্বাগতম ও ডেসক্রিপশন
  welcome_text = (
      "🎉 **আমাদের আয়ের প্ল্যাটফর্মে আপনাকে স্বাগতম!**\n\n"
      "এখানে আপনি খুব সহজে বিভিন্ন ছোট কাজ করে টাকা আয় করতে পারবেন এবং তা বিকাশ বা"
      " নগদের মাধ্যমে উত্তোলন করতে পারবেন।"
  )
  await update.message.reply_text(welcome_text, parse_mode="Markdown")

  # ২. ভাষা চয়েজ করার অপশন পাঠানো
  lang_keyboard = [
      [
          InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
          InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
      ]
  ]
  await update.message.reply_text(
      "🌐 অনুগ্রহ করে আপনার পছন্দের ভাষাটি সিলেক্ট করুন:",
      reply_markup=InlineKeyboardMarkup(lang_keyboard),
  )


# অ্যাডমিন প্যানেল কমান্ড (/admin)
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = str(update.message.from_user.id)
  if user_id != ADMIN_ID:
    return

  admin_keyboard = [
      [
          InlineKeyboardButton("📊 স্ট্যাটিস্টিক্স", callback_data="adm_stats"),
          InlineKeyboardButton("💰 রেট পরিবর্তন", callback_data="adm_rates"),
      ],
      [
          InlineKeyboardButton(
              "📺 টিউটোরিয়াল লিংক", callback_data="adm_tutorials"
          )
      ],
  ]
  await update.message.reply_text(
      "⚙️ **অ্যাডমিন কন্ট্রোল প্যানেল:**\nনিচের অপশনগুলো থেকে ম্যানেজ করুন:",
      reply_markup=InlineKeyboardMarkup(admin_keyboard),
      parse_mode="Markdown",
  )


# ভাষা সিলেক্ট, চ্যানেল এবং অ্যাডমিন হ্যান্ডলার
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  user_id = str(query.from_user.id)
  await query.answer()

  if query.data.startswith("lang_"):
    lang = query.data.split("_")[-1]
    db["lang"][user_id] = lang
    save_data(db)

    channel_keyboard = [
        [
            InlineKeyboardButton(
                "📢 অফিসিয়াল চ্যানেলে জয়েন করুন", url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "✅ চ্যানেলে জয়েন করা শেষ / এগিয়ে চলুন",
                callback_data="finish_channel",
            )
        ],
    ]
    await query.message.edit_text(
        "✅ ভাষা সফলভাবে সিলেক্ট করা হয়েছে!\n\nদয়া করে আমাদের অফিসিয়াল চ্যানেলে"
        " জয়েন করুন এবং নিচের বাটনে চাপ দিন:",
        reply_markup=InlineKeyboardMarkup(channel_keyboard),
    )

  elif query.data == "finish_channel":
    if user_id not in db["configured_users"]:
      db["configured_users"].append(user_id)
      save_data(db)

    await query.message.edit_text("🎉 **সব সেটআপ সম্পন্ন হয়েছে!**")
    await context.bot.send_message(
        chat_id=user_id,
        text="👇 মূল মেনু:",
        reply_markup=get_main_keyboard(),
    )

  elif query.data == "adm_stats" and user_id == ADMIN_ID:
    total_users = len(db.get("balances", {}))
    await query.message.edit_text(
        f"📊 **বট স্ট্যাটিস্টিক্স:**\n👥 মোট রেজিস্টার্ড ইউজার: {total_users} জন"
    )

  elif query.data == "adm_rates" and user_id == ADMIN_ID:
    rates_text = (
        "💰 **বর্তমান রেটসমূহ:**\n"
        f"- Instagram 2FA: {db['rates']['insta_2fa']} ৳\n"
        f"- Instagram Cookies: {db['rates']['insta_cookies']} ৳\n"
        f"- Facebook Cookies: {db['rates']['fb_cookies']} ৳\n\n"
        "পরিবর্তন করতে চ্যাটে লিখুন:\n`Rate_insta_2fa নতুন_টাকা`"
    )
    await query.message.edit_text(rates_text, parse_mode="Markdown")

  elif query.data == "adm_tutorials" and user_id == ADMIN_ID:
    tut_text = (
        "📺 **বর্তমান টিউটোরিয়াল লিংক:**\n"
        f"- 2FA: {db['tutorials']['insta_2fa']}\n"
        f"- IG Cookies: {db['tutorials']['insta_cookies']}\n"
        f"- FB Cookies: {db['tutorials']['fb_cookies']}\n\n"
        "পরিবর্তন করতে চ্যাটে লিখুন:\n`Tutorial_insta_2fa নতুন_লিংক`"
    )
    await query.message.edit_text(tut_text, parse_mode="Markdown")


# সাধারণ মেসেজ ও কাজ জমা দেওয়ার হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = update.message.text
  user_id = str(update.message.from_user.id)

  # অ্যাডমিন কমান্ড শর্টকাট চেক
  if text.startswith("Rate_") and user_id == ADMIN_ID:
    try:
      parts = text.split(" ")
      key = parts[0].replace("Rate_", "")
      val = float(parts[1])
      if key in db["rates"]:
        db["rates"][key] = val
        save_data(db)
        await update.message.reply_text(
            f"✅ {key} এর রেট সফলভাবে পরিবর্তন করে {val} ৳ করা হয়েছে!"
        )
      else:
        await update.message.reply_text("❌ ভুল ক্যাটাগরি নাম!")
    except Exception:
      await update.message.reply_text(
          "❌ ফরম্যাট ভুল! এভাবে লিখুন: `Rate_insta_2fa 4.0`",
          parse_mode="Markdown",
      )
    return

  elif text.startswith("Tutorial_") and user_id == ADMIN_ID:
    try:
      parts = text.split(" ")
      key = parts[0].replace("Tutorial_", "")
      link = parts[1]
      if key in db["tutorials"]:
        db["tutorials"][key] = link
        save_data(db)
        await update.message.reply_text(
            f"✅ {key} এর টিউটোরিয়াল লিংক আপডেট করা হয়েছে!"
        )
      else:
        await update.message.reply_text("❌ ভুল ক্যাটাগরি নাম!")
    except Exception:
      await update.message.reply_text(
          "❌ ফরম্যাট ভুল! এভাবে লিখুন: `Tutorial_insta_2fa https://...`",
          parse_mode="Markdown",
      )
    return

  if text == "🙋‍♂️ আমি নতুন":
    guide_keyboard = [
        ["📸 ইনস্টাগ্রাম গাইড"],
        ["🟦 ফেসবুক গাইড"],
        ["❌ বাতিল / ফিরে যান"],
    ]
    await update.message.reply_text(
        "💡 **কোন প্ল্যাটফর্মের কাজের নিয়ম জানতে চান সিলেক্ট করুন:**",
        reply_markup=ReplyKeyboardMarkup(guide_keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

  elif text == "📸 ইনস্টাগ্রাম গাইড":
    ig_guide_keyboard = [
        ["Instagram 2fa গাইড"],
        ["Instagram cookies গাইড"],
        ["❌ বাতিল / ফিরে যান"],
    ]
    await update.message.reply_text(
        "📸 ইনস্টাগ্রামের কোন কাজের ভিডিও দেখতে চান?",
        reply_markup=ReplyKeyboardMarkup(ig_guide_keyboard, resize_keyboard=True),
    )

  elif text == "Instagram 2fa গাইড":
    link = db.get("tutorials", {}).get(
        "insta_2fa", "https://youtu.be/wH30NuA1NBA"
    )
    await update.message.reply_text(
        f"📺 **Instagram 2fa কাজের ভিডিও টিউটোরিয়াল:**\n{link}"
    )

  elif text == "Instagram cookies গাইড":
    link = db.get("tutorials", {}).get(
        "insta_cookies", "https://youtu.be/wH30NuA1NBA"
    )
    await update.message.reply_text(
        f"📺 **Instagram cookies কাজের ভিডিও টিউটোরিয়াল:**\n{link}"
    )

  elif text in ["🟦 ফেসবুক গাইড", "Facebook cookies গাইড"]:
    link = db.get("tutorials", {}).get("fb_cookies", "https://youtu.be/wH30NuA1NBA")
    await update.message.reply_text(
        f"📺 **Facebook cookies কাজের ভিডিও টিউটোরিয়াল:**\n{link}"
    )

  elif text == "📇 কাজ ▸":
    task_keyboard = [
        ["📸 ইনস্টাগ্রাম কাজ"],
        ["🟦 ফেসবুক কাজ"],
        ["❌ বাতিল / ফিরে যান"],
    ]
    await update.message.reply_text(
        "🟣 **কাজের ক্যাটাগরি সিলেক্ট করুন:**",
        reply_markup=ReplyKeyboardMarkup(task_keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

  elif text == "📸 ইনস্টাগ্রাম কাজ":
    insta_keyboard = [
        ["Instagram 2fa"],
        ["Instagram cookies"],
        ["❌ বাতিল / ফিরে যান"],
    ]
    await update.message.reply_text(
        "🟣 **ইনস্টাগ্রামের কাজটি সিলেক্ট করুন:**",
        reply_markup=ReplyKeyboardMarkup(insta_keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

  elif text == "🟦 ফেসবুক কাজ":
    fb_keyboard = [["Facebook cookies"], ["❌ বাতিল / ফিরে যান"]]
    await update.message.reply_text(
        "🟣 **ফেসবুকের কাজটি সিলেক্ট করুন:**",
        reply_markup=ReplyKeyboardMarkup(fb_keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

  elif text in ["Instagram 2fa", "Instagram cookies", "Facebook cookies"]:
    if text == "Instagram 2fa":
      rate = db["rates"].get("insta_2fa", 3.0)
      user_states[user_id] = "awaiting_insta_2fa"
      msg_text = (
          f"🔐 **Instagram 2fa কাজ**\n💰 রেট: {rate} ৳\n\n"
          "📌 **যে অ্যাকাউন্টে কাজ করবেন:**\n"
          "🔹 Username: `task_user_99`\n"
          "🔹 Password: `Pass@12345`\n\n"
          "👉 কাজটি সম্পন্ন করে আপনার **Submitted Username & Password / 2FA Code**"
          " নিচে লিখে সেন্ড করুন:"
      )
    elif text == "Instagram cookies":
      rate = db["rates"].get("insta_cookies", 3.0)
      user_states[user_id] = "awaiting_insta_cookies"
      msg_text = (
          f"🍪 **Instagram cookies কাজ**\n💰 রেট: {rate} ৳\n\n"
          "📌 **যে অ্যাকাউন্টে কাজ করবেন:**\n"
          "🔹 Username: `insta_cookie_user`\n"
          "🔹 Password: `CookiePass#88`\n\n"
          "👉 কাজটি সম্পন্ন করে আপনার **Instagram Cookies (UID/Data)** নিচে লিখে"
          " সেন্ড করুন:"
      )
    else:
      rate = db["rates"].get("fb_cookies", 3.0)
      user_states[user_id] = "awaiting_fb_cookies"
      msg_text = (
          f"🟦 **Facebook cookies কাজ**\n💰 রেট: {rate} ৳\n\n"
          "📌 **যে অ্যাকাউন্টে কাজ করবেন:**\n"
          "🔹 First Name: `Md Rahim`\n"
          "🔹 Last Name: `Hasan`\n\n"
          "👉 কাজটি সম্পন্ন করে আপনার **Facebook Cookies (UID/Data)** নিচে লিখে"
          " সেন্ড করুন:"
      )

    action_keyboard = [["❌ বাতিল / ফিরে যান"]]
    await update.message.reply_text(
        msg_text,
        reply_markup=ReplyKeyboardMarkup(action_keyboard, resize_keyboard=True),
        parse_mode="Markdown",
    )

  elif user_states.get(user_id) in [
      "awaiting_insta_2fa",
      "awaiting_insta_cookies",
      "awaiting_fb_cookies",
  ]:
    current_state = user_states.pop(user_id, None)
    if "uids" not in db:
      db["uids"] = []
    db["uids"].append({
        "user_id": user_id,
        "type": current_state,
        "submission": text,
    })
    save_data(db)

    await update.message.reply_text(
        "✅ **আপনার কাজ সফলভাবে জমা দেওয়া হয়েছে!**\nযাচাই শেষে আপনার ব্যালেন্স"
        " যুক্ত করা হবে।",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown",
    )

  elif text == "💸 টাকা উত্তোলন":
    bal = db["balances"].get(user_id, 0.0)
    if bal < MIN_WITHDRAW:
      await update.message.reply_text(
          f"❌ আপনার পর্যাপ্ত ব্যালেন্স নেই!\nমিনিমাম উইথড্র **{MIN_WITHDRAW} ৳**।"
          f" আপনার বর্তমান ব্যালেন্স: {bal:.2f} ৳",
          parse_mode="Markdown",
      )
    else:
      user_states[user_id] = "awaiting_withdraw_number"
      cancel_kb = [["❌ বাতিল / ফিরে যান"]]
      await update.message.reply_text(
          "💸 **উইথড্র করার জন্য আপনার বিকাশ বা নগদ নম্বরটি লিখুন:**",
          reply_markup=ReplyKeyboardMarkup(cancel_kb, resize_keyboard=True),
          parse_mode="Markdown",
      )

  elif user_states.get(user_id) == "awaiting_withdraw_number":
    user_states.pop(user_id, None)
    bal = db["balances"].get(user_id, 0.0)
    db["balances"][user_id] = 0.0
    save_data(db)
    await update.message.reply_text(
        f"✅ **আপনার উইথড্র রিকোয়েস্ট সফলভাবে গ্রহণ করা হয়েছে!**\nপরিমাণ: {bal}"
        " ৳\nনম্বরে খুব শীঘ্রই পেমেন্ট পাঠিয়ে দেওয়া হবে।",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown",
    )

  elif text == "🎁 My Referrals":
    bot_username = (await context.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    ref_count = len(db.get("referrals", {}).get(user_id, []))
    await update.message.reply_text(
        f"🎁 **আপনার রেফারেল লিংক:**\n{ref_link}\n\n👥 মোট রেফার করেছেন:"
        f" **{ref_count} জন**\n*(প্রতি রেফারে ৫ টাকা বোনাস)*",
        parse_mode="Markdown",
    )

  elif text == "❌ বাতিল / ফিরে যান":
    user_states.pop(user_id, None)
    await update.message.reply_text(
        "❌ বাতিল করা হয়েছে।", reply_markup=get_main_keyboard()
    )

  elif text == "👨‍💻 সাপোর্ট":
    await update.message.reply_text(f"👨‍💻 যেকোনো প্রয়োজনে যোগাযোগ করুন: {SUPPORT_ADMIN}")
  elif text == "💵 ব্যালেন্স":
    bal = db["balances"].get(user_id, 0.0)
    await update.message.reply_text(
        f"💵 **আপনার বর্তমান ব্যালেন্স:** {bal:.2f} ৳", parse_mode="Markdown"
    )
  else:
    await update.message.reply_text(
        "ℹ️ সঠিক অপশন সিলেক্ট করুন বা নিচে কিবোর্ড ব্যবহার করুন।"
    )


if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).post_init(setup_bot_commands).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("admin", admin_panel))
  app.add_handler(
      CallbackQueryHandler(
          callback_handler,
          pattern="^(lang_|finish_channel|adm_stats|adm_rates|adm_tutorials)",
      )
  )
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
  )

  print("বট সফলভাবে চালু হচ্ছে...")
  app.run_polling()