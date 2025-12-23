from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aile Notu</title>
    <style>
        body { font-family: sans-serif; background: #f0f8ff; padding: 20px; }
        .container { max-width: 500px; margin: 30px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        input, textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; }
        button { background: #25D366; color: white; padding: 15px; border: none; border-radius: 8px; width: 100%; font-size: 18px; }
        h2 { text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📩 Aileye Not Gönder</h2>
        <p style="text-align:center; color:#666; font-size:14px;">Bu form sadece ailemiz için.</p>
        <form method="POST">
            <input type="text" name="baslik" placeholder="Kimden? (örneğin: Anne'den)" required>
            <textarea name="mesaj" rows="6" placeholder="Notu yaz..." required></textarea>
            <button type="submit">Gönder → Telegram</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        baslik = request.form['baslik']
        mesaj = request.form['mesaj']
        tam_mesaj = f"<b>{baslik}</b>\n\n{mesaj}"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        veri = {'chat_id': CHAT_ID, 'text': tam_mesaj, 'parse_mode': 'HTML'}
        
        try:
            response = requests.post(url, data=veri)
            if response.ok:
                return '<h3 style="text-align:center;color:green;">✅ Gönderildi!</h3><br><a href="/">← Yeni not</a>'
            else:
                return '<h3 style="text-align:center;color:red;">❌ Gönderim hatası</h3>'
        except:
            return '<h3 style="text-align:center;color:red;">❌ Bağlantı hatası</h3>'
    
    return render_template_string(HTML)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)