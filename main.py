import config
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from base import SQL

db = SQL('db.db')  # соединение с БД

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

#inline клавиатура
buttons = [
        [InlineKeyboardButton(text="Создать новый рандомизатор", callback_data="new_project")],
        [InlineKeyboardButton(text="Мои проекты", callback_data="projects")],
        [InlineKeyboardButton(text="Пользователь", callback_data="user")]
    ]
kb = InlineKeyboardMarkup(inline_keyboard=buttons)

buttons2 = [
        [InlineKeyboardButton(text="Зайти", callback_data="object_")]
    ]
kb2 = InlineKeyboardMarkup(inline_keyboard=buttons2)

#когда пользователь написал сообщение
@dp.message()
async def start(message):
    id = message.from_user.id
    status = db.get_field("users", id, "status")  # получаем статус пользователя
    if not db.user_exist(id):#если пользователя нет в бд
        db.add_user(id)#добавляем
    if status == 1:  # если пользователя нет в бд
        db.add_project(id,message.text)
        db.update_field("users", id, "status", 2)
        await message.answer("Теперь, вписывай объекты списка")
    if status == 1:  # если пользователя нет в бд
        db.add_project(id,message.text)
        db.update_field("users", id, "status", 2)
        await message.answer("Теперь, вписывай объекты списка")
    #db.update_field("users", id, "status", 1) #изменяем статус пользователя
    await message.answer("Выбери вариант!", reply_markup=kb)#отправка сообщения с клавиатурой


#когда пользователь нажал на inline кнопку
@dp.callback_query()
async def start_call(call):
    id = call.from_user.id
    if not db.user_exist(id):#если пользователя нет в бд
        db.add_user(id)#добавляем
    if call.data == "new_project":
        db.update_field("users", id, "status",1)
        await call.message.answer("Впишите название списка:")
    if call.data == "projects":
        projects = db.get_all("project")
        print(projects)
        for i in range(len(projects)):
            project_id, _, project_name = projects[i]
            if not projects:
                await call.answer("Вы ещё не создали ничего!")
                return
            await call.message.answer("Ваши проекты:")
            kb2 = [[InlineKeyboardButton(text="Зайти", callback_data=f"object_{project_id}")]]
            await call.message.answer(f"{project_name}", kb2)
    if "object_" in call.data:
        print()

    if call.data == "user":
        await call.message.answer("Это находится в разработке")
    #if call.data == "yes": проверка нажатия на кнопку
    #await call.answer("Оповещение сверху")
    #await call.message.answer("Отправка сообщения")
    #await call.message.edit_text("Редактирование сообщения")
    #await call.message.delete()#удаление сообщения
    await bot.answer_callback_query(call.id)#ответ на запрос, чтобы бот не зависал

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
