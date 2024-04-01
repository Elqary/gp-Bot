<?php

// Include the Telegram bot API library
require 'vendor/autoload.php';

// Import classes from the Telegram bot API library
use Telegram\Bot\Api;
use Carbon\Carbon;
use Sunra\PhpSimple\HtmlDomParser;

// Set up the Telegram bot API
$api_token = 'YOUR_TELEGRAM_API_TOKEN';
$bot = new Api($api_token);

// Function to fetch a random dua
function get_random_dua() {
    $url = "https://kalemtayeb.com/adeiah/section/16";
    $response = file_get_contents($url);
    $html = HtmlDomParser::str_get_html($response);
    $dua_elements = $html->find('div.item_nass');
    if ($dua_elements) {
        $random_index = array_rand($dua_elements);
        $random_dua = $dua_elements[$random_index]->plaintext;
        // Replace * with ۞
        $random_dua = str_replace('*', '۞', $random_dua);
        // Remove "
        $random_dua = str_replace('"', '', $random_dua);
        return $random_dua;
    } else {
        return "لا يمكن العثور على الدعاء";
    }
}

// Function to get current time
function get_current_time() {
    $now = Carbon::now('Africa/Cairo');
    $hijri_date = hijri_converter::gregorianToHijri($now->year, $now->month, $now->day);
    return [$now, $hijri_date];
}

// Function to update group information
function update_group_info() {
    $chat_id = 'YOUR_CHAT_ID';
    list($now, $hijri_date) = get_current_time();
    $current_time = $now->format('h:i A');
    $current_time_arabic = arabic_am_pm($current_time);
    $gregorian_date = $now->format('Y/m/d');
    $gregorian_date_arabic = arabic_numerals($gregorian_date);
    
    // تاريخ 15/6
    $target_date = Carbon::create($now->year, 6, 15, 0, 0, 0, 'Africa/Cairo');
    
    // عدد الأيام المتبقية
    $remaining_days = $target_date->diffInDays($now);
    
    // إعداد اسم المجموعة بناءً على الأيام المتبقية
    $group_name = "باقي $remaining_days على النهاية";
    
    $arabic_day_names = [
        'Monday' => 'الاثنين',
        'Tuesday' => 'الثلاثاء',
        'Wednesday' => 'الأربعاء',
        'Thursday' => 'الخميس',
        'Friday' => 'الجمعة',
        'Saturday' => 'السبت',
        'Sunday' => 'الأحد'
    ];
    
    $new_group_name = "المجموعة في $current_time_arabic";
    
    $dua = get_random_dua();
    $new_about = "«$dua»\n" .
                 "────────────────\n" .
                 "🕰╽الساعة الان بتوقيت مصر⇜ $current_time_arabic ؛\n" .
                 "🌏╽التاريخ ⇜ $gregorian_date ؛\n" .
                 "🌈╽اليوم⇜ " . $arabic_day_names[$now->format('l')] . " ؛";
    
    // تحديث اسم المجموعة والوصف
    $bot->setChatTitle(['chat_id' => $chat_id, 'title' => $group_name]);
    $bot->setChatDescription(['chat_id' => $chat_id, 'description' => $new_about]);
}

// استدعاء الدالة للتأكد من تحديث المعلومات في البداية
update_group_info();

// تحديث المعلومات بانتظام
while (true) {
    update_group_info();
    sleep(60);
}
?>
