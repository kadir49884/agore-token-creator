from flask import Flask, request, jsonify
from flask_cors import CORS
from agora_token_builder import RtcTokenBuilder
import os
import time
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)
CORS(app)

# Agora kimlik bilgileri
APP_ID = os.getenv('AGORA_APP_ID')
APP_CERTIFICATE = os.getenv('AGORA_APP_CERTIFICATE')

# Token geçerlilik süresi (1 saat)
TOKEN_EXPIRY_TIME = 3600

@app.route('/')
def home():
    return jsonify({
        'status': 'active',
        'message': 'Video Chat Token Server is running'
    })

@app.route('/token')
def generate_token():
    try:
        # URL parametrelerini al
        channel_name = request.args.get('channel')
        uid = request.args.get('uid', '0')
        
        if not channel_name:
            return jsonify({'error': 'Channel name is required'}), 400
            
        if not APP_ID or not APP_CERTIFICATE:
            return jsonify({'error': 'Agora credentials not configured'}), 500
        
        # String uid'yi int'e çevir
        uid = int(uid)
        
        # Şu anki timestamp
        current_timestamp = int(time.time())
        
        # Token oluştur
        token = RtcTokenBuilder.buildTokenWithUid(
            appId=APP_ID,
            appCertificate=APP_CERTIFICATE,
            channelName=channel_name,
            uid=uid,
            role=1, # Publisher rolü
            privilegeExpiredTs=current_timestamp + TOKEN_EXPIRY_TIME
        )
        
        return jsonify({
            'token': token,
            'expires_in': TOKEN_EXPIRY_TIME
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 