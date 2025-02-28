import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "7801672319:AAHwF0XcbyCmwpmmTl4z8XoT0yjS0LTOG10"  # 🔹 Замени на свой токен
CHAT_ID = -1002214740308  # 🔹 Замени на ID вашей группы (нужен с "-" для супергрупп!)

# Список дежурных
duty_list = ["Артемьева Маргарита", "Будрина Арина", "Венцов Андрей", "Ветренко Артем", "Дурягина Алеся", "Ершов Евгений",
      "Жилинский Тимур", "Заостровцев Михаил", "Кладовиков Кирилл", "Корякин Илья", "Котов Антон", "Лямин Максим", 
      "Макарьин Антон", "Малахов Егор", "Наумов Илья", "Невзоров Яков", "Панюков Данил", "Пекишев Роман", "Рыжков Данил", 
      "Сёмин Максим", "Соколова Дана ", "Стрижов Сергей", "Толстиков Даниил", "Тремба Иван", "Третьяков Владислав", "Тютрин Антон",
      "Уварова Арина", "Чирков Никита", "Шапоров Кирилл"]
duty_index = 0  # Индекс для выбора дежурных

bot = Bot(TOKEN)
dp = Dispatcher()

# Команда для смены списка дежурных (только для админов)
@dp.message(Command("set_duty"))
async def set_duty(message: Message):
    global duty_list, duty_index
    if message.chat.id != CHAT_ID:
        return  # Бот не реагирует на команды вне группы
    
    if message.from_user.id != 5191687357:  # 🔹 Замени на свой Telegram ID
        await message.reply("❌ У вас нет прав для выполнения этой команды.")
        return

    new_list = message.text.replace("/set_duty", "").strip().split(",")
    if len(new_list) < 2:
        await message.reply("❌ Минимум 2 дежурных!")
        return

    duty_list = [name.strip() for name in new_list]
    duty_index = 0  # Сбрасываем индекс
    await message.reply(f"✅ Новый список дежурных: {', '.join(duty_list)}")

# Функция выбора дежурных **по очереди**
def get_next_duty():
    global duty_index
    duty_today = [duty_list[duty_index % len(duty_list)], duty_list[(duty_index + 1) % len(duty_list)]]
    duty_index = (duty_index + 2) % len(duty_list)  # Увеличиваем индекс на 2 (чтобы не повторялись)
    return duty_today

# Функция отправки сообщения в 8:00
async def send_daily_message():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)  # 8:00 утра
        
        # Если текущее время уже позже 8:00, устанавливаем цель на следующий день
        if now > target_time:
            target_time += timedelta(days=1)
        
        # Пропуск выходных (суббота и воскресенье)
        while target_time.weekday() >= 5:  # 5 - суббота, 6 - воскресенье
            target_time += timedelta(days=1)
        
        sleep_time = (target_time - now).total_seconds()
        await asyncio.sleep(sleep_time)
        
        duty_today = get_next_duty()
        message = f"\U0001F468‍🏫 Дежурные на сегодня:\n- {duty_today[0]}\n- {duty_today[1]}"
        await bot.send_message(CHAT_ID, message, disable_notification=False)  # Отправка сообщения в группу

# Запускаем бота
async def main():
    asyncio.create_task(send_daily_message())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
