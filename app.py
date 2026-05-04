{\rtf1\ansi\ansicpg1251\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import asyncio\
import sqlite3\
import datetime\
import os\
from aiogram import Bot, Dispatcher, types\
from aiogram.filters import Command\
from aiogram.fsm.state import State, StatesGroup\
from aiogram.fsm.context import FSMContext\
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove\
from apscheduler.schedulers.asyncio import AsyncIOScheduler\
\
TOKEN = os.environ.get("BOT_TOKEN")\
if not TOKEN:\
    print("\uc0\u1054 \u1064 \u1048 \u1041 \u1050 \u1040 : \u1053 \u1077  \u1085 \u1072 \u1081 \u1076 \u1077 \u1085  BOT_TOKEN \u1074  \u1087 \u1077 \u1088 \u1077 \u1084 \u1077 \u1085 \u1085 \u1099 \u1093  \u1086 \u1082 \u1088 \u1091 \u1078 \u1077 \u1085 \u1080 \u1103 ")\
    exit(1)\
\
bot = Bot(token=TOKEN)\
dp = Dispatcher()\
\
conn = sqlite3.connect('mood_tracker_multi.db', check_same_thread=False)\
cursor = conn.cursor()\
\
cursor.execute('''\
CREATE TABLE IF NOT EXISTS users (\
    user_id INTEGER PRIMARY KEY,\
    username TEXT,\
    first_date TEXT,\
    gender TEXT\
)\
''')\
conn.commit()\
\
cursor.execute('''\
CREATE TABLE IF NOT EXISTS mood_log (\
    id INTEGER PRIMARY KEY AUTOINCREMENT,\
    user_id INTEGER,\
    date TEXT,\
    gender TEXT,\
    cycle TEXT,\
    weather TEXT,\
    sleep_norm BOOLEAN,\
    bad_sleep BOOLEAN,\
    work_tasks BOOLEAN,\
    fatigue BOOLEAN,\
    hunger BOOLEAN,\
    sugar_spikes BOOLEAN,\
    caffeine BOOLEAN,\
    alcohol BOOLEAN,\
    water_norm BOOLEAN,\
    vitamins BOOLEAN,\
    pms BOOLEAN,\
    menstruation BOOLEAN,\
    emotion_suppression BOOLEAN,\
    self_criticism BOOLEAN,\
    procrastination BOOLEAN,\
    conflicts BOOLEAN,\
    loneliness BOOLEAN,\
    devalued BOOLEAN,\
    bad_news BOOLEAN,\
    phone_glued BOOLEAN,\
    tactility BOOLEAN,\
    self_care BOOLEAN,\
    pleasant_comm BOOLEAN,\
    walk BOOLEAN,\
    sport BOOLEAN,\
    mood INTEGER,\
    feeling TEXT,\
    UNIQUE(user_id, date)\
)\
''')\
conn.commit()\
\
yes_no = ReplyKeyboardMarkup(\
    keyboard=[[KeyboardButton(text="\uc0\u9989  \u1044 \u1072 "), KeyboardButton(text="\u10060  \u1053 \u1077 \u1090 ")]],\
    resize_keyboard=True\
)\
\
gender_kb = ReplyKeyboardMarkup(\
    keyboard=[[KeyboardButton(text="\uc0\u55357 \u56425  \u1046 \u1077 \u1085 \u1097 \u1080 \u1085 \u1072 "), KeyboardButton(text="\u55357 \u56424  \u1052 \u1091 \u1078 \u1095 \u1080 \u1085 \u1072 ")]],\
    resize_keyboard=True\
)\
\
cycle_kb = ReplyKeyboardMarkup(\
    keyboard=[\
        [KeyboardButton(text="\uc0\u55356 \u57144  \u1060 \u1086 \u1083 \u1083 \u1080 \u1082 \u1091 \u1083 \u1103 \u1088 \u1085 \u1072 \u1103 ")],\
        [KeyboardButton(text="\uc0\u55357 \u56475  \u1054 \u1074 \u1091 \u1083 \u1103 \u1094 \u1080 \u1103 ")],\
        [KeyboardButton(text="\uc0\u55356 \u57113  \u1051 \u1102 \u1090 \u1077 \u1080 \u1085 \u1086 \u1074 \u1072 \u1103  (\u1055 \u1052 \u1057 )")],\
        [KeyboardButton(text="\uc0\u55358 \u56952  \u1052 \u1077 \u1085 \u1089 \u1090 \u1088 \u1091 \u1072 \u1094 \u1080 \u1103 ")]\
    ],\
    resize_keyboard=True\
)\
\
weather_kb = ReplyKeyboardMarkup(\
    keyboard=[\
        [KeyboardButton(text="\uc0\u9728 \u65039  \u1057 \u1086 \u1083 \u1085 \u1077 \u1095 \u1085 \u1086 "), KeyboardButton(text="\u9925  \u1054 \u1073 \u1083 \u1072 \u1095 \u1085 \u1086 ")],\
        [KeyboardButton(text="\uc0\u9729 \u65039  \u1055 \u1072 \u1089 \u1084 \u1091 \u1088 \u1085 \u1086 "), KeyboardButton(text="\u55356 \u57127 \u65039  \u1044 \u1086 \u1078 \u1076 \u1100 ")]\
    ],\
    resize_keyboard=True\
)\
\
mood_kb = ReplyKeyboardMarkup(\
    keyboard=[\
        [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3"), KeyboardButton(text="4"), KeyboardButton(text="5")],\
        [KeyboardButton(text="6"), KeyboardButton(text="7"), KeyboardButton(text="8"), KeyboardButton(text="9"), KeyboardButton(text="10")]\
    ],\
    resize_keyboard=True\
)\
\
feeling_kb = ReplyKeyboardMarkup(\
    keyboard=[\
        [KeyboardButton(text="\uc0\u55357 \u56842  \u1056 \u1072 \u1076 \u1086 \u1089 \u1090 \u1100 "), KeyboardButton(text="\u55357 \u56844  \u1057 \u1087 \u1086 \u1082 \u1086 \u1081 \u1089 \u1090 \u1074 \u1080 \u1077 "), KeyboardButton(text="\u55357 \u56866  \u1043 \u1088 \u1091 \u1089 \u1090 \u1100 ")],\
        [KeyboardButton(text="\uc0\u55357 \u56864  \u1047 \u1083 \u1086 \u1089 \u1090 \u1100 "), KeyboardButton(text="\u55357 \u56880  \u1058 \u1088 \u1077 \u1074 \u1086 \u1075 \u1072 "), KeyboardButton(text="\u55357 \u56852  \u1040 \u1087 \u1072 \u1090 \u1080 \u1103 ")],\
        [KeyboardButton(text="\uc0\u55357 \u56911  \u1041 \u1083 \u1072 \u1075 \u1086 \u1076 \u1072 \u1088 \u1085 \u1086 \u1089 \u1090 \u1100 "), KeyboardButton(text="\u55358 \u56596  \u1056 \u1072 \u1079 \u1076 \u1088 \u1072 \u1078 \u1077 \u1085 \u1080 \u1077 "), KeyboardButton(text="\u55357 \u56490  \u1059 \u1074 \u1077 \u1088 \u1077 \u1085 \u1085 \u1086 \u1089 \u1090 \u1100 ")],\
        [KeyboardButton(text="\uc0\u55357 \u56851  \u1059 \u1089 \u1090 \u1072 \u1083 \u1086 \u1089 \u1090 \u1100 "), KeyboardButton(text="\u55358 \u56688  \u1042 \u1076 \u1086 \u1093 \u1085 \u1086 \u1074 \u1077 \u1085 \u1080 \u1077 "), KeyboardButton(text="\u55358 \u57026  \u1054 \u1076 \u1080 \u1085 \u1086 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086 ")]\
    ],\
    resize_keyboard=True\
)\
\
class MoodForm(StatesGroup):\
    gender = State()\
    cycle = State()\
    weather = State()\
    sleep_norm = State()\
    bad_sleep = State()\
    work_tasks = State()\
    fatigue = State()\
    hunger = State()\
    sugar_spikes = State()\
    caffeine = State()\
    alcohol = State()\
    water_norm = State()\
    pms = State()\
    menstruation = State()\
    vitamins = State()\
    emotion_suppression = State()\
    self_criticism = State()\
    procrastination = State()\
    conflicts = State()\
    loneliness = State()\
    devalued = State()\
    bad_news = State()\
    phone_glued = State()\
    tactility = State()\
    self_care = State()\
    pleasant_comm = State()\
    walk = State()\
    sport = State()\
    mood = State()\
    feeling = State()\
\
async def ask_yes_no(message: types.Message, state: FSMContext, field: str, next_state, question: str):\
    if message.text == "\uc0\u9989  \u1044 \u1072 ":\
        await state.update_data(**\{field: True\})\
    elif message.text == "\uc0\u10060  \u1053 \u1077 \u1090 ":\
        await state.update_data(**\{field: False\})\
    else:\
        await message.answer("\uc0\u1053 \u1072 \u1078 \u1084 \u1080  \u9989  \u1044 \u1072  \u1080 \u1083 \u1080  \u10060  \u1053 \u1077 \u1090 ")\
        return\
    await message.answer(question, reply_markup=yes_no)\
    await state.set_state(next_state)\
\
def register_user(user_id, username, gender):\
    today = datetime.date.today().isoformat()\
    cursor.execute('''\
        INSERT OR IGNORE INTO users (user_id, username, first_date, gender)\
        VALUES (?, ?, ?, ?)\
    ''', (user_id, username, today, gender))\
    conn.commit()\
\
def user_exists(user_id):\
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))\
    return cursor.fetchone() is not None\
\
@dp.message(Command("start"))\
async def cmd_start(message: types.Message, state: FSMContext):\
    user_id = message.from_user.id\
    today = datetime.date.today().isoformat()\
    \
    cursor.execute('SELECT date FROM mood_log WHERE user_id = ? AND date = ?', (user_id, today))\
    if cursor.fetchone():\
        await message.answer("\uc0\u55357 \u56541  \u1047 \u1072  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1091 \u1078 \u1077  \u1079 \u1072 \u1087 \u1086 \u1083 \u1085 \u1077 \u1085 \u1086 ! \u1042 \u1086 \u1079 \u1074 \u1088 \u1072 \u1097 \u1072 \u1081 \u1089 \u1103  \u1079 \u1072 \u1074 \u1090 \u1088 \u1072 .")\
        return\
    \
    if not user_exists(user_id):\
        await message.answer(\
            "\uc0\u55357 \u56395  \u1055 \u1088 \u1080 \u1074 \u1077 \u1090 ! \u1071  \u1073 \u1086 \u1090 -\u1090 \u1088 \u1077 \u1082 \u1077 \u1088  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1085 \u1080 \u1103 .\\n\\n"\
            "\uc0\u1057 \u1085 \u1072 \u1095 \u1072 \u1083 \u1072  \u1091 \u1082 \u1072 \u1078 \u1080  \u1089 \u1074 \u1086 \u1081  \u1087 \u1086 \u1083 :",\
            reply_markup=gender_kb\
        )\
        await state.set_state(MoodForm.gender)\
    else:\
        cursor.execute('SELECT gender FROM users WHERE user_id = ?', (user_id,))\
        gender = cursor.fetchone()[0]\
        await state.update_data(gender=gender)\
        \
        if gender == "\uc0\u55357 \u56424  \u1052 \u1091 \u1078 \u1095 \u1080 \u1085 \u1072 ":\
            await state.update_data(cycle="\uc0\u1053 \u1077  \u1087 \u1088 \u1080 \u1084 \u1077 \u1085 \u1080 \u1084 \u1086 ", pms=False, menstruation=False)\
            await message.answer("\uc0\u9729 \u65039  \u1050 \u1072 \u1082 \u1072 \u1103  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1087 \u1086 \u1075 \u1086 \u1076 \u1072 ?", reply_markup=weather_kb)\
            await state.set_state(MoodForm.weather)\
        else:\
            await message.answer("\uc0\u55356 \u57144  \u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1092 \u1072 \u1079 \u1091  \u1094 \u1080 \u1082 \u1083 \u1072 :", reply_markup=cycle_kb)\
            await state.set_state(MoodForm.cycle)\
\
@dp.message(MoodForm.gender)\
async def q_gender(message: types.Message, state: FSMContext):\
    if message.text not in ["\uc0\u55357 \u56425  \u1046 \u1077 \u1085 \u1097 \u1080 \u1085 \u1072 ", "\u55357 \u56424  \u1052 \u1091 \u1078 \u1095 \u1080 \u1085 \u1072 "]:\
        await message.answer("\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1087 \u1086 \u1083  \u1080 \u1079  \u1082 \u1085 \u1086 \u1087 \u1086 \u1082  \u55357 \u56391 ")\
        return\
    \
    gender = message.text\
    user_id = message.from_user.id\
    username = message.from_user.username or message.from_user.first_name\
    \
    register_user(user_id, username, gender)\
    await state.update_data(gender=gender)\
    \
    if gender == "\uc0\u55357 \u56424  \u1052 \u1091 \u1078 \u1095 \u1080 \u1085 \u1072 ":\
        await state.update_data(cycle="\uc0\u1053 \u1077  \u1087 \u1088 \u1080 \u1084 \u1077 \u1085 \u1080 \u1084 \u1086 ", pms=False, menstruation=False)\
        await message.answer("\uc0\u9729 \u65039  \u1050 \u1072 \u1082 \u1072 \u1103  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1087 \u1086 \u1075 \u1086 \u1076 \u1072 ?", reply_markup=weather_kb)\
        await state.set_state(MoodForm.weather)\
    else:\
        await message.answer("\uc0\u55356 \u57144  \u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1092 \u1072 \u1079 \u1091  \u1094 \u1080 \u1082 \u1083 \u1072 :", reply_markup=cycle_kb)\
        await state.set_state(MoodForm.cycle)\
\
@dp.message(MoodForm.cycle)\
async def q_cycle(message: types.Message, state: FSMContext):\
    if message.text not in ["\uc0\u55356 \u57144  \u1060 \u1086 \u1083 \u1083 \u1080 \u1082 \u1091 \u1083 \u1103 \u1088 \u1085 \u1072 \u1103 ", "\u55357 \u56475  \u1054 \u1074 \u1091 \u1083 \u1103 \u1094 \u1080 \u1103 ", "\u55356 \u57113  \u1051 \u1102 \u1090 \u1077 \u1080 \u1085 \u1086 \u1074 \u1072 \u1103  (\u1055 \u1052 \u1057 )", "\u55358 \u56952  \u1052 \u1077 \u1085 \u1089 \u1090 \u1088 \u1091 \u1072 \u1094 \u1080 \u1103 "]:\
        await message.answer("\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1092 \u1072 \u1079 \u1091  \u1080 \u1079  \u1082 \u1085 \u1086 \u1087 \u1086 \u1082  \u55357 \u56391 ")\
        return\
    await state.update_data(cycle=message.text)\
    await message.answer("\uc0\u9729 \u65039  \u1050 \u1072 \u1082 \u1072 \u1103  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103  \u1087 \u1086 \u1075 \u1086 \u1076 \u1072 ?", reply_markup=weather_kb)\
    await state.set_state(MoodForm.weather)\
\
@dp.message(MoodForm.weather)\
async def q_weather(message: types.Message, state: FSMContext):\
    if message.text not in ["\uc0\u9728 \u65039  \u1057 \u1086 \u1083 \u1085 \u1077 \u1095 \u1085 \u1086 ", "\u9925  \u1054 \u1073 \u1083 \u1072 \u1095 \u1085 \u1086 ", "\u9729 \u65039  \u1055 \u1072 \u1089 \u1084 \u1091 \u1088 \u1085 \u1086 ", "\u55356 \u57127 \u65039  \u1044 \u1086 \u1078 \u1076 \u1100 "]:\
        await message.answer("\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1087 \u1086 \u1075 \u1086 \u1076 \u1091  \u1080 \u1079  \u1082 \u1085 \u1086 \u1087 \u1086 \u1082  \u55357 \u56391 ")\
        return\
    await state.update_data(weather=message.text)\
    await message.answer("\uc0\u55357 \u56884  \u1053 \u1086 \u1088 \u1084 \u1072  \u1089 \u1085 \u1072  (7-8 \u1095 \u1072 \u1089 \u1086 \u1074 )?", reply_markup=yes_no)\
    await state.set_state(MoodForm.sleep_norm)\
\
@dp.message(MoodForm.sleep_norm)\
async def q_sleep_norm(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "sleep_norm", MoodForm.bad_sleep, "\uc0\u55356 \u57113  \u1041 \u1099 \u1083  \u1073 \u1077 \u1089 \u1087 \u1086 \u1082 \u1086 \u1081 \u1085 \u1099 \u1081  \u1089 \u1086 \u1085 ?")\
\
@dp.message(MoodForm.bad_sleep)\
async def q_bad_sleep(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "bad_sleep", MoodForm.work_tasks, "\uc0\u55357 \u56425 \u8205 \u55357 \u56507  \u1041 \u1099 \u1083 \u1080  \u1088 \u1072 \u1073 \u1086 \u1095 \u1080 \u1077  \u1079 \u1072 \u1076 \u1072 \u1095 \u1080 ?")\
\
@dp.message(MoodForm.work_tasks)\
async def q_work_tasks(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "work_tasks", MoodForm.fatigue, "\uc0\u9889  \u1063 \u1091 \u1074 \u1089 \u1090 \u1074 \u1086 \u1074 \u1072 \u1083 (\u1072 ) \u1091 \u1089 \u1090 \u1072 \u1083 \u1086 \u1089 \u1090 \u1100 ?")\
\
@dp.message(MoodForm.fatigue)\
async def q_fatigue(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "fatigue", MoodForm.hunger, "\uc0\u55356 \u57213 \u65039  \u1041 \u1099 \u1083  \u1089 \u1080 \u1083 \u1100 \u1085 \u1099 \u1081  \u1075 \u1086 \u1083 \u1086 \u1076 ?")\
\
@dp.message(MoodForm.hunger)\
async def q_hunger(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "hunger", MoodForm.sugar_spikes, "\uc0\u55356 \u57196  \u1041 \u1099 \u1083 \u1080  \u1089 \u1082 \u1072 \u1095 \u1082 \u1080  \u1089 \u1072 \u1093 \u1072 \u1088 \u1072 ?")\
\
@dp.message(MoodForm.sugar_spikes)\
async def q_sugar_spikes(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "sugar_spikes", MoodForm.caffeine, "\uc0\u9749  \u1055 \u1080 \u1083 (\u1072 ) \u1082 \u1086 \u1092 \u1077 \u1080 \u1085 ?")\
\
@dp.message(MoodForm.caffeine)\
async def q_caffeine(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "caffeine", MoodForm.alcohol, "\uc0\u55358 \u56642  \u1041 \u1099 \u1083  \u1072 \u1083 \u1082 \u1086 \u1075 \u1086 \u1083 \u1100 ?")\
\
@dp.message(MoodForm.alcohol)\
async def q_alcohol(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "alcohol", MoodForm.water_norm, "\uc0\u55357 \u56487  \u1042 \u1099 \u1087 \u1080 \u1083 (\u1072 ) \u1085 \u1086 \u1088 \u1084 \u1091  \u1074 \u1086 \u1076 \u1099 ?")\
\
@dp.message(MoodForm.water_norm)\
async def q_water_norm(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "water_norm", MoodForm.vitamins, "\uc0\u55357 \u56458  \u1055 \u1088 \u1080 \u1085 \u1080 \u1084 \u1072 \u1083 (\u1072 ) \u1074 \u1080 \u1090 \u1072 \u1084 \u1080 \u1085 \u1099 /\u1041 \u1040 \u1044 \u1099  \u1089 \u1077 \u1075 \u1086 \u1076 \u1085 \u1103 ?")\
\
@dp.message(MoodForm.vitamins)\
async def q_vitamins(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "vitamins", MoodForm.emotion_suppression, "\uc0\u55357 \u56868  \u1055 \u1086 \u1076 \u1072 \u1074 \u1083 \u1103 \u1083 (\u1072 ) \u1101 \u1084 \u1086 \u1094 \u1080 \u1080 ?")\
\
@dp.message(MoodForm.emotion_suppression)\
async def q_emotion_suppression(message: types.Message, state: FSMContext):\
    data = await state.get_data()\
    if data.get('gender') == "\uc0\u55357 \u56424  \u1052 \u1091 \u1078 \u1095 \u1080 \u1085 \u1072 ":\
        await ask_yes_no(message, state, "emotion_suppression", MoodForm.self_criticism, "\uc0\u55357 \u56803 \u65039  \u1041 \u1099 \u1083 (\u1072 ) \u1089 \u1072 \u1084 \u1086 \u1082 \u1088 \u1080 \u1090 \u1080 \u1095 \u1077 \u1085 (\u1072 )?")\
    else:\
        await ask_yes_no(message, state, "emotion_suppression", MoodForm.pms, "\uc0\u55358 \u56952  \u1045 \u1089 \u1090 \u1100  \u1055 \u1052 \u1057 ?")\
\
@dp.message(MoodForm.pms)\
async def q_pms(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "pms", MoodForm.menstruation, "\uc0\u55358 \u56952  \u1048 \u1076 \u1091 \u1090  \u1084 \u1077 \u1089 \u1103 \u1095 \u1085 \u1099 \u1077 ?")\
\
@dp.message(MoodForm.menstruation)\
async def q_menstruation(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "menstruation", MoodForm.self_criticism, "\uc0\u55357 \u56803 \u65039  \u1041 \u1099 \u1083 (\u1072 ) \u1089 \u1072 \u1084 \u1086 \u1082 \u1088 \u1080 \u1090 \u1080 \u1095 \u1077 \u1085 (\u1072 )?")\
\
@dp.message(MoodForm.self_criticism)\
async def q_self_criticism(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "self_criticism", MoodForm.procrastination, "\uc0\u9200  \u1055 \u1088 \u1086 \u1082 \u1088 \u1072 \u1089 \u1090 \u1080 \u1085 \u1080 \u1088 \u1086 \u1074 \u1072 \u1083 (\u1072 )?")\
\
@dp.message(MoodForm.procrastination)\
async def q_procrastination(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "procrastination", MoodForm.conflicts, "\uc0\u55357 \u56485  \u1041 \u1099 \u1083 \u1080  \u1082 \u1086 \u1085 \u1092 \u1083 \u1080 \u1082 \u1090 \u1099 ?")\
\
@dp.message(MoodForm.conflicts)\
async def q_conflicts(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "conflicts", MoodForm.loneliness, "\uc0\u55357 \u56852  \u1063 \u1091 \u1074 \u1089 \u1090 \u1074 \u1086 \u1074 \u1072 \u1083 (\u1072 ) \u1086 \u1076 \u1080 \u1085 \u1086 \u1095 \u1077 \u1089 \u1090 \u1074 \u1086 ?")\
\
@dp.message(MoodForm.loneliness)\
async def q_loneliness(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "loneliness", MoodForm.devalued, "\uc0\u55357 \u56398  \u1054 \u1073 \u1077 \u1089 \u1094 \u1077 \u1085 \u1080 \u1083 \u1080  \u1080 \u1083 \u1080  \u1085 \u1072 \u1093 \u1072 \u1084 \u1080 \u1083 \u1080 ?")\
\
@dp.message(MoodForm.devalued)\
async def q_devalued(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "devalued", MoodForm.bad_news, "\uc0\u55357 \u56560  \u1063 \u1080 \u1090 \u1072 \u1083 (\u1072 ) \u1085 \u1077 \u1075 \u1072 \u1090 \u1080 \u1074 \u1085 \u1099 \u1077  \u1085 \u1086 \u1074 \u1086 \u1089 \u1090 \u1080 ?")\
\
@dp.message(MoodForm.bad_news)\
async def q_bad_news(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "bad_news", MoodForm.phone_glued, "\uc0\u55357 \u56561  \u1047 \u1072 \u1083 \u1080 \u1087 \u1072 \u1083 (\u1072 ) \u1074  \u1090 \u1077 \u1083 \u1077 \u1092 \u1086 \u1085 \u1077  >2 \u1095 \u1072 \u1089 \u1086 \u1074 ?")\
\
@dp.message(MoodForm.phone_glued)\
async def q_phone_glued(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "phone_glued", MoodForm.tactility, "\uc0\u55358 \u56599  \u1041 \u1099 \u1083 \u1072  \u1090 \u1072 \u1082 \u1090 \u1080 \u1083 \u1100 \u1085 \u1086 \u1089 \u1090 \u1100  (\u1086 \u1073 \u1098 \u1103 \u1090 \u1080 \u1103  \u1080  \u1090 .\u1087 .)?")\
\
@dp.message(MoodForm.tactility)\
async def q_tactility(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "tactility", MoodForm.self_care, "\uc0\u55358 \u56820  \u1041 \u1099 \u1083  \u1091 \u1093 \u1086 \u1076  \u1079 \u1072  \u1089 \u1086 \u1073 \u1086 \u1081 /\u1079 \u1072 \u1073 \u1086 \u1090 \u1072  \u1086  \u1089 \u1077 \u1073 \u1077 ?")\
\
@dp.message(MoodForm.self_care)\
async def q_self_care(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "self_care", MoodForm.pleasant_comm, "\uc0\u55357 \u56492  \u1041 \u1099 \u1083 \u1086  \u1087 \u1088 \u1080 \u1103 \u1090 \u1085 \u1086 \u1077  \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077 ?")\
\
@dp.message(MoodForm.pleasant_comm)\
async def q_pleasant_comm(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "pleasant_comm", MoodForm.walk, "\uc0\u55357 \u57014  \u1041 \u1099 \u1083 (\u1072 ) \u1085 \u1072  \u1087 \u1088 \u1086 \u1075 \u1091 \u1083 \u1082 \u1077 ?")\
\
@dp.message(MoodForm.walk)\
async def q_walk(message: types.Message, state: FSMContext):\
    await ask_yes_no(message, state, "walk", MoodForm.sport, "\uc0\u55356 \u57283  \u1041 \u1099 \u1083  \u1089 \u1087 \u1086 \u1088 \u1090  \u1080 \u1083 \u1080  \u1092 \u1080 \u1079 . \u1072 \u1082 \u1090 \u1080 \u1074 \u1085 \u1086 \u1089 \u1090 \u1100 ?")\
\
@dp.message(MoodForm.sport)\
async def q_sport(message: types.Message, state: FSMContext):\
    if message.text == "\uc0\u9989  \u1044 \u1072 ":\
        await state.update_data(sport=True)\
    elif message.text == "\uc0\u10060  \u1053 \u1077 \u1090 ":\
        await state.update_data(sport=False)\
    else:\
        await message.answer("\uc0\u1053 \u1072 \u1078 \u1084 \u1080  \u9989  \u1044 \u1072  \u1080 \u1083 \u1080  \u10060  \u1053 \u1077 \u1090 ")\
        return\
    await message.answer("\uc0\u55356 \u57263  \u1054 \u1094 \u1077 \u1085 \u1080  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1085 \u1080 \u1077  \u1086 \u1090  1 \u1076 \u1086  10:", reply_markup=mood_kb)\
    await state.set_state(MoodForm.mood)\
\
@dp.message(MoodForm.mood)\
async def q_mood(message: types.Message, state: FSMContext):\
    if not message.text.isdigit() or int(message.text) not in range(1, 11):\
        await message.answer("\uc0\u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1095 \u1080 \u1089 \u1083 \u1086  \u1086 \u1090  1 \u1076 \u1086  10 \u1085 \u1072  \u1082 \u1085 \u1086 \u1087 \u1082 \u1072 \u1093  \u55357 \u56391 ")\
        return\
    await state.update_data(mood=int(message.text))\
    await message.answer("\uc0\u55357 \u56493  \u1050 \u1072 \u1082 \u1086 \u1077  \u1075 \u1083 \u1072 \u1074 \u1085 \u1086 \u1077  \u1095 \u1091 \u1074 \u1089 \u1090 \u1074 \u1086  \u1076 \u1085 \u1103 ?", reply_markup=feeling_kb)\
    await state.set_state(MoodForm.feeling)\
\
@dp.message(MoodForm.feeling)\
async def q_feeling(message: types.Message, state: FSMContext):\
    await state.update_data(feeling=message.text)\
    \
    data = await state.get_data()\
    user_id = message.from_user.id\
    today = datetime.date.today().isoformat()\
    \
    cursor.execute('''\
        INSERT INTO mood_log (\
            user_id, date, gender, cycle, weather, sleep_norm, bad_sleep, work_tasks, fatigue, hunger,\
            sugar_spikes, caffeine, alcohol, water_norm, vitamins, pms, menstruation,\
            emotion_suppression, self_criticism, procrastination, conflicts, loneliness,\
            devalued, bad_news, phone_glued, tactility, self_care, pleasant_comm, walk, sport, mood, feeling\
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)\
    ''', (\
        user_id, today, data['gender'], data.get('cycle', '\uc0\u1053 \u1077  \u1087 \u1088 \u1080 \u1084 \u1077 \u1085 \u1080 \u1084 \u1086 '), data['weather'],\
        data['sleep_norm'], data['bad_sleep'], data['work_tasks'], data['fatigue'],\
        data['hunger'], data['sugar_spikes'], data['caffeine'], data['alcohol'],\
        data['water_norm'], data['vitamins'], data.get('pms', False), data.get('menstruation', False),\
        data['emotion_suppression'], data['self_criticism'], data['procrastination'],\
        data['conflicts'], data['loneliness'], data['devalued'], data['bad_news'],\
        data['phone_glued'], data['tactility'], data['self_care'], data['pleasant_comm'],\
        data['walk'], data['sport'], data['mood'], data['feeling']\
    ))\
    conn.commit()\
    \
    await message.answer("\uc0\u9989  \u1044 \u1072 \u1085 \u1085 \u1099 \u1077  \u1089 \u1086 \u1093 \u1088 \u1072 \u1085 \u1077 \u1085 \u1099 !\\n\\n\u1050 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099 :\\n/stats \'97 \u1084 \u1086 \u1103  \u1089 \u1090 \u1072 \u1090 \u1080 \u1089 \u1090 \u1080 \u1082 \u1072 \\n/insights \'97 \u1072 \u1085 \u1072 \u1083 \u1080 \u1090 \u1080 \u1082 \u1072 ")\
    await state.clear()\
\
@dp.message(Command("stats"))\
async def show_stats(message: types.Message):\
    user_id = message.from_user.id\
    \
    cursor.execute('SELECT mood, feeling, date FROM mood_log WHERE user_id = ? ORDER BY date DESC LIMIT 7', (user_id,))\
    last_days = cursor.fetchall()\
    \
    cursor.execute('SELECT AVG(mood) FROM mood_log WHERE user_id = ?', (user_id,))\
    avg_mood = cursor.fetchone()[0]\
    if avg_mood is None:\
        avg_mood = 0\
    avg_mood = round(avg_mood, 1)\
    \
    cursor.execute('SELECT COUNT(*) FROM mood_log WHERE user_id = ?', (user_id,))\
    total_days = cursor.fetchone()[0]\
    \
    stats = f"\uc0\u55357 \u56522  \u1058 \u1042 \u1054 \u1071  \u1057 \u1058 \u1040 \u1058 \u1048 \u1057 \u1058 \u1048 \u1050 \u1040 \\n\\n\u55357 \u56517  \u1042 \u1089 \u1077 \u1075 \u1086  \u1076 \u1085 \u1077 \u1081 : \{total_days\}\\n\u55356 \u57119  \u1057 \u1088 \u1077 \u1076 \u1085 \u1077 \u1077  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1085 \u1080 \u1077 : \{avg_mood\}/10\\n\\n\u55357 \u56517  \u1055 \u1086 \u1089 \u1083 \u1077 \u1076 \u1085 \u1080 \u1077  \u1076 \u1085 \u1080 :\\n"\
    for mood, feeling, date in last_days[:5]:\
        stats += f"\'95 \{date\}: \{mood\}/10 \'97 \{feeling\}\\n"\
    await message.answer(stats)\
\
@dp.message(Command("insights"))\
async def show_insights(message: types.Message):\
    user_id = message.from_user.id\
    cursor.execute('SELECT * FROM mood_log WHERE user_id = ? ORDER BY date DESC', (user_id,))\
    rows = cursor.fetchall()\
    \
    if len(rows) < 3:\
        await message.answer("\uc0\u55357 \u56522  \u1053 \u1091 \u1078 \u1085 \u1086  \u1084 \u1080 \u1085 \u1080 \u1084 \u1091 \u1084  3 \u1076 \u1085 \u1103  \u1079 \u1072 \u1087 \u1080 \u1089 \u1077 \u1081  \u1076 \u1083 \u1103  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1072 .")\
        return\
    \
    factors = \{\
        "\uc0\u55357 \u56884  \u1053 \u1077 \u1076 \u1086 \u1089 \u1099 \u1087 ": "sleep_norm", "\u55356 \u57113  \u1041 \u1077 \u1089 \u1087 \u1086 \u1082 \u1086 \u1081 \u1085 \u1099 \u1081  \u1089 \u1086 \u1085 ": "bad_sleep", "\u55357 \u56425 \u8205 \u55357 \u56507  \u1056 \u1072 \u1073 \u1086 \u1095 \u1080 \u1077  \u1079 \u1072 \u1076 \u1072 \u1095 \u1080 ": "work_tasks",\
        "\uc0\u9889  \u1059 \u1089 \u1090 \u1072 \u1083 \u1086 \u1089 \u1090 \u1100 ": "fatigue", "\u9749  \u1050 \u1086 \u1092 \u1077 \u1080 \u1085 ": "caffeine", "\u55358 \u56642  \u1040 \u1083 \u1082 \u1086 \u1075 \u1086 \u1083 \u1100 ": "alcohol",\
        "\uc0\u55357 \u56458  \u1042 \u1080 \u1090 \u1072 \u1084 \u1080 \u1085 \u1099 ": "vitamins", "\u55357 \u56868  \u1055 \u1086 \u1076 \u1072 \u1074 \u1083 \u1077 \u1085 \u1080 \u1077  \u1101 \u1084 \u1086 \u1094 \u1080 \u1081 ": "emotion_suppression", "\u55357 \u56485  \u1050 \u1086 \u1085 \u1092 \u1083 \u1080 \u1082 \u1090 \u1099 ": "conflicts",\
        "\uc0\u55358 \u56599  \u1058 \u1072 \u1082 \u1090 \u1080 \u1083 \u1100 \u1085 \u1086 \u1089 \u1090 \u1100 ": "tactility", "\u55358 \u56820  \u1059 \u1093 \u1086 \u1076  \u1079 \u1072  \u1089 \u1086 \u1073 \u1086 \u1081 ": "self_care", "\u55357 \u56492  \u1055 \u1088 \u1080 \u1103 \u1090 \u1085 \u1086 \u1077  \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1077 ": "pleasant_comm",\
        "\uc0\u55357 \u57014  \u1055 \u1088 \u1086 \u1075 \u1091 \u1083 \u1082 \u1072 ": "walk", "\u55356 \u57283  \u1057 \u1087 \u1086 \u1088 \u1090 ": "sport"\
    \}\
    \
    impact = \{\}\
    for name, field in factors.items():\
        cursor.execute(f'SELECT AVG(mood) FROM mood_log WHERE user_id = ? AND \{field\} = 1', (user_id,))\
        mood_with = cursor.fetchone()[0]\
        cursor.execute(f'SELECT AVG(mood) FROM mood_log WHERE user_id = ? AND \{field\} = 0', (user_id,))\
        mood_without = cursor.fetchone()[0]\
        if mood_with and mood_without:\
            diff = mood_with - mood_without\
            impact[name] = round(diff, 1)\
    \
    worst = sorted(impact.items(), key=lambda x: x[1])[:5]\
    best = sorted(impact.items(), key=lambda x: x[1], reverse=True)[:5]\
    \
    report = "\uc0\u55357 \u56589  *\u1058 \u1042 \u1054 \u1071  \u1043 \u1051 \u1059 \u1041 \u1054 \u1050 \u1040 \u1071  \u1040 \u1053 \u1040 \u1051 \u1048 \u1058 \u1048 \u1050 \u1040 *\\n\\n\u55357 \u56521  *\u1063 \u1090 \u1086  \u1087 \u1086 \u1088 \u1090 \u1080 \u1090  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1085 \u1080 \u1077 :*\\n"\
    for name, diff in worst:\
        if diff < 0:\
            report += f"\'95 \{name\}: \uc0\u8595  \{abs(diff)\} \u1073 \u1072 \u1083 \u1083 \u1072 \\n"\
    report += "\\n\uc0\u55357 \u56520  *\u1063 \u1090 \u1086  \u1091 \u1083 \u1091 \u1095 \u1096 \u1072 \u1077 \u1090  \u1085 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1085 \u1080 \u1077 :*\\n"\
    for name, diff in best:\
        if diff > 0:\
            report += f"\'95 \{name\}: \uc0\u8593  \{diff\} \u1073 \u1072 \u1083 \u1083 \u1072 \\n"\
    await message.answer(report, parse_mode="Markdown")\
\
async def main():\
    scheduler = AsyncIOScheduler()\
    scheduler.start()\
    print("\uc0\u9989  \u1052 \u1053 \u1054 \u1043 \u1054 \u1055 \u1054 \u1051 \u1068 \u1047 \u1054 \u1042 \u1040 \u1058 \u1045 \u1051 \u1068 \u1057 \u1050 \u1048 \u1049  \u1041 \u1054 \u1058  \u1047 \u1040 \u1055 \u1059 \u1065 \u1045 \u1053 !")\
    await dp.start_polling(bot)\
\
if __name__ == "__main__":\
    asyncio.run(main())}