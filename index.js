const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const { HijriDate } = require('hijri-converter');

// تهيئة بوت التيليغرام
const token = '6501737126:AAHY6RF31BYOUj5PRzhSETB7r8YTTkzinVo';
const bot = new TelegramBot(token, { polling: true });

// دالة لجلب دعاء عشوائي
async function get_random_dua() {
    const url = "https://kalemtayeb.com/adeiah/section/16";
    try {
        const response = await axios.get(url);
        const dua_elements = response.data.match(/<div class="item_nass">(.*?)<\/div>/gs);
        if (dua_elements && dua_elements.length > 0) {
            const random_index = Math.floor(Math.random() * dua_elements.length);
            let random_dua = dua_elements[random_index].replace(/<\/?[^>]+(>|$)/g, "");
            random_dua = random_dua.replace('*', '۞');
            return random_dua;
        } else {
            return "لا يمكن العثور على الدعاء";
        }
    } catch (error) {
        console.error("Error fetching random dua:", error);
        return "لا يمكن العثور على الدعاء";
    }
}

// دالة لتحديث معلومات المجموعة
async function update_group_info() {
    const chat_id = '-4136537724';
    const now = new Date();
    const hijri_date = new HijriDate(now);
    const current_time = now.toLocaleTimeString('en-US', { hour12: true });
    const gregorian_date = now.toISOString().split('T')[0];
    
    // تاريخ 15/6
    const target_date = new Date(now.getFullYear(), 5, 15);
    
    // عدد الأيام المتبقية
    const remaining_days = Math.ceil((target_date - now) / (1000 * 60 * 60 * 24));
    
    // إعداد اسم المجموعة بناءً على الأيام المتبقية
    const group_name = `باقي ${remaining_days} على النهاية`;
    
    const arabic_day_names = {
        0: 'الأحد',
        1: 'الاثنين',
        2: 'الثلاثاء',
        3: 'الأربعاء',
        4: 'الخميس',
        5: 'الجمعة',
        6: 'السبت'
    };
    
    const new_group_name = `المجموعة في ${current_time}`;
    
    const dua = await get_random_dua();
    const new_about = `«${dua}»\n────────────────\n🕰╽الساعة الان بتوقيت مصر⇜ ${current_time} ؛\n🌏╽التاريخ ⇜ ${gregorian_date} ؛\n🌈╽اليوم⇜ ${arabic_day_names[now.getDay()]} ؛`;
    
    // تحديث اسم المجموعة والوصف
    try {
        await bot.setChatTitle(chat_id, group_name);
        await bot.setChatDescription(chat_id, new_about);
    } catch (error) {
        console.error("Error updating group info:", error);
    }
}

// استدعاء الدالة للتأكد من تحديث المعلومات في البداية
update_group_info();

// تحديث المعلومات بانتظام
setInterval(update_group_info, 60000);
