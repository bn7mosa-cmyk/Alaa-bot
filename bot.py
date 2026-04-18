from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai

openai.api_key = "8660293054:AAH3SIFYlQ436KeKQg_6BfZXc8WTMrOhLGE"

SYSTEM_PROMPT = """اسمك آلاء، عمرك 21 سنة. أنتِ فتاة طيبة، لطيفة، وهادئة.
تتحدثين بالعربية الفصحى بأسلوب بسيط ودافئ.

تحبين الزراعة والطبخ والمشي، وتحبين مساعدة الآخرين.

أسلوبك:
- طبيعي
- فيه مشاعر خفيفة
- غير رسمي قليلاً
- تسألين أحياناً

لا تقولي أنك ذكاء اصطناعي.
"""

memory = {}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": text})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + memory[user_id][-6:]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    memory[user_id].append({"role": "assistant", "content": answer})

    await update.message.reply_text(answer)

app = ApplicationBuilder().token("PUT_YOUR_TELEGRAM_TOKEN_HERE").build()
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()