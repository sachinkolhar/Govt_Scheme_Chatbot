# IVR Demo - Quick Start

## 🚀 Start the Project

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🌐 Access the Demo

Open browser: **http://localhost:3000/ivr-demo**

## 📱 How to Use

1. Click **"🟢 Take a Call"** button
2. Listen to greeting with language options
3. Press **1-5** to select language (or 6 to exit)
4. Listen to **Summary** in your language
5. Press **1-5** to select section:
   - 1 = Benefits
   - 2 = Eligibility
   - 3 = Documents
   - 4 = Application Process
   - 5 = Repeat Summary
   - 6 = End Call
6. Listen to section content
7. Repeat steps 5-6 or press 6 to end

## 🎮 Keyboard Shortcuts

- Press **0-9, \*, #** on keyboard to press dial pad
- Works alongside mouse/touch

## 🗂️ Folder Structure

```
Backend:
backend/ivr/
  ├── __init__.py
  ├── routes.py (FastAPI endpoints)
  └── schemes.py (Hardcoded data)

Frontend:
frontend/
  ├── app/ivr-demo/page.tsx (Route)
  ├── components/ivr/ (5 components)
  └── lib/
      ├── types/ivr.ts (Interfaces)
      └── api/ivr.ts (API functions)
```

## 🎯 Key Features

✅ Hardcoded PM Kisan Yojana data
✅ 5 languages supported (English, Kannada, Hindi, Telugu, Tamil)
✅ Dynamic translation via Groq
✅ Text-to-speech via gTTS
✅ Mobile dial pad UI
✅ Real-time waveform animation
✅ Keyboard + mouse/touch support
✅ Call status tracking
✅ Volume control + mute
✅ Responsive design

## 📊 Call Flow

```
Take Call → Greeting → Language Selection → Summary →
Menu → Section Selection → Play Section → Menu (repeat) → Exit
```

## 🔧 API Endpoints

- `POST /api/ivr/translate` - Translate text
- `POST /api/ivr/speak` - Generate speech
- `GET /api/ivr/scheme/demo` - Get PM Kisan data
- `GET /api/ivr/languages` - Get language list

## 📖 Full Documentation

See **IVR_DEMO_GUIDE.md** for comprehensive implementation details.
