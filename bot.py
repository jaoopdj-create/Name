import os
import telebot
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Render के Environment Variables से बोट टोकन लेना
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 नमस्ते! मैं आपका ऑल-इन-वन एडवांस मूवी बोट हूँ।\n\nमुझे किसी भी बॉलीवुड, हॉलीवुड या वेब सीरीज का नाम भेजें (जैसे: *Jawan*, *Inception*), मैं आपको तुरंत वर्किंग डाउनलोड लिंक्स ढूँढ कर दूँगा।")

@bot.message_handler(func=lambda message: True)
def search_movies_fast(message):
    query = message.text
    bot.reply_to(message, f"🔍 '{query}' को फ़ास्ट सर्वर पर ढूँढा जा रहा है, कृपया 3-5 सेकंड का समय दें...")

    # मूवी सर्च करने के लिए एक बिल्कुल नया और चालू अनब्लॉक्ड प्रॉक्सी URL
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://apibay.org{encoded_query}"

    try:
        # सीधे JSON API से डेटा निकालना (यह कभी ब्लॉक नहीं होता)
        response = requests.get(search_url, timeout=10).json()
        
        # अगर कोई मूवी नहीं मिली
        if not response or response[0]['id'] == '0':
            bot.reply_to(message, "❌ माफ़ कीजिये, इस नाम की कोई मूवी या वेब सीरीज नहीं मिली। कृपया सही स्पेलिंग के साथ दोबारा कोशिश करें।")
            return

        response_text = f"🎬 *'{query}' के लिए मिले बेस्ट डाउनलोड लिंक्स:*\n\n"
        
        # टॉप 4 सबसे बेस्ट रिपॉन्स दिखाना
        for item in response[:4]:
            title = item.get('name', 'Unknown Movie')
            size_bytes = int(item.get('size', 0))
            seeds = item.get('seeders', '0')
            info_hash = item.get('info_hash')
            
            # साइज को GB या MB में बदलना
            if size_bytes > 0:
                size = f"{round(size_bytes / (1024 * 1024 * 1024), 2)} GB" if size_bytes > 1024*1024*1024 else f"{round(size_bytes / (1024 * 1024), 2)} MB"
            else:
                size = "N/A"
                
            if info_hash:
                # मैग्नेट लिंक तैयार करना
                magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(title)}"
                
                response_text += f"📦 *{title}*\n"
                response_text += f"⚖️ साइज: {size} | ⚡ स्पीड: {seeds} Seeds\n"
                response_text += f"🧲 [यहाँ क्लिक करके डाउनलोड करें (Magnet Link)]({magnet_link})\n\n"

        bot.send_message(message.chat.id, response_text, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        print(f"Error Log: {e}")
        bot.reply_to(message, "⚠️ सर्वर अभी व्यस्त है। कृपया एक बार फिर प्रयास करें या किसी दूसरी मूवी का नाम लिखें।")

if __name__ == "__main__":
    bot.infinity_polling()
                
