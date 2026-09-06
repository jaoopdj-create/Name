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
    bot.reply_to(message, "👋 नमस्ते! मैं एक ऑल-इन-वन मूवी बोट हूँ।\n\nमुझे किसी भी बॉलीवुड, हॉलीवुड या वेब सीरीज का नाम भेजें (जैसे: Jawan, Avatar Hindi, Stranger Things), मैं आपको डाउनलोड लिंक ढूंढ कर दूँगा।")

@bot.message_handler(func=lambda message: True)
def search_all_movies(message):
    query = message.text
    bot.reply_to(message, f"🔍 '{query}' को इंटरनेट पर ढूंढा जा रहा है, कृपया 5-10 सेकंड का समय दें...")

    # 1337x टॉरेंट साइट को सर्च करने के लिए URL बनाना
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://1337x.to{encoded_query}/1/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # सर्च रिजल्ट्स से पहली 4 मूवीज की डिटेल्स निकालना
        rows = soup.select('table.table-list tbody tr')
        
        if not rows:
            bot.reply_to(message, "❌ माफ़ कीजिये, इस नाम की कोई मूवी या सीरीज नहीं मिली। कृपया सही स्पेलिंग के साथ दोबारा कोशिश करें।")
            return

        response_text = f"🎬 *'{query}' के लिए मिले बेस्ट डाउनलोड लिंक्स:*\n\n"
        
        for row in rows[:4]:
            name_element = row.select_one('td.coll-1 a:nth-of-type(2)')
            seeds = row.select_one('td.coll-2').text if row.select_one('td.coll-2') else "N/A"
            size_element = row.select_one('td.coll-4')
            size = size_element.text if size_element else "N/A"
            
            if name_element:
                movie_title = name_element.text
                movie_href = name_element['href']
                
                # मूवी के अंदर जाकर मैग्नेट लिंक निकालना
                movie_page_url = f"https://1337x.to{movie_href}"
                movie_res = requests.get(movie_page_url, headers=headers, timeout=10)
                movie_soup = BeautifulSoup(movie_res.text, 'html.parser')
                
                magnet_element = movie_soup.select_one('a[href^="magnet:"]')
                if magnet_element:
                    magnet_link = magnet_element['href']
                    
                    # रिस्पॉन्स पैकेज तैयार करना
                    response_text += f"📦 *{movie_title}*\n"
                    response_text += f"⚖️ साइज: {size} | ⚡ स्पीड: {seeds} Seeds\n"
                    response_text += f"🧲 [यहाँ क्लिक करके डाउनलोड करें (Magnet Link)]({magnet_link})\n\n"

        bot.send_message(message.chat.id, response_text, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        bot.reply_to(message, "⚠️ सर्वर पर ज्यादा ट्रैफिक होने के कारण कनेक्शन टूट गया। कृपया एक बार फिर प्रयास करें।")

# बोट पोलिंग शुरू करना
if __name__ == "__main__":
    bot.infinity_polling()
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
    bot.reply_to(message, "👋 नमस्ते! मैं एक ऑल-इन-वन मूवी बोट हूँ।\n\nमुझे किसी भी बॉलीवुड, हॉलीवुड या वेब सीरीज का नाम भेजें (जैसे: Jawan, Avatar Hindi, Stranger Things), मैं आपको डाउनलोड लिंक ढूंढ कर दूँगा।")

@bot.message_handler(func=lambda message: True)
def search_all_movies(message):
    query = message.text
    bot.reply_to(message, f"🔍 '{query}' को ग्लोबल सर्वर पर ढूंढा जा रहा है, कृपया 5-10 सेकंड का समय दें...")

    # 1337x को सर्च करने के लिए एनकोडेड कीवर्ड बनाना
    encoded_query = urllib.parse.quote(query)
    
    # वर्किंग प्रॉक्सी डोमेन का इस्तेमाल ताकि कनेक्शन ब्लॉक न हो
    search_url = f"https://1337x.tw{encoded_query}/1/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        # वेबसाइट से डेटा फेच करना
        res = requests.get(search_url, headers=headers, timeout=12)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # सर्च रिजल्ट्स की रो (Rows) निकालना
        rows = soup.select('table.table-list tbody tr')
        
        if not rows:
            bot.reply_to(message, "❌ माफ़ कीजिये, इस नाम की कोई मूवी या सीरीज नहीं मिली। कृपया सही स्पेलिंग के साथ दोबारा कोशिश करें।")
            return

        response_text = f"🎬 *'{query}' के लिए मिले बेस्ट डाउनलोड लिंक्स:*\n\n"
        
        # टॉप 4 मूवीज के लिंक्स निकालना
        for row in rows[:4]:
            name_element = row.select_one('td.coll-1 a:nth-of-type(2)')
            seeds = row.select_one('td.coll-2').text if row.select_one('td.coll-2') else "N/A"
            size_element = row.select_one('td.coll-4')
            
            # साइज टेक्स्ट को साफ करना
            size = "N/A"
            if size_element:
                # सिर्फ टेक्स्ट पार्ट निकालना (ताकि फालतू टैग्स न आएं)
                size = size_element.get_text(strip=True).split('B')[0] + 'B'

            if name_element:
                movie_title = name_element.text
                movie_href = name_element['href']
                
                # मूवी के स्पेसिफिक पेज से मैग्नेट लिंक निकालना
                movie_page_url = f"https://1337x.tw{movie_href}"
                movie_res = requests.get(movie_page_url, headers=headers, timeout=12)
                movie_soup = BeautifulSoup(movie_res.text, 'html.parser')
                
                magnet_element = movie_soup.select_one('a[href^="magnet:"]')
                if magnet_element:
                    magnet_link = magnet_element['href']
                    
                    # मैसेज में मूवी डिटेल जोड़ना
                    response_text += f"📦 *{movie_title}*\n"
                    response_text += f"⚖️ साइज: {size} | ⚡ स्पीड: {seeds} Seeds\n"
                    response_text += f"🧲 [यहाँ क्लिक करके डाउनलोड करें (Magnet Link)]({magnet_link})\n\n"

        bot.send_message(message.chat.id, response_text, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        print(f"Error Log: {e}")
        bot.reply_to(message, "⚠️ सर्वर से जुड़ने में समस्या आ रही है। कृपया एक बार फिर प्रयास करें या मूवी का नाम बदलें।")

# बोट पोलिंग शुरू करना
if __name__ == "__main__":
    bot.infinity_polling()

