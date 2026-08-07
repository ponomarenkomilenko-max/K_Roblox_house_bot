import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5577614358

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


class Form(StatesGroup):
    name = State()
    age = State()
    roblox = State()
    photo = State()


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer(
        "Приветик! 💗\n"
        "Если ты хочешь в наш хаус, то заполни пожалуйста анкету:\n\n"
        "Имя/псевдоним:"
    )


@router.message(Form.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Возраст:")


@router.message(Form.age)
async def age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.roblox)
    await message.answer("Ник Roblox:")


@router.message(Form.roblox)
async def roblox(message: types.Message, state: FSMContext):
    await state.update_data(roblox=message.text)
    await state.set_state(Form.photo)
    await message.answer("Теперь отправь фото своего скина 📸")


@router.message(Form.photo, lambda m: m.photo)
async def photo(message: types.Message, state: FSMContext):
    data = await state.get_data()

    text = (
        "📨 Новая анкета!\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Ник Roblox: {data['roblox']}\n"
        f"Telegram: @{message.from_user.username}"
    )

    await bot.send_message(ADMIN_ID, text)
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id)

    await message.answer(
        "💗 Ваша анкета была отправлена!\n"
        "В течение суток к вам придет ответ "
        "(постараемся как можно скорее ответить 💗)"
    )

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
