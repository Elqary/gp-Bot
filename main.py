import telebot
from datetime import datetime
import hijri_converter as hc
import pytz
import schedule
import time
from bs4 import BeautifulSoup
import requests
import random

api_token = '6501737126:AAHY6RF31BYOUj5PRzhSETB7r8YTTkzinVo'
bot = telebot.TeleBot(api_token)

def get_random_dua():
    url = "https://kalemtayeb.com/adeiah/section/16"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    dua_elements = soup.find_all("div", class_="item_nass")
    if dua_elements:
        random_dua = random.choice(dua_elements)
        dua_text = random_dua.text.strip()
        # Replace * with ۞
        dua_text = dua_text.replace('*', '۞')
        # Remove "
        dua_text = dua_text.replace('"', '')
        return dua_text
    else:
        return "لا يمكن العثور على الدعاء"

def get_current_time():
    tz = pytz.timezone('Africa/Cairo')
    now = datetime.now(tz)
    hijri_date = hc.Gregorian(now.year, now.month, now.day).to_hijri()
    return now, hijri_date, tz

def arabic_am_pm(time_str):
    if 'AM' in time_str:
        return time_str.replace('AM', 'ص')
    elif 'PM' in time_str:
        return time_str.replace('PM', 'م')
    else:
        return time_str

def arabic_numerals(text):
    arabic_digits = {
        '0': '٠',
        '1': '١',
        '2': '٢',
        '3': '٣',
        '4': '٤',
        '5': '٥',
        '6': '٦',
        '7': '٧',
        '8': '٨',
        '9': '٩'
    }
    for eng, arabic in arabic_digits.items():
        text = text.replace(eng, arabic)
    return text

def update_group_info():
    chat_id = '-1002392074660'
    now, hijri_date, tz = get_current_time()
    current_time = now.strftime("%I:%M %p")
    current_time_arabic = arabic_am_pm(current_time)
    gregorian_date = now.strftime("%Y/%m/%d")
    gregorian_date_arabic = arabic_numerals(gregorian_date)
    
    # تاريخ 15/6
    target_date = datetime(now.year, 6, 15, tzinfo=tz)
    
    # عدد الأيام المتبقية
    remaining_days = (target_date - now).days
    
    # إعداد اسم المجموعة بناءً على الأيام المتبقية
    group_name = f"باقي {remaining_days} يوم على النهاية | طلاب ثانوية دفعه2024🙂❤️"
    
    arabic_month_names = {
        1: 'يناير',
        2: 'فبراير',
        3: 'مارس',
        4: 'أبريل',
        5: 'مايو',
        6: 'يونيو',
        7: 'يوليو',
        8: 'أغسطس',
        9: 'سبتمبر',
        10: 'أكتوبر',
        11: 'نوفمبر',
        12: 'ديسمبر'
    }
    month_arabic = arabic_month_names[now.month]
    day_name = now.strftime("%A")
    
    arabic_day_names = {
        'Monday': 'الاثنين',
        'Tuesday': 'الثلاثاء',
        'Wednesday': 'الأربعاء',
        'Thursday': 'الخميس',
        'Friday': 'الجمعة',
        'Saturday': 'السبت',
        'Sunday': 'الأحد'
    }
    
    new_group_name = f"المجموعة في {current_time_arabic}"
    
    dua = get_random_dua()
    new_about = f"«{dua}»\n" \
                "────────────────\n" \
                f"🕰╽الساعة الان بتوقيت مصر⇜ {current_time_arabic} ؛\n" \
                f"🌏╽التاريخ ⇜ {gregorian_date} ؛\n" \
                f"🌈╽اليوم⇜ {arabic_day_names[day_name]} ؛"
    
    # تحديث اسم المجموعة والوصف
    #bot.set_chat_title(chat_id, group_name)
    bot.set_chat_description(chat_id, new_about)

# استدعاء الدالة للتأكد من تحديث المعلومات في البداية
update_group_info()

# جدولة تحديث المعلومات بانتظام
schedule.every().minute.do(update_group_info)
print("running ......")
while True:
    schedule.run_pending()
    time.sleep(1)
