from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# 🔑 ВСТАВ СВІЙ ТОКЕН ТУТ
TOKEN = "YOUR TOKEN"
NASA_API_KEY = "YOUR TOKEN"
# 🔑 N2YO.COM API КЛЮЧ ТУТ
N2YO_API_KEY = "YOUR TOKEN" 


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Я CosmoBot — твій космічний помічник!\n\n"
        "📡 Команди:\n"
        "/news – космічні новини\n"
        "/apod – фото дня від NASA\n"
        "/mars – фото з Марса\n"
        "/asteroids – небезпечні об'єкти\n"
        "/epic – зображення Землі\n"
        "/exoplanet – дані про екзопланети\n"
        "/imagelibrary – пошук фото NASA\n"
        "/ssc – Satellite Situation Center\n"
        "/iss - Проліт МКС над Києвом\n"
        "/trek – карти Moon/Mars/Vesta\n"
        "/quiz – космічна вікторина\n"
        "/help – інструкція"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Як користуватись:\n"
        "/news — космічні новини\n"
        "/apod — Astronomy Picture of the Day\n"
        "/mars — фото з ровера Curiosity\n"
        "/asteroids — наближені обʼєкти до Землі\n"
        "/epic — зображення Землі (EPIC)\n"
        "/exoplanet — посилання на екзопланети\n"
        "/imagelibrary — пошук NASA фото\n"
        "/ssc — Satellite Situation Center\n"
        "/iss - Проліт МКС над Києвом\n"
        "/trek — Moon, Mars, Vesta карти"
        "/quiz – космічна вікторина\n"
    )

# /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.spaceflightnewsapi.net/v4/articles?limit=2"
    response = requests.get(url)
    if response.status_code == 200:
        for article in response.json()["results"]:
            title = article["title"]
            summary = article["summary"][:300] + "..."
            link = article["url"]
            await update.message.reply_text(
                f"🚀 <b>{title}</b>\n\n{summary}\n🔗 <a href='{link}'>Читати далі</a>",
                parse_mode="HTML"
            )
    else:
        await update.message.reply_text("❌ Не вдалося отримати новини.")

# /apod
async def apod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        d = r.json()
        await update.message.reply_photo(
            photo=d["url"],
            caption=f"🪐 <b>{d['title']}</b>\n\n{d['explanation'][:300]}...",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text("❌ APOD не працює.")

# /mars
async def mars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={NASA_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        photos = r.json().get("latest_photos", [])
        if photos:
            p = photos[0]
            await update.message.reply_photo(photo=p["img_src"], caption=f"📸 Curiosity, {p['earth_date']}")
        else:
            await update.message.reply_text("😔 Фото з Марса не знайдено.")
    else:
        await update.message.reply_text("❌ Помилка при запиті до Mars API.")

# /asteroids
async def asteroids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={NASA_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        msg = "☄️ Найближчі астероїди:\n"
        count = 0
        for date, objs in data["near_earth_objects"].items():
            for obj in objs[:2]:
                name = obj["name"]
                size = obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
                dist = obj["close_approach_data"][0]["miss_distance"]["kilometers"]
                msg += f"\n🔸 {name}\n   ~{round(size)} м\n   Відстань: {round(float(dist))} км\n"
                count += 1
                if count >= 4:
                    break
            if count >= 4:
                break
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ Не вдалося отримати астероїди.")

# /epic
async def epic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if data:
            img = data[0]
            date = img["date"].split()[0].replace("-", "/")
            url_img = f"https://epic.gsfc.nasa.gov/archive/natural/{date}/jpg/{img['image']}.jpg"
            await update.message.reply_photo(photo=url_img, caption=f"🌍 EPIC, {img['date']}")
        else:
            await update.message.reply_text("😔 Зображень немає.")
    else:
        await update.message.reply_text("❌ EPIC не працює.")

# /exoplanet
async def exoplanet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔭 Дані про екзопланети:\nhttps://exoplanetarchive.ipac.caltech.edu/"
    )

# /imagelibrary
async def image_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = "mars"
    url = f"https://images-api.nasa.gov/search?q={q}"
    r = requests.get(url)
    if r.status_code == 200:
        items = r.json()["collection"]["items"]
        if items:
            item = items[0]
            img_url = item["links"][0]["href"]
            title = item["data"][0]["title"]
            await update.message.reply_photo(photo=img_url, caption=f"🖼️ {title}")
        else:
            await update.message.reply_text("📸 Нічого не знайдено.")
    else:
        await update.message.reply_text("❌ Image API не працює.")

# /ssc
async def ssc(update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text( "🛰️ Satellite Situation Center:\nhttps://sscweb.gsfc.nasa.gov/"
)
# /iss - Проліт МКС над Києвом
from datetime import datetime

async def iss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    NORAD_ID = 25544           # ISS
    latitude = 50.45
    longitude = 30.52
    altitude = 150             # м
    days_forward = 2 #днів вперед

    # ► Виберіть ОДИН з двох варіантів -------------------------------
    use_visual = False         # True = видимі прольоти, False = радіопрольоти
    # ----------------------------------------------------------------

    if use_visual:
        min_visibility = 1     # сек
        endpoint = (
            f"visualpasses/{NORAD_ID}/{latitude}/{longitude}/{altitude}/"
            f"{days_forward}/{min_visibility}"
        )
    else:
        min_elevation = 10     # °
        endpoint = (
            f"radiopasses/{NORAD_ID}/{latitude}/{longitude}/{altitude}/"
            f"{days_forward}/{min_elevation}"
        )

    url = f"https://api.n2yo.com/rest/v1/satellite/{endpoint}/?apiKey={N2YO_API_KEY}"
    print("Запит:", url)

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        if data.get("info", {}).get("passescount", 0) == 0:
            await update.message.reply_text(
                "😔 У зазначений період прольотів не знайдено."
            )
            return

        msg = "📡 Найближчі прольоти МКС над Києвом:\n\n"
        for p in data["passes"]:
            start = datetime.utcfromtimestamp(p["startUTC"])
            # у visualpasses є готовий duration,
            # у radiopasses рахуємо по UTC-мітках
            duration = p.get("duration") or (p["endUTC"] - p["startUTC"])

            msg += (
                f"🔹 Початок: {start.strftime('%d.%m.%Y о %H:%M:%S UTC')}\n"
                f"  Тривалість: {duration} сек\n"
                f"  Макс. висота: {p['maxEl']}°\n"
                f"  Напрямок: від {p['startAzCompass']} до {p['endAzCompass']}\n\n"
            )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ Помилка: {e}")
        print("ISS-handler error:", e)

# /trek
async def trek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌖 Інтерактивні карти:\n"
        "• Moon Trek – https://trek.nasa.gov/moon\n"
        "• Mars Trek – https://trek.nasa.gov/mars\n"
        "• Vesta Trek – https://trek.nasa.gov/vesta"
    )

# Підготовка до інтерактивної космічної вікторини з 15 запитаннями (частина 1 — питання + логіка)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler

# ✅ Список запитань з варіантами
quiz_questions = [
    {
        "question": "Коли перші люди висадилися на Місяці?",
        "options": ["1965", "1969", "1972"],
        "answer": "1969"
    },
    {
        "question": "Скільки днів займає один оберт Місяця навколо Землі?",
        "options": ["14", "27", "30"],
        "answer": "27"
    },
    {
        "question": "Коли був запущений перший штучний супутник Землі?",
        "options": ["1957", "1961", "1969"],
        "answer": "1957"
    },
    {
        "question": "Хто був першою людиною в космосі?",
        "options": ["Ніл Армстронг", "Юрій Гагарін", "Джон Гленн"],
        "answer": "Юрій Гагарін"
    },
    {
        "question": "Яка планета найбільша у Сонячній системі?",
        "options": ["Земля", "Юпітер", "Сатурн"],
        "answer": "Юпітер"
    },
    {
        "question": "Скільки планет у Сонячній системі?",
        "options": ["8", "9", "10"],
        "answer": "8"
    },
    {
        "question": "Яка найближча зірка до Землі?",
        "options": ["Альфа Центавра", "Сонце", "Сіріус"],
        "answer": "Сонце"
    },
    {
        "question": "Який марсохід не належить NASA?",
        "options": ["Curiosity", "Perseverance", "Fobos-Grunt"],
        "answer": "Fobos-Grunt"
    },
    {
        "question": "Як називається перший успішний марсіанський зонд NASA?",
        "options": ["Viking 1", "Pathfinder", "Spirit"],
        "answer": "Viking 1"
    },
    {
        "question": "Скільки людей побувало на Місяці (станом на 2025)?",
        "options": ["6", "12", "24"],
        "answer": "12"
    },
    {
        "question": "Як називається телескоп, що замінив «Габбл»?",
        "options": ["Кеплер", "Джеймс Вебб", "Чандра"],
        "answer": "Джеймс Вебб"
    },
    {
        "question": "Скільки супутників Starlink на орбіті (орієнтовно 2025)?",
        "options": ["2500", "5000", "8000"],
        "answer": "8000"
    },
    {
        "question": "Яке тіло в Сонячній системі має найбільше вулканів?",
        "options": ["Венера", "Іо", "Меркурій"],
        "answer": "Іо"
    },
    {
        "question": "Що таке чорна діра?",
        "options": ["Планета", "Зірка", "Об'єкт гравітації"],
        "answer": "Об'єкт гравітації"
    },
    {
        "question": "Як називається галактика, в якій ми живемо?",
        "options": ["Андромеда", "Молочний Шлях", "Магелланова Хмара"],
        "answer": "Молочний Шлях"
    },
]

# Збереження стану вікторини (user_id -> index питання + результат)
user_quiz_state = {}

# /quiz — початок вікторини
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_quiz_state[user_id] = {"index": 0, "score": 0}
    await send_question(update, context, user_id)

# Надсилання поточного запитання
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    state = user_quiz_state[user_id]
    index = state["index"]
    if index >= len(quiz_questions):
        score = state["score"]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🏁 Вікторина завершена!\nТвій результат: {score}/{len(quiz_questions)}"
        )
        del user_quiz_state[user_id]
        return

    q = quiz_questions[index]
    buttons = [
        [InlineKeyboardButton(opt, callback_data=opt)] for opt in q["options"]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=user_id,
        text=f"❓ {q['question']}",
        reply_markup=reply_markup
    )

# Обробка відповіді користувача
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    answer = query.data
    await query.answer()

    state = user_quiz_state.get(user_id)
    if state is None:
        await query.edit_message_text("❗ Ця вікторина вже завершена або недоступна.")
        return

    index = state["index"]
    correct = quiz_questions[index]["answer"]

    if answer == correct:
        state["score"] += 1
        response = "✅ Правильно!"
    else:
        response = f"❌ Неправильно! Правильна відповідь: {correct}"

    await query.edit_message_text(response)
    state["index"] += 1
    await send_question(update, context, user_id)



# Відповіді на текст
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "привіт" in text:
        await update.message.reply_text("Привіт! 🚀")
    elif "як справи" in text:
        await update.message.reply_text("У космосі — супер! А в тебе?")
    else:
        await update.message.reply_text("Напиши /help, щоб дізнатися мої команди.")

# Старт
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("news", news))
app.add_handler(CommandHandler("apod", apod))
app.add_handler(CommandHandler("mars", mars))
app.add_handler(CommandHandler("asteroids", asteroids))
app.add_handler(CommandHandler("epic", epic))
app.add_handler(CommandHandler("exoplanet", exoplanet))
app.add_handler(CommandHandler("imagelibrary", image_search))
app.add_handler(CommandHandler("ssc", ssc))
app.add_handler(CommandHandler("iss", iss)) 
app.add_handler(CommandHandler("trek", trek))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CallbackQueryHandler(handle_answer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("🚀 CosmoBot запущено!")
app.run_polling()
