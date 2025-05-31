from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram_bot.dialogs.states import CategoryDialog
from telegram_bot.keyboards.reply import (
    category_actions_keyboard,
    category_list_keyboard,
    confirm_keyboard,
    cancel_button,
)
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from database.mongo import get_category_names, delete_category_group, add_category_group
from telegram_bot.handlers.manage_start import i18n
from telegram_bot.filters.text_i18n import TextI18nFilter
from database.redis import clear_state


cat_router = Router()


@cat_router.message(TextI18nFilter("buttons.cancel"))
async def cancel_action(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        await i18n.get(key="messages.cancel", user_id=user_id),
        reply_markup=ReplyKeyboardRemove()
    )
    await message.delete()

    await message.answer(
        await i18n.get(key="messages.start.help", user_id=user_id),
    )

    await clear_state(message.from_user.id)
    await state.clear()


@cat_router.message(Command("cats"))
async def start_categories_dialog(message: Message, state: FSMContext):
    user_id = message.from_user.id
    category_names = await get_category_names(user_id)
    cat_list_str = await i18n.get(key="messages.categories.cat_list", user_id=user_id)

    await message.answer(
        cat_list_str + "\n".join(f"- {c}" for c in category_names))
    await message.answer(
        await i18n.get(key="messages.categories.action_qa", user_id=user_id),
        reply_markup=await category_actions_keyboard(user_id),
    )
    await state.set_state(CategoryDialog.ChoosingAction)


@cat_router.message(CategoryDialog.ChoosingAction, TextI18nFilter("buttons.add_cat"))
async def ask_new_category_name(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        await i18n.get(key="messages.categories.ask_cat_name", user_id=message.from_user.id),
        reply_markup=await cancel_button(user_id)
    )
    await state.set_state(CategoryDialog.Adding)


@cat_router.message(CategoryDialog.Adding)
async def confirm_new_category(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(new_category=message.text.strip())
    await message.answer(
        await i18n.get(
            key="messages.categories.confirm_new_name",
            new_name=message.text.strip(),
            user_id=user_id),
        reply_markup=await confirm_keyboard(user_id=user_id)
    )
    await state.set_state(CategoryDialog.ConfirmAdd)


@cat_router.message(CategoryDialog.ConfirmAdd, TextI18nFilter("messages.confirm.yes"))
async def ask_for_keywords(message: Message, state: FSMContext):
    data = await state.get_data()
    cat = data["new_category"]
    await message.answer(
        await i18n.get(
            key="messages.categories.ask_key_words",
            cat=cat,
            user_id=message.from_user.id),
        parse_mode='Markdown',
        reply_markup=await cancel_button(message.from_user.id)
    )
    await state.set_state(CategoryDialog.AddingKeywords)


@cat_router.message(CategoryDialog.ConfirmAdd, TextI18nFilter("messages.confirm.no"))
async def cancel_add_category(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        await i18n.get(key="messages.cancel", user_id=user_id),
        reply_markup=ReplyKeyboardRemove()
    )
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
        await message.answer(
            await i18n.get(
                key="messages.categories.error",
                user_id=user_id,
            )
        )
        return

    await add_category_group(user_id, cat, key_words)

    await message.answer(
        await i18n.get(
            key="messages.categories.success_add",
            cat=cat,
            user_id=user_id,
        ) + ", ".join(key_words),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(CategoryDialog.ChoosingAction)


@cat_router.message(CategoryDialog.ChoosingAction, TextI18nFilter("buttons.del_cat"))
async def choose_category_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    category_names = await get_category_names(user_id)

    await message.answer(
        await i18n.get(
            key="messages.categories.ask_cat_del",
            user_id=user_id,
        ),
        reply_markup=await category_list_keyboard(category_names),
    )
    await state.set_state(CategoryDialog.DeletingChoose)


@cat_router.message(CategoryDialog.DeletingChoose)
async def confirm_delete_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cat = message.text.strip()

    await state.update_data(delete_category=cat)
    await message.answer(
        await i18n.get(
            key="messages.categories.confirm_del",
            cat=cat,
            user_id=user_id,
        ),
        reply_markup=await confirm_keyboard(user_id=user_id),
    )
    await state.set_state(CategoryDialog.ConfirmDelete)


@cat_router.message(CategoryDialog.ConfirmDelete, TextI18nFilter("messages.confirm.yes"))
async def delete_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    cat = data["delete_category"]

    if await delete_category_group(user_id, cat):
        await message.answer(
            await i18n.get(
                key="messages.categories.success_del",
                user_id=user_id,
            ),
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            await i18n.get(
                key="messages.categories.not_found_error",
                user_id=user_id,
            ),
            reply_markup=await category_actions_keyboard(user_id),
        )
    await state.set_state(CategoryDialog.ChoosingAction)


@cat_router.message(CategoryDialog.ConfirmDelete, TextI18nFilter("messages.confirm.no"))
async def cancel_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        await i18n.get(key="messages.cancel", user_id=user_id),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(CategoryDialog.ChoosingAction)
