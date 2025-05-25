from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram_bot.dialogs.states import CategoryDialog
from telegram_bot.keyboards.reply import (
    category_actions_keyboard,
    category_list_keyboard,
    confirm_keyboard,
)
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from database.mongo import get_category_names, delete_category_group, add_category_group


cat_router = Router()


@cat_router.message(Command("cats"))
async def start_categories_dialog(message: Message, state: FSMContext):
    user_id = message.from_user.id
    category_names = await get_category_names(user_id)

    await message.answer(
        "🏷 Your categories:\n" + "\n".join(f"- {c}" for c in category_names))
    await message.answer("What do you want to do?",
                         reply_markup=category_actions_keyboard())
    await state.set_state(CategoryDialog.ChoosingAction)


@cat_router.message(CategoryDialog.ChoosingAction, F.text == "➕ Add")
async def ask_new_category_name(message: Message, state: FSMContext):
    await message.answer("Enter the name of the new category:")
    await state.set_state(CategoryDialog.Adding)


@cat_router.message(CategoryDialog.Adding)
async def confirm_new_category(message: Message, state: FSMContext):
    await state.update_data(new_category=message.text.strip())
    await message.answer(
        f'Add "{message.text.strip()}" to your categories?',
        reply_markup=confirm_keyboard())
    await state.set_state(CategoryDialog.ConfirmAdd)


@cat_router.message(CategoryDialog.ConfirmAdd, F.text == "Yes")
async def ask_for_keywords(message: Message, state: FSMContext):
    data = await state.get_data()
    cat = data["new_category"]
    await message.answer(
        f'Now enter keywords for the category "{cat}" (comma-separated).\nExample: gym, trainer, weights'
    )
    await state.set_state(CategoryDialog.AddingKeywords)


@cat_router.message(CategoryDialog.ConfirmAdd, F.text == "No")
async def cancel_add_category(message: Message, state: FSMContext):
    await message.answer("❌ Cancelled.", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryDialog.ChoosingAction)



@cat_router.message(CategoryDialog.AddingKeywords)
async def save_category_with_keywords(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    cat = data["new_category"]

    # Parse and clean keywords
    raw_text = message.text.strip()
    key_words = [kw.strip() for kw in raw_text.split(",") if kw.strip()]

    if not key_words:
        await message.answer("❌ Please enter at least one keyword, separated by commas.")
        return

    await add_category_group(user_id, cat, key_words)

    await message.answer(
        f'✅ Category "{cat}" added with keywords: {", ".join(key_words)}',
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryDialog.ChoosingAction)


@cat_router.message(CategoryDialog.ChoosingAction, F.text == "🗑 Delete")
async def choose_category_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    category_names = await get_category_names(user_id)

    await message.answer(
        "Choose a category to delete:",
        reply_markup=category_list_keyboard(category_names))
    await state.set_state(CategoryDialog.DeletingChoose)


@cat_router.message(CategoryDialog.DeletingChoose)
async def confirm_delete_category(message: Message, state: FSMContext):
    cat = message.text.strip()
    await state.update_data(delete_category=cat)
    await message.answer(
        f'Delete "{cat}"? This action cannot be undone.',
        reply_markup=confirm_keyboard()
    )
    await state.set_state(CategoryDialog.ConfirmDelete)


@cat_router.message(CategoryDialog.ConfirmDelete, F.text == "Yes")
async def delete_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    cat = data["delete_category"]

    if await delete_category_group(user_id, cat):
        await message.answer("✅ Deleted successfully.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(
            "❌ Category not found.",
            reply_markup=category_actions_keyboard())
    await state.set_state(CategoryDialog.ChoosingAction)


@cat_router.message(CategoryDialog.ConfirmDelete, F.text == "No")
async def cancel_delete(message: Message, state: FSMContext):
    await message.answer("❌ Cancelled.", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryDialog.ChoosingAction)
