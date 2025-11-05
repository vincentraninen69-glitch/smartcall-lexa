# smartcall-lexa
Svensk AI-röstassistent – Lexa från Smart Call. Demo för röstbaserad AI med GPT och ElevenLabs.
# 🎙️ Smart Call — Lexa AI Voice Demo 🇸🇪

**Lexa** är en svensk AI-röstagent skapad av **Smart Call**, designad för att demonstrera hur företag kan automatisera kundsamtal med hjälp av AI.

Den här demon använder:
- 🧠 **OpenAI GPT-5** — hjärnan (konversation och förståelse)
- 🎙️ **ElevenLabs** — naturlig svensk kvinnlig röst (TTS)
- 🗣️ **Whisper (OpenAI)** — transkriberar tal till text
- ☎️ **Twilio** — tar emot och spelar upp telefonsamtal
- 💻 **Replit / Flask** — kör servern enkelt i webbläsaren

---

## ⚙️ Funktioner
✅ Svarar på inkommande telefonsamtal  
✅ Pratar naturlig svenska  
✅ Spelar in samtal och sparar dem i `recordings/`  
✅ Ställer enkla frågor tillbaka till den som ringer  
✅ Låter som en riktig mänsklig röst  

---

## 🚀 Kom igång (för Replit)

### 1️⃣ Skapa konton
Du behöver:
- [OpenAI API-key](https://platform.openai.com)
- [ElevenLabs API-key](https://elevenlabs.io)
- [Twilio account & phone number](https://www.twilio.com)

### 2️⃣ Importera till Replit
1. Gå till [https://replit.com](https://replit.com)
2. Klicka **Create new app**
3. Välj **Import from GitHub**
4. Klistra in:
5. https://github.com/
<ditt-användarnamn>/smartcall-lexa

5. Klicka **Import**

---

### 3️⃣ Lägg till dina API-nycklar
Klicka på **Secrets (🔑)** i vänstermenyn och lägg till:

| Key | Value |
|------|--------|
| `OPENAI_API_KEY` | din OpenAI-nyckel (börjar med sk-) |
| `ELEVEN_API_KEY` | din ElevenLabs-nyckel (börjar med eleven_) |
| `PUBLIC_BASE_URL` | din Replit-URL (fås efter första körningen) |

---

### 4️⃣ Kör servern
Tryck **Run**.  
Replit visar:


Your app is running at https://smartcall-lexa.username.repl.co


Kopiera länken och lägg in den i `PUBLIC_BASE_URL`.

Kör sedan **Run** igen.

---

### 5️⃣ Koppla till Twilio
1. Logga in på [Twilio Console → Phone Numbers](https://www.twilio.com/console/phone-numbers/incoming)
2. Klicka på ditt nummer
3. Under **Voice & Fax → A CALL COMES IN**, välj:
   - **Webhook**
   - URL:  
     ```
     https://smartcall-lexa.username.repl.co/voice
     ```
   - **HTTP POST**
4. Spara.

---

### 6️⃣ Testa demon 🎧
Ring ditt Twilio-nummer — Lexa svarar med svensk röst:
> “Hej! Du pratar med Lexa från Smart Call. Jag är en AI-röstassistent som hjälper företag att automatisera sina kundsamtal. Vill du testa hur jag fungerar?”

Samtalen spelas in i mappen `recordings/` — du kan klicka där i Replit för att lyssna på dem direkt.

---

## 🧠 System Prompt (Lexas personlighet)

Lexa är:
- Svensk, kvinnlig, proffsig men avslappnad  
- Hjälpsam, positiv och på hugget  
- Fokus: visa hur Smart Call kan effektivisera företagssamtal  
- Frågar gärna: “Vad jobbar du med idag?” eller “Vilken typ av samtal vill du automatisera?”

Avslutar alltid med:
> “Tack för att du testade Smart Calls AI-röst.  
> Vill du veta mer? Gå in på smartcall.ai.  
> Ha en fin dag!”

---

## 💬 Kontakt
**Smart Call AB**  
AI Voice Automation Demo – “Lexa”  
📧 info@smartcall.ai  
🌐 [smartcall.ai](https://smartcall.ai)

---

## 🧩 Mappstruktur


smartcall-lexa/
├── main.py
├── requirements.txt
├── .env.example
├── media/
│ └── .gitkeep
└── recordings/
└── .gitkeep


---

## ⚠️ Viktigt
- Lägg **inte** upp dina riktiga API-nycklar i GitHub.  
- Replit Free stänger av servern när den inte används (kan ta några sekunder innan Lexa svarar första gången).  
- För konstant drift, använd t.ex. Render eller Replit Pro.

---

✨ **Lexa – Powered by Smart Call**
