import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# রেন্ডারের পোর্ট সমস্যা সমাধানের জন্য সার্ভার (এটি ব্যাকগ্রাউন্ডে চলবে)
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# আপনার আসল প্রজেক্ট বা বটের কোড এখানে থাকবে
print("বট সফলভাবে চালু হচ্ছে...")

# আপনার যদি নিজস্ব কোড থাকে, সেটি এর নিচে বসাতে পারেন।
import json
import os
import threading
import time
import requests
import telebot
from telebot import types

# আপনার দেওয়া টোকেন এবং এডমিন আইডি এখানে বসানো আছে
TOKEN = "8802240153:AAEnnbsfOCykXufnCwwq39CcyPBxjZC8FcY"
ADMIN_ID = 7633418734
URL = "http://skysysx.net/e/boss"

bot = telebot.TeleBot(TOKEN)
USERS_FILE = "users.json"
CONFIG_FILE = "config.json"


# ইউজার লোড ও সেভ করার ফাংশন
def load_users():
  if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
      try:
        return set(json.load(f))
      except:
        return set()
  return set()


def save_users(users_set):
  with open(USERS_FILE, "w") as f:
    json.dump(list(users_set), f)


users = load_users()

# ডিফল্ট মেসেজ সেটআপ (প্রিমিয়াম ইমোজি সহ)
default_config = {
    "msg_on": (
        "🚀 **Link On!** 🚀\n\n✅ আপনারা সবাই আনলিমিটেড একাউন্ট সাবমিট করুন"
        " ✅🤝\n\n📢 অবশ্যই আমাদের অফিসিয়াল টেলিগ্রাম চ্যানেলে জয়েন"
        " করবেন।\n\n🔗 **টেলিগ্রাম চ্যানেল লিংক 👇**\nhttps://t.me/+ArhD5R5-d6k3ZjVl"
    ),
    "msg_off": (
        "📴 **Link Off!** 📴\n\n⏳ আপনারা সবাই অপেক্ষা করুন, লিংক আবার অন"
        " হবে। 🔄\n\n📢 অবশ্যই আমাদের অফিসিয়াল টেলিগ্রাম চ্যানেলে জয়েন"
        " করবেন।\n\n🔗 **টেলিগ্রাম চ্যানেল লিংক 👇**\nhttps://t.me/+ArhD5R5-d6k3ZjVl"
    ),
}


def load_config():
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except:
        return default_config
  return default_config


def save_config(config):
  with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=4)


config = load_config()


# নিচের কিবোর্ডে "বিস্তারিত জানুন ℹ️" বাটন তৈরি করার ফাংশন
def get_main_keyboard():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  details_btn = types.KeyboardButton("বিস্তারিত জানুন ℹ️")
  markup.add(details_btn)
  return markup


# বটের বাম পাশের থ্রি-ডট মেনুতে কমান্ড সেট করার ফাংশন
def set_bot_commands():
  try:
    bot.set_my_commands(
        [types.BotCommand("start", "বট স্টার্ট বা রিফ্রেশ করুন 🚀")]
    )
  except Exception as e:
    print("Command set error:", e)


# /start কমান্ড দিলে প্রিমিয়াম ওয়েলকাম মেসেজ শো করবে
@bot.message_handler(commands=["start"])
def send_welcome(message):
  chat_id = message.chat.id
  if chat_id not in users:
    users.add(chat_id)
    save_users(users)

  welcome_text = (
      "🌟 **স্বাগতম!** 🌟\n\n🎯 আমাদের কুকিজ সাবমিট লিংক অন হওয়া মাত্রই"
      " আপনাকে আমাদের অফিসিয়াল বট নোটিফিকেশন দিয়ে দিবে। ⚡️\n\n📢 অনুগ্রহ"
      " করে বট ফলো করুন এবং গুরুত্বপূর্ণ আপডেট পেতে আমাদের অফিসিয়াল চ্যানেল"
      " ফলো করুন। 👇\n\n🔗 **আমাদের অফিসিয়াল চ্যানেল লিংক:**\nhttps://t.me/+ArhD5R5-d6k3ZjVl"
  )

  bot.reply_to(
      message,
      welcome_text,
      parse_mode="Markdown",
      reply_markup=get_main_keyboard(),
  )


# ব্যবহারকারী যখন "বিস্তারিত জানুন ℹ️" বাটনে ক্লিক করবে
@bot.message_handler(
    func=lambda message: message.text == "বিস্তারিত জানুন ℹ️"
)
def show_details(message):
  details_text = (
      "💎 **কুকিজ কাজের বিস্তারিত তথ্য** 💎\n\n🔍 ইন্সটাগ্রাম কুকিজ কাজ"
      " সম্পর্কে ডিটেইলসে সব তথ্য জানতে আমাদের অফিসিয়াল চ্যানেলে জয়েন"
      " করুন এবং আমাদেরকে ইনবক্স করুন। 📩\n\n📌 **অফিসিয়াল চ্যানেল লিংক"
      " 👇**\nhttps://t.me/+ArhD5R5-d6k3ZjVl"
  )
  bot.reply_to(
      message,
      details_text,
      parse_mode="Markdown",
      reply_markup=get_main_keyboard(),
  )


# --- এডমিন প্যানেল (পাসওয়ার্ড: munnanaim) ---


@bot.message_handler(commands=["admin"])
def admin_panel(message):
  if message.from_user.id != ADMIN_ID:
    bot.reply_to(message, "দুঃখিত, আপনি এই কমান্ডটি ব্যবহার করার অনুমতি নেই।")
    return

  parts = message.text.split(maxsplit=1)
  if len(parts) < 2 or parts[1] != "munnanaim":
    bot.reply_to(
        message,
        "⚠️ ভুল পাসওয়ার্ড!\nসঠিক নিয়মে লিখুন: `/admin munnanaim`",
        parse_mode="Markdown",
    )
    return

  total_users = len(users)
  panel_text = (
      f"🛠 **বট এডমিন প্যানেল** 🛠\n\n👥 মোট ইউজার সংখ্যা: `{total_users}` জন\n\n"
      f"📌 **বর্তমান ON মেসেজ:**\n{config['msg_on']}\n\n📌 **বর্তমান OFF"
      f" মেসেজ:**\n{config['msg_off']}\n\n--- \n**মেসেজ পরিবর্তন করার"
      " নিয়ম:**\n• ON মেসেজ বদলাতে লিখুন: `/seton আপনার নতুন লেখা`\n• OFF মেসেজ"
      " বদলাতে লিখুন: `/setoff আপনার নতুন লেখা`"
  )
  bot.reply_to(message, panel_text, parse_mode="Markdown")


# ON মেসেজ এডিট করার কমান্ড
@bot.message_handler(commands=["seton"])
def set_on_message(message):
  if message.from_user.id != ADMIN_ID:
    return

  new_msg = message.text.replace("/seton", "").strip()
  if not new_msg:
    bot.reply_to(
        message,
        "দয়া করে মেসেজ লিখে দিন। যেমন: `/seton আপনার নতুন মেসেজ`",
        parse_mode="Markdown",
    )
    return

  config["msg_on"] = new_msg
  save_config(config)
  bot.reply_to(message, "✅ সফলভাবে লিংক ON হওয়ার মেসেজটি আপডেট করা হয়েছে!")


# OFF মেসেজ এডিট করার কমান্ড
@bot.message_handler(commands=["setoff"])
def set_off_message(message):
  if message.from_user.id != ADMIN_ID:
    return

  new_msg = message.text.replace("/setoff", "").strip()
  if not new_msg:
    bot.reply_to(
        message,
        "দয়া করে মেসেজ লিখে দিন। যেমন: `/setoff আপনার নতুন মেসেজ`",
        parse_mode="Markdown",
    )
    return

  config["msg_off"] = new_msg
  save_config(config)
  bot.reply_to(message, "✅ সফলভাবে লিংক OFF হওয়ার মেসেজটি আপডেট করা হয়েছে!")


# সবার কাছে ব্রডকাস্ট মেসেজ পাঠানো
def broadcast_message(message_text):
  for chat_id in users:
    try:
      bot.send_message(
          chat_id,
          message_text,
          parse_mode="Markdown",
          reply_markup=get_main_keyboard(),
      )
    except Exception as e:
      print(f"Failed to send to {chat_id}: {e}")


# ওয়েবসাইট মনিটর করার ব্যাকগ্রাউন্ড লুপ
def monitor_website():
  last_status = None
  print("Website monitoring started...")

  while True:
    try:
      response = requests.get(URL, timeout=10)
      html_content = response.text

      if "বায়ার এপিআই অফলাইন" in html_content:
        current_status = "OFF"
      else:
        current_status = "ON"

      if last_status is not None and current_status != last_status:
        current_config = load_config()
        if current_status == "ON":
          broadcast_message(current_config["msg_on"])
          print("[ALERT] Link turned ON. Broadcasted to all users.")
        elif current_status == "OFF":
          broadcast_message(current_config["msg_off"])
          print("[ALERT] Link turned OFF. Broadcasted to all users.")

      last_status = current_status

    except Exception as e:
      print("Connection error:", e)

    time.sleep(30)


if __name__ == "__main__":
  set_bot_commands()  # বাম পাশের মেনু সেটআপ রান করা
  t = threading.Thread(target=monitor_website)
  t.daemon = True
  t.start()

  print("Bot is running successfully with all features!")
  bot.polling()
