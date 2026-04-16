import config
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from base import SQL
from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy='http://proxy.server:3128')

db = SQL('db.db')  # соединение с БД

bot = Bot(token=config.TOKEN, session=session)
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
    if status == 11:  # если пользователя нет в бд
        db.add_project(id,message.text)
        db.update_field("users", id, "status", 1)
        await message.answer("Проект добавлен!")
    if status == 12:
        db.update_field("objects",id,"save", message.answer)
        await message.answer("ОбЪект добавлен!")

    #db.update_field("users", id, "status", 1) #изменяем статус пользователя
    await message.answer("Выбери вариант!", reply_markup=kb)#отправка сообщения с клавиатурой


#когда пользователь нажал на inline кнопку
@dp.callback_query()
async def start_call(call):
    id = call.from_user.id
    if not db.user_exist(id):#если пользователя нет в бд
        db.add_user(id)#добавляем
    if call.data == "new_project":
        db.update_field("users", id, "status",11)
        await call.message.answer("Впишите название списка:")
    if call.data == "projects":
        projects = db.get_all("project")
        print(projects)
        await call.message.answer("Ваши проекты:")
        for i in range(len(projects)):
            project_id, _, project_name = projects[i]
            if not projects:
                await call.answer("Вы ещё не создали ничего!")
                return
            buttons2 = [
                [InlineKeyboardButton(text="Зайти", callback_data=f"open_project_{project_id}")]
            ]
            kb2 = InlineKeyboardMarkup(inline_keyboard=buttons2)
            await call.message.answer(f"{project_name}", reply_markup=kb2 )
    if "open_project_" in call.data:
        project_id = int(call.data[13:])
        buttons2 = [
            [InlineKeyboardButton(text="Добавить объект", callback_data=f"add_object_{project_id}")],
            [InlineKeyboardButton(text="Удалить проект", callback_data=f"delete_project_{project_id}")]
        ]
        db.get_objects_by_project(id,project_id)
        kb2 = InlineKeyboardMarkup(inline_keyboard=buttons2)
        await call.message.answer("Доступные действия:", reply_markup=kb2)
    if "add_object_" in call.data:
        project_id = int(call.data[11:])
        project_name = db.get_field("project",project_id,"project_name")
        db.add_object(id,project_id,project_name)
        object_id = db.get_object_by_idk(id,project_id,project_name)
        db.update_field("users",id, "object_id", object_id)
        await call.message.answer("Впишите название объекта:")
        db.update_field("users", id, "status", 12)




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
