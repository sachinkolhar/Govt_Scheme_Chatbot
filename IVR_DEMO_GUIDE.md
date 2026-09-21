# IVR Demo Implementation Guide

## Project Structure

```
Government_Scheme_Chatbot/
├── backend/
│   └── ivr/
│       ├── __init__.py
│       ├── routes.py           (FastAPI endpoints)
│       └── schemes.py          (Hardcoded PM Kisan data)
│
└── frontend/
    ├── app/
    │   └── ivr-demo/
    │       └── page.tsx        (Next.js page route)
    │
    ├── components/
    │   └── ivr/
    │       ├── IVRDemoPage.tsx       (Main component)
    │       ├── PhoneKeypad.tsx       (Dial pad UI)
    │       ├── WaveformAnimation.tsx (Audio visualization)
    │       ├── CallStatusPanel.tsx   (Call info display)
    │       └── VoicePlayer.tsx       (Audio playback)
    │
    └── lib/
        ├── types/
        │   └── ivr.ts          (TypeScript interfaces)
        └── api/
            └── ivr.ts          (API wrapper functions)
```

## Backend Implementation

### 1. `/backend/ivr/schemes.py`

**Hardcoded PM Kisan Yojana Data**

- Scheme name, summary, benefits, eligibility, documents, application process
- Language mapping for keypad (1-5 for different languages, 6 for exit)
- National scheme designation

### 2. `/backend/ivr/routes.py`

**FastAPI Endpoints**

```python
POST /api/ivr/translate
- Input: text, language
- Output: original_text, translated_text, language
- Uses Groq for translation

POST /api/ivr/speak
- Input: text, language
- Output: audio (hex-encoded), language, text, format
- Uses existing gTTS system

GET /api/ivr/scheme/demo
- Returns hardcoded PM Kisan data

GET /api/ivr/languages
- Returns available languages (1-6 keypad mapping)
```

### 3. Backend Integration

- Added `"ivr.routes"` to router inclusion in `main.py`
- Uses existing Groq client for translation (`get_groq_client()`)
- Uses existing gTTS for speech synthesis (`text_to_speech_bytes()`)

## Frontend Implementation

### 1. TypeScript Types (`frontend/lib/types/ivr.ts`)

```typescript
- IVRScheme: Scheme data structure
- TranslateRequest/Response: Translation API models
- SpeakRequest/Response: Speech API models
- IVRLanguage: Union type for supported languages
- IVRCallState: Call state management
- PhoneKeypadEvent: Key press events
```

### 2. API Wrapper Functions (`frontend/lib/api/ivr.ts`)

```typescript
- translateText(): Call POST /api/ivr/translate
- speakText(): Call POST /api/ivr/speak
- getDemoScheme(): Fetch hardcoded PM Kisan data
- getAvailableLanguages(): Get language options
- audioHexToBlob(): Convert hex-encoded audio to Blob
```

### 3. Reusable Components

#### `PhoneKeypad.tsx`

- 4x3 grid (0-9, \*, #)
- Mobile dial pad styling with Tailwind
- Touch-based and keyboard support (both work!)
- Hover and active animations
- Disabled state when speaking
- Responsive sizing (smaller on mobile, larger on desktop)

#### `WaveformAnimation.tsx`

- 12 animated bars representing audio
- Updates every 100ms when playing
- Gradient color (blue to cyan)
- Smooth transitions

#### `CallStatusPanel.tsx`

- Call status indicators (🟢 Connected, 🔊 Speaking, etc.)
- Language display (English, Kannada, etc.)
- Current section display (Summary, Benefits, etc.)
- Real-time call timer (MM:SS format)
- Volume slider (0-100%)
- Mute button
- Red End Call button

#### `VoicePlayer.tsx`

- Hidden audio element
- Manages audio blob playback
- Volume and mute control
- Auto-play support
- Completion callback

#### `IVRDemoPage.tsx` (Main Component)

- State management for entire IVR flow
- Call lifecycle (ringing → connected → speaking → ended)
- Language selection logic
- Menu navigation
- Section selection
- Dynamic speech generation and playback
- Integration of all sub-components

### 4. Routing (`frontend/app/ivr-demo/page.tsx`)

- Next.js page at `/ivr-demo`
- Metadata for SEO
- Server component wrapper

## IVR Call Flow

### Step 1: Initial State

```
User sees: "🟢 Take a Call" button
Action: Click button
```

### Step 2: Greeting & Language Selection

```
Audio plays: "Welcome to Government Scheme Assistant..."
Shows: Language menu (1-5 options + 6 to exit)
User presses: 1-5 for language or 6 to exit
```

### Step 3: Summary

```
Summary is translated to selected language
Audio: PM Kisan summary in selected language
After playback: Menu automatically plays
```

### Step 4: Main Menu

```
Audio plays: "Press 1 for Benefits, Press 2 for Eligibility..."
User can select: 1=Benefits, 2=Eligibility, 3=Documents, 4=Process, 5=Repeat Summary, 6=Exit
```

### Step 5: Section Display

```
Selected section is translated and spoken
After playback: Menu repeats automatically
```

### Step 6: End Call

```
Press 6 at any menu → Call ends
Call timer stops
UI returns to initial state
```

## Supported Languages

| Key | Language | Code |
| --- | -------- | ---- |
| 1   | English  | en   |
| 2   | Kannada  | kn   |
| 3   | Hindi    | hi   |
| 4   | Telugu   | te   |
| 5   | Tamil    | ta   |
| 6   | Exit     | -    |

## UI Features

### Visual Components

- **Call Status Indicator**: Shows current state with emoji (🟢 Connected, 🔊 Speaking, etc.)
- **Waveform Animation**: Real-time audio visualization
- **Call Timer**: MM:SS format duration
- **Phone Keypad**: Mobile dial pad design
- **Display Text**: Shows transcribed/spoken content
- **Volume Slider**: Control audio volume
- **Mute Button**: Toggle audio mute

### Responsive Design

- Mobile: Smaller buttons, compact layout
- Tablet: Medium-sized components
- Desktop: Full-sized interactive elements
- All components use Tailwind CSS

### Interactions

- **Keyboard Support**: Press 0-9, \*, # on keyboard
- **Mouse/Touch**: Click dial pad buttons
- **Mobile**: Full touch optimization
- **Hover Effects**: Visual feedback on buttons
- **Active States**: Button press animations

## Data Flow

```
User Press Key
    ↓
handleKeyPress() processes key
    ↓
Route to appropriate handler (language/menu/section)
    ↓
Fetch translation if needed
    ↓
Generate speech via Groq + TTS
    ↓
Convert hex audio to Blob
    ↓
Play audio with VoicePlayer
    ↓
Update UI (status, display text, waveform)
    ↓
On completion, trigger next step
```

## Testing Instructions

### 1. Start Backend

```bash
# Terminal 1: Start FastAPI server
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend

```bash
# Terminal 2: Start Next.js dev server
cd frontend
npm run dev
```

### 3. Test IVR Demo

```
Navigate to: http://localhost:3000/ivr-demo
1. Click "🟢 Take a Call" button
2. Listen to greeting (language options)
3. Press "1" for English (or 2-5 for other languages)
4. Wait for summary to play
5. After summary, menu plays automatically
6. Press "1" for Benefits, "2" for Eligibility, etc.
7. Listen to selected section
8. Menu repeats
9. Press "6" to end call
```

## Hardcoded Scheme Data: PM Kisan Samman Nidhi Yojana

**Scheme Name:** PM Kisan Samman Nidhi Yojana

**Summary:**
PM Kisan Samman Nidhi Yojana provides financial assistance of ₹6000 per year to eligible farmer families across India. The amount is transferred directly to beneficiaries' bank accounts in three installments.

**Benefits:**

- ₹6000 annual financial support
- Direct Benefit Transfer (DBT)
- Available across India
- Supports small and marginal farmers

**Eligibility:**

- Applicant must be a farmer
- Must own cultivable land
- Indian citizen
- Government employees and income tax payers are generally excluded

**Documents:**

- Aadhaar Card
- Bank Account Details
- Land Ownership Documents
- Mobile Number

**Application Process:**

1. Visit PM Kisan portal
2. Register farmer details
3. Upload required documents
4. Submit application
5. Verification by authorities
6. Amount credited after approval

## Future Enhancements

1. **Connect to Real Database**: Replace hardcoded data with database queries
2. **Multiple Schemes**: Add support for multiple schemes via dropdown
3. **Recording**: Record calls for training/analysis
4. **Sentiment Analysis**: Detect user emotions from voice
5. **Natural Language Processing**: Understand free-form voice input
6. **Persistent Call History**: Save call logs per user
7. **Analytics Dashboard**: Track call metrics (duration, language, sections accessed)
8. **Escalation**: Transfer to human agent option

## Dependencies

### Backend

- FastAPI: API framework
- Pydantic: Request/response validation
- Groq: Translation AI
- gTTS: Text-to-speech

### Frontend

- Next.js 15: React framework
- TypeScript: Type safety
- Tailwind CSS: Styling
- React Hooks: State management

## Notes

- **No Database Connection**: Demo uses hardcoded data only
- **Language Limitations**: Translations depend on Groq availability
- **Audio Format**: MP3 via gTTS
- **Browser Compatibility**: Modern browsers with Web Audio API support
- **Accessibility**: Full keyboard support, ARIA labels included
- **CORS**: Frontend on localhost:3000, Backend on localhost:8000

## Troubleshooting

### Audio Not Playing

- Check browser console for errors
- Verify Groq API availability
- Check volume settings in CallStatusPanel
- Ensure browser microphone permissions

### Translation Not Working

- Verify Groq API key in backend
- Check language code mapping
- Review Groq rate limits

### Keypad Not Responding

- Ensure audio is not currently playing (keypad disables during playback)
- Check browser keyboard focus
- Verify enabled prop in PhoneKeypad component

### Call Not Starting

- Check if scheme data loaded (verify `getDemoScheme()` response)
- Review browser console for API errors
- Check CORS headers from backend
