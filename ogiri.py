from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI
import os

from dotenv import load_dotenv
# .envファイルの内容を読み込む
load_dotenv()
# 環境変数からAPIキーを取得
api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
client = OpenAI(api_key=api_key) # OpenAIクライアントの初期化


HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>大喜利アプリ</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: #f0f0f5;

                /* === 最背面背景画像追加（修正済）=== */
            background-image: url('/static/2.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed; /* 追加でしっかり固定表示 */

            background-color: #f0f0f5; /* 万が一画像が読めない場合の下地 */
        }

        }

        header {
            text-align: center;
            padding-top: 30px;
        }

        h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }

        .input-box {
            display: inline-flex;
            margin-bottom: 30px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            background: white;
            padding: 10px;
            border-radius: 6px;
        }

        #prompt {
            padding: 10px;
            width: 300px;
            font-size: 16px;
            border: 2px solid #333;
            border-radius: 5px 0 0 5px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 0 5px 5px 0;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }

        .main {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 40px;
            padding: 20px;
        }

        .person-img {
            width: 200px;
            height: auto;
        }

        .speech-container {
            position: relative;
            width: 600px;
            height: 300px;
            background-image: none;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: none;
            justify-content: center;
            align-items: center;
        }

        .speech-container.show {
            display: flex;
            background-image: url('/static/shuchusen.png');
        }

        .speech-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            font-weight: bold;
            color: #000;
            max-width: 60%;
            max-height: 40%;
            text-align: center;
            word-break: break-word;
            white-space: pre-wrap;
            line-height: 1.5;
            padding: 10px;
        }
    </style>
</head>
<body>

    <header>
        <h1>大喜利アプリ</h1>
        <div class="input-box">
            <input type="text" id="prompt" placeholder="お題を入力">
            <button onclick="submitPrompt()">出題</button>
            <button onclick="toggleRecording()">🎤 録音</button>
        </div>
    </header>

    <div class="main">
        <img src="/static/raw.png" class="person-img">
        <div class="speech-container" id="speechContainer">
            <div class="speech-text" id="response"></div>
        </div>
    </div>

    <audio id="audio" controls></audio>

    <script>
    let recognition;
    let isRecording = false;

    function toggleRecording() {
        if (!isRecording) {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'ja-JP';
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('prompt').value = transcript;
                submitPrompt(transcript);
            };
            recognition.start();
            isRecording = true;
        } else {
            recognition.stop();
            isRecording = false;
        }
    }

    function submitPrompt(prompt=null) {
        if (!prompt) {
            prompt = document.getElementById('prompt').value;
        }
        if (!prompt) return;

        fetch('/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: prompt})
        })
        .then(response => response.json())
        .then(data => {
            const responseDiv = document.getElementById('response');
            const speechContainer = document.getElementById('speechContainer');

            responseDiv.innerText = data.reply;

            const length = data.reply.length;
            responseDiv.style.fontSize = "24px";
            if (length > 60) {
                responseDiv.style.fontSize = "18px";
            } else if (length > 30) {
                responseDiv.style.fontSize = "20px";
            }

            speechContainer.classList.add("show");

            document.getElementById('audio').src = data.audio_url + '?t=' + new Date().getTime();
            document.getElementById('audio').play();
        });
    }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data['prompt']

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは大喜利のプロの芸人です。ユーモア、ひねり、意外性を持った短い回答を一つだけ出してください。"},
            {"role": "user", "content": f"お題: {prompt}\n一言でオチがつく面白い答えを一つだけ考えてください。"}
        ]
    )

    reply = response.choices[0].message.content.strip()

    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=reply
    )

    audio_path = os.path.join('static', 'speech.mp3')
    with open(audio_path, 'wb') as f:
        for chunk in speech_response.iter_bytes():
            f.write(chunk)

    return jsonify({'reply': reply, 'audio_url': '/static/speech.mp3'})

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
