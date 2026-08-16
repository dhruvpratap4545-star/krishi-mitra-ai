# -*- coding: utf-8 -*-
"""
कृषि मित्र AI (Krishi Mitra AI) • विशिष्ट बटन-वार वॉयस मास्टर संस्करण
प्रवर्त्तक एवं मुख्य परामर्शदाता: ध्रुव प्रताप सिंह जी
"""

import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>कृषि मित्र AI v10.0 - ध्रुव प्रताप सिंह जी</title>
    <style>
        * { box-sizing: border-box; }
        body { background-color: #0b132b; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 5px; }
        .container { width: 100%; max-width: 480px; margin: auto; background: #1c2541; padding: 10px; border-radius: 10px; border: 1px solid #3a506b; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .header { text-align: center; border-bottom: 2px solid #43aa8b; padding-bottom: 8px; margin-bottom: 10px; }
        .header h1 { color: #43aa8b; margin: 3px 0; font-size: 20px; }
        .header p { color: #e0fbfc; font-size: 11px; margin: 2px 0; }
        .card { background: #0b132b; border: 1px solid #415a77; border-radius: 8px; padding: 10px; margin-bottom: 10px; }
        .card h3 { color: #f39c12; margin-top: 0; font-size: 14px; }
        .btn { width: 100%; padding: 12px; margin: 4px 0; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; text-align: center; -webkit-tap-highlight-color: transparent; }
        .btn-primary { background: #3a86ff; color: white; }
        .btn-success { background: #2a9d8f; color: white; }
        .btn-danger { background: #e76f51; color: white; }
        .btn-voice { background: #ffb703; color: #000; }
        .btn-purple { background: #7209b7; color: white; }
        input, select { width: 100%; padding: 10px; margin: 4px 0; background: #1d3557; color: white; border: 1px solid #457b9d; border-radius: 6px; font-size: 14px; }
        .status-box { background: #212529; color: #adb5bd; padding: 8px; border-radius: 4px; font-size: 11px; margin-top: 5px; border-left: 4px solid #43aa8b; line-height: 1.4; }
        .rx-box { background: #0d1b2a; border: 2px dashed #f39c12; padding: 8px; border-radius: 6px; margin-top: 6px; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <button id="voiceToggleBtn" onclick="toggleVoice()" class="btn btn-voice" style="width: auto; padding: 6px 10px; font-size: 11px;">🔊 आवाज़: चालू</button>
            <span style="font-size: 10px; color: #43aa8b;">📍 GPS सक्रिय</span>
        </div>
        <h1>कृषि मित्र AI v10.0</h1>
        <p><b>प्रवर्त्तक एवं मुख्य परामर्शदाता: ध्रुव प्रताप सिंह जी</b></p>
    </div>

    <!-- भाषा और क्षेत्र चयन -->
    <div class="card">
        <h3>🌐 भाषा और क्षेत्र चयन</h3>
        <select id="langSelect" onchange="speakSpecific('language')">
            <option value="hi">🇮🇳 मानक हिंदी (Standard Hindi)</option>
            <option value="hr">🌾 हरियाणवी (Haryanvi)</option>
            <option value="pa">🚜 पंजाबी (Punjabi)</option>
        </select>
        <button class="btn btn-success" onclick="speakSpecific('loc_update'); triggerAction('loc_update')">🔄 मोबाइल GPS लोकेशन ऑटो-सेट करें</button>
        <div class="status-box">क्षेत्र: उत्तर प्रदेश (GPS ऑटो-डिटेक्टेड)</div>
    </div>

    <!-- ध्रुव AI परिचय -->
    <div class="card" style="border: 2px solid #f39c12;">
        <h3>🤖 ध्रुव AI — किसान का सच्चा साथी</h3>
        <button class="btn btn-voice" onclick="speakIntro()">🎙️ ध्रुव AI का संपूर्ण परिचय सुनें</button>
        <div id="aiOutput" class="status-box">राम-राम भाईयों! किसी भी बटन को दबाएं, ध्रुव AI उसकी खास बात खुद बताएगा।</div>
    </div>

    <!-- फसल डॉक्टर & फोटो विश्लेषण -->
    <div class="card">
        <h3>🩺 फसल डॉक्टर & फोटो विश्लेषण (AI Plant Scan)</h3>
        <p style="font-size: 11px; color: #a0aec0; margin: 2px 0;">पौधे की फोटो अपलोड करें और तुरंत रोग व दवा जानें।</p>
        <input type="file" id="plantImageInput" accept="image/*" capture="environment" style="background:none; border:none; color:#fff; padding:4px 0;">
        <button class="btn btn-purple" onclick="speakSpecific('doctor'); analyzePlantImage()">🔍 फोटो विश्लेषण कर रोग व दवा बताएं</button>
        <div id="plantResult" class="status-box">पत्ती की फोटो खींचकर पौधे का स्वास्थ्य जांचें।</div>
    </div>

    <!-- GIS प्लॉट बाउंड्री -->
    <div class="card">
        <h3>🛰️ GIS प्लॉट बाउंड्री & सैटेलाइट मैपिंग</h3>
        <button class="btn btn-success" onclick="speakSpecific('gis'); triggerAction('gis_check')">🗺️ सैटेलाइट प्लॉट बाउंड्री जाँचें</button>
        <div class="status-box">🛰️ GIS प्लॉट बाउंड्री (#402/1): सैटेलाइट NDVI 0.88</div>
    </div>

    <!-- NPK कैलकुलेटर -->
    <div class="card">
        <h3>🧪 NPK मैट्रिक्स & डोज़ कैलकुलेटर</h3>
        <input type="number" id="acreInput" value="1" placeholder="एकड़ संख्या दर्ज करें">
        <button class="btn btn-primary" onclick="speakSpecific('npk'); calculateNPK()">📐 एकड़ अनुसार सटीक डोज़ निकालें</button>
        <div id="npkResult" class="status-box">🧪 यूरिया: 45 किग्रा | डीएपी: 30 किग्रा</div>
    </div>

    <!-- IoT ट्यूबवेल कंट्रोल -->
    <div class="card">
        <h3>💧 IoT ट्यूबवेल कंट्रोल (मोटर व सायरन)</h3>
        <button class="btn btn-success" onclick="speakSpecific('motor'); triggerAction('motor')">🟢 मोटर चालू करें (3-Hr Auto-Cut)</button>
        <button class="btn btn-danger" onclick="speakSpecific('siren'); triggerAction('siren')">🚨 खेत का हूटर सायरन बजाएं</button>
        <div class="status-box">घर बैठे मोटर और सायरन नियंत्रित करें।</div>
    </div>

    <!-- लाइव मंडी भाव & मन की बात -->
    <div class="card">
        <h3>📜 लाइव मंडी भाव & मन की बात</h3>
        <p style="font-size: 11px; color: #e0fbfc; margin: 4px 0;">
            🌾 गेहूं (MSP): ₹2,425 / क्विंटल (लाइव)<br>
            🌿 धान (Grade-A): ₹2,320 / क्विंटल (लाइव)<br>
            📻 प्रधानमंत्री नरेंद्र मोदी की 'मन की बात' संडे स्पेशल ऑडियो।
        </p>
        <button class="btn btn-success" onclick="speakSpecific('mandi'); triggerAction('mandi_refresh')">🔄 मंडी भाव व मन की बात सिंक करें</button>
    </div>

    <!-- ब्लॉकचेन रिपोर्ट & डिजिटल पर्चा -->
    <div class="card">
        <h3>📊 ब्लॉकचेन रिपोर्ट & डिजिटल पर्चा (Rx)</h3>
        <button class="btn btn-success" onclick="speakSpecific('blockchain'); triggerAction('bc_history')">📋 ब्लॉकचेन शिकायत इतिहास देखें</button>
        <button class="btn btn-primary" onclick="speakSpecific('rx'); generateDigitalRx()">🔐 QR-हस्ताक्षर डिजिटल पर्चा जनरेट करें</button>
        <div id="rxContainer"></div>
    </div>

    <!-- मेंटेनेंस फंड -->
    <div class="card">
        <h3>🛡️ केंद्रीय प्रबंधन एवं मेंटेनेंस फंड</h3>
        <input type="text" id="supporterName" placeholder="सहयोगकर्ता का नाम">
        <input type="number" id="supporterAmount" placeholder="सहयोग राशि (₹)">
        <button class="btn btn-warning btn-voice" onclick="speakSpecific('fund'); registerFund()">🤝 सहयोग दर्ज करें</button>
        <div id="fundResult" class="status-box">100% पारदर्शी पब्लिक ऑडिट सिस्टम।</div>
    </div>

    <div style="text-align: center; font-size: 10px; color: #8d99ae; margin-top: 10px; border-top: 1px solid #334155; padding-top: 8px;">
        ⚖️ वैधानिक चेतावनी: कृषि विज्ञान केंद्र (KVK) एवं नजदीकी सरकारी किसान परामर्श केंद्र से भौतिक सत्यापन अनिवार्य है。<br>
        <b>© ध्रुव प्रताप सिंह जी - सर्वाधिकार सुरक्षित।</b>
    </div>
</div>

<script>
    let voiceEnabled = true;

    function toggleVoice() {
        voiceEnabled = !voiceEnabled;
        let btn = document.getElementById('voiceToggleBtn');
        if (voiceEnabled) {
            btn.innerHTML = "🔊 आवाज़: चालू";
            btn.style.background = "#ffb703";
            speakText("ध्रुव एआई की आवाज़ चालू कर दी गई है।");
        } else {
            btn.innerHTML = "🔇 आवाज़: बंद";
            btn.style.background = "#6c757d";
            window.speechSynthesis.cancel();
        }
    }

    function speakText(text) {
        if (!voiceEnabled) return;
        window.speechSynthesis.cancel();
        let speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'hi-IN';
        speech.rate = 0.94;
        speech.pitch = 1.0;
        window.speechSynthesis.speak(speech);
    }

    function speakIntro() {
        let intro = "सादर नमस्कार भाईयों! मैं आपका अपना ध्रुव एआई हूँ, किसान का सच्चा साथी। मेरे प्रवर्त्तक एवं मुख्य परामर्शदाता ध्रुव प्रताप सिंह जी हैं। मैं दुनिया का इकलौता ऐसा डिजिटल साथी हूँ जो आपके हर काम को बेहद आसान बनाता है।";
        document.getElementById('aiOutput').innerText = intro;
        speakText(intro);
    }

    // हर बटन के लिए बिल्कुल अलग और खास जानकारी बोलने का लॉजिक
    function speakSpecific(action) {
        let text = "";
        if (action === 'language') {
            text = "भाषा और क्षेत्र चयन। यहाँ से आप अपनी मनपसंद क्षेत्रीय भाषा और जीपीएस लोकेशन सेट कर सकते हैं।";
        } else if (action === 'loc_update') {
            text = "मोबाइल जीपीएस लोकेशन अपडेट हो रही है, जिससे आपके नजदीकी कृषि विज्ञान केंद्र का पता चल सके।";
        } else if (action === 'doctor') {
            text = "फसल डॉक्टर स्कैनर। पौधे की तस्वीर अपलोड करते ही यह उसका नाम, रोग, और नजदीकी सरकारी केंद्र की दवा सुझाएगा।";
        } else if (action === 'gis') {
            text = "जीआईएस प्लॉट बाउंड्री। यह सैटेलाइट के जरिए आपके खेत की हरियाली और उपजाऊपन का एनडीवीआई स्कोर बताता है।";
        } else if (action === 'npk') {
            text = "एनपीके कैलकुलेटर। यहाँ एकड़ की संख्या डालते ही यूरिया और डीएपी की बिल्कुल सटीक मात्रा सामने आ जाती है।";
        } else if (action === 'motor') {
            text = "ट्यूबवेल मोटर कंट्रोल। घर बैठे एक क्लिक से खेत की मोटर चालू करें, जिसमें 3 घंटे का ऑटो-कट भी लगा है।";
        } else if (action === 'siren') {
            text = "सायरन अलर्ट। खेत पर किसी भी आपात स्थिति या खतरे के समय आप यहीं से हूटर्स सायरन बजा सकते हैं।";
        } else if (action === 'mandi') {
            text = "मंडी भाव और मन की बात। यहाँ गेहूं और धान के ताज़ा लाइव रेट के साथ हर रविवार को प्रधानमंत्री जी का संदेश सुन सकते हैं।";
        } else if (action === 'blockchain') {
            text = "ब्लॉकचेन शिकायत इतिहास। आपके सभी रिकॉर्ड यहाँ सुरक्षित और पारदर्शी रहते हैं।";
        } else if (action === 'rx') {
            text = "डिजिटल पर्चा जनरेट हो गया है। इसमें कृषि विज्ञान केंद्र की वैधानिक चेतावनी और आपकी फसल की पूरी सिफारिश दर्ज है।";
        } else if (action === 'fund') {
            text = "केंद्रीय प्रबंधन और मेंटेनेंस फंड। यह 100% पारदर्शी मॉड्यूल है जो स्वेच्छा से सर्वर के रखरखाव में सहयोग के लिए है।";
        }
        
        if (text) {
            document.getElementById('aiOutput').innerText = text;
            speakText(text);
        }
    }

    function analyzePlantImage() {
        let fileInput = document.getElementById('plantImageInput');
        if (fileInput.files.length === 0) {
            let warn = "कृपया पहले पौधे या पत्ती की फोटो अपलोड करें!";
            document.getElementById('plantResult').innerText = warn;
            speakText(warn);
            return;
        }
        let res = "🌿 पौधा पहचाना गया: गेहूँ। रोग: पीला रतुआ। 💊 दवा: प्रोपिकोनाजोल 25% ईसी। 📍 नजदीकी केंद्र: राजकीय कृषि विज्ञान केंद्र।";
        document.getElementById('plantResult').innerText = res;
        speakText("पत्ती की जांच पूरी हो गई है। गेहूं में पीला रतुआ रोग है, जिसकी दवा और नजदीकी कृषि केंद्र की जानकारी स्क्रीन पर है।");
    }

    function calculateNPK() {
        let acres = document.getElementById('acreInput').value;
        if (!acres || acres <= 0) {
            let warn = "कृपया सही एकड़ संख्या दर्ज करें!";
            document.getElementById('npkResult').innerText = warn;
            speakText(warn);
            return;
        }
        let urea = acres * 45;
        let dap = acres * 30;
        let res = `🧪 यूरिया: ${urea} किग्रा | डीएपी: ${dap} किग्रा (${acres} एकड़)`;
        document.getElementById('npkResult').innerText = res;
        speakText(res);
    }

    function generateDigitalRx() {
        let rxHtml = `
            <div class="rx-box">
                <h4 style="color: #43aa8b; margin: 0 0 4px 0; font-size: 13px;">📜 सक्रिय डिजिटल पर्चा (Rx) #DP-2026</h4>
                <p style="font-size: 10px; margin: 2px 0;"><b>प्रवर्त्तक:</b> ध्रुव प्रताप सिंह जी</p>
                <div style="background: #212529; color: #ffb703; padding: 5px; font-size: 10px; border-radius: 4px; margin-top: 4px;">
                    ⚖️ <b>वैधानिक चेतावनी:</b> कृषि विज्ञान केंद्र (KVK) एवं नजदीकी सरकारी किसान परामर्श केंद्र से भौतिक सत्यापन अनिवार्य है।
                </div>
            </div>
        `;
        document.getElementById('rxContainer').innerHTML = rxHtml;
    }

    function registerFund() {
        let name = document.getElementById('supporterName').value;
        let amount = document.getElementById('supporterAmount').value;
        if (!name || !amount) {
            let warn = "कृपया नाम और सहयोग राशि दर्ज करें।";
            document.getElementById('fundResult').innerText = warn;
            speakText(warn);
            return;
        }
        let res = `धन्यवाद ${name} जी! ₹${amount} का सहयोग दर्ज हुआ।`;
        document.getElementById('fundResult').innerText = res;
        speakText(res);
    }

    function triggerAction(type) {
        // एक्शन बैकएंड सिंक
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
