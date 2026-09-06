        import os
import telebot
import requests
import urllib.parse

# Render के Environment Variables से बोट टोकन लेना
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 नमस्ते! मैं आपका ऑल-इन-वन एडवांस मूवी बोट हूँ।\n\nमुझे किसी भी बॉलीवुड, हॉलीवुड या वेब सीरीज का नाम भेजें (जैसे: *Jawan*, *Inception*, *Mirzapur*), मैं आपको डायरेक्ट सुपरफास्ट डाउनलोड लिंक ढूँढ कर दूँगा।")

@bot.message_handler(func=lambda message: True)
def search_all_movies_unblocked(message):
    query = message.text
    bot.reply_to(message, f"🔍 '{query}' को अनब्लॉक्ड ग्लोबल सर्वर पर ढूँढा जा रहा है, कृपया 3-5 सेकंड का समय दें...")

    # Torrentio API का इस्तेमाल (यह रेंडर पर 100% वर्किंग है और कभी ब्लॉक नहीं होता)
    encoded_query = urllib.parse.quote(query.lower())
    api_url = f"https://strem.fun|sort=seeders/search?query={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=12).json()
        
        # चेक करना कि स्ट्रीम लिंक्स मिले या नहीं
        if "streams" in response and len(response["streams"]) > 0:
            streams = response["streams"]
            
            response_text = f"🎬 *'{query}' के लिए मिले बेस्ट डाउनलोड लिंक्स:*\n\n"
            
            # टॉप 5 बेस्ट रिजल्ट्स (हाई स्पीड वाले) यूजर को दिखाने के लिए
            for stream in streams[:5]:
                title_details = stream.get("title", "Unknown Movie")
                
                # मैग्नेट लिंक निकालना
                magnet_link = stream.get("infoHash")
                if magnet_link:
                    # फुल मैग्नेट यूआरएल बनाना
                    full_magnet = f"magnet:?xt=urn:btih:{magnet_link}&dn={encoded_query}"
                    
                    # टेक्स्ट को साफ़-सुथरा फ़ॉर्मेट करना
                    # Torrentio के टाइटल में साइज और क्वालिटी पहले से होती है
                    clean_title = title_details.replace("\n", " | ")
                    
                    response_text += f"📦 *{clean_title}*\n"
                    response_text += f"🧲 [यहाँ क्लिक करके डाउनलोड करें (Magnet Link)]({full_magnet})\n\n"
            
            bot.send_message(message.chat.id, response_text, parse_mode="Markdown", disable_web_page_preview=True)
            
        else:
            bot.reply_to(message, "❌ माफ़ कीजिये, इस नाम की कोई मूवी या वेब सीरीज नहीं मिली। कृपया स्पेलिंग चेक करके दोबारा कोशिश करें।")
            
    except Exception as e:
        print(f"API Error Log: {e}")
        bot.reply_to(message, "⚠️ सर्वर कनेक्टिविटी में कुछ समस्या है। कृपया एक बार फिर प्रयास करें।")

if __name__ == "__main__":
    bot.infinity_polling()
    
