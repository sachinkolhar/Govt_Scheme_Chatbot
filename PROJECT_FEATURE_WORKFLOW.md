# Government Scheme Recommendation & Assistance System

## 1. Project Overview

### Purpose of the project

This system helps citizens discover relevant government schemes, check eligibility, ask scheme-related questions in natural language, and use voice or IVR-style interaction for easier access.

### Problem being solved

Many users struggle to:

- Find the right scheme among many options
- Understand eligibility conditions
- Navigate language and digital barriers
- Track next actions such as reminders and document readiness

The platform solves this by combining profile-based filtering, semantic search, AI-generated explanations, and multi-modal interfaces (text, voice, IVR demo).

### Main technologies used

- Frontend: Next.js (App Router), TypeScript, Tailwind CSS
- Backend: FastAPI, Python
- AI/ML: Sentence Transformer encoder, FAISS index, Groq LLM, Whisper, gTTS
- Database: SQLite via SQLAlchemy
- Storage: Local file storage for user uploads

---

## 2. System Workflow Overview

### End-to-end high-level flow

```text
+----------------+
| User           |
+----------------+
        |
        v
+----------------+
| Login/Register |
+----------------+
        |
        v
+---------------------------+
| Dashboard (Profile + UI)  |
+---------------------------+
   |           |           |
   |           |           |
   v           v           v
+-----------+ +----------------+ +----------------+
| Eligibility| | Chat Assistant | | Voice / IVR   |
| Finder     | |                | |                |
+-----------+ +----------------+ +----------------+
      \           |             /
       \          |            /
        \         v           /
         +-------------------+
         | Recommendation     |
         | & Response Engine  |
         +-------------------+
                  |
                  v
         +-------------------+
         | Results to User   |
         +-------------------+
```

### Architecture-style flow (frontend, backend, AI, data)

```text
+--------------------+          HTTP (Next rewrite/proxy)          +----------------------+
| Frontend (Next.js) | -------------------------------------------> | Backend (FastAPI)    |
| - Dashboard pages  |                                              | - Auth routes        |
| - Chat/Voice/IVR   | <------------------------------------------- | - Feature routes     |
+--------------------+              JSON / SSE / Audio              +----------------------+
          |                                                                    |
          |                                                                    |
          v                                                                    v
+----------------------+                                            +-----------------------+
| Browser local state  |                                            | SQLite (SQLAlchemy)   |
| - token, chat UI     |                                            | users/favorites/...   |
+----------------------+                                            +-----------------------+
                                                                               |
                                                                               v
                                                                  +-------------------------+
                                                                  | AI Components           |
                                                                  | FAISS + Encoder + Groq |
                                                                  | Whisper + gTTS         |
                                                                  +-------------------------+
```

### User interaction flow

1. User authenticates.
2. User completes/updates profile.
3. User runs eligibility search or asks chatbot/voice query.
4. Backend validates input and selects processing path.
5. AI/search modules produce matched schemes and/or explanation.
6. User saves favorites, adds reminders, and uploads documents.

### Frontend flow summary

- The frontend calls route-style endpoints like `/api/*` and `/auth/*`.
- Next.js rewrites/proxies these to FastAPI (`127.0.0.1:8000`).
- Chat uses streaming (SSE) for token-by-token assistant output.
- Voice uses audio APIs for STT (transcribe) and TTS (synthesize).

### Backend flow summary

- FastAPI app loads dataset, semantic encoder, FAISS index, and optional speech models at startup.
- Feature routers handle auth, search, eligibility, chat, voice, IVR, reminders, documents, and profile assets.
- SQLAlchemy models persist user and workflow data.

### AI flow summary

- Query/profile text -> semantic candidate retrieval (FAISS).
- Threshold logic decides confident DB match vs fallback behavior.
- Groq generates natural-language answer when required.
- Whisper converts speech to text; gTTS converts text to speech.

---

## 3. Eligibility Finder Workflow

### Step-by-step workflow

1. User enters profile details:
   - Age
   - Gender
   - Income
   - State
   - Category
   - Student/Farmer/Disability status
2. Frontend sends profile to backend (`POST /api/find-eligible`) or uses saved profile recommendations (`GET /api/recommendations`).
3. Backend validates payload through schema.
4. Eligibility engine builds a profile query and retrieves semantic candidates.
5. State compatibility filtering runs before scoring.
6. Rule-based eligibility checks are applied.
7. Match score (%) and recommendation reasons are computed.
8. Results are sorted and returned to frontend.
9. Frontend renders scheme cards with match percentage and reasons.

### Flow diagram

```text
+-------------------------+
| User fills profile form |
+-------------------------+
            |
            v
+------------------------------+
| Frontend API call            |
| /api/find-eligible (POST)    |
+------------------------------+
            |
            v
+------------------------------+
| Backend schema validation    |
+------------------------------+
            |
            v
+------------------------------+
| semantic_candidates()        |
| (FAISS + encoder)            |
+------------------------------+
            |
            v
+------------------------------+
| State pre-filter             |
| + eligibility rule checks    |
+------------------------------+
            |
            v
+------------------------------+
| calculate_match_score()      |
| + recommendation reasons     |
+------------------------------+
            |
            v
+------------------------------+
| Sorted top_k results         |
+------------------------------+
            |
            v
+------------------------------+
| Frontend result display      |
+------------------------------+
```

### Inputs

- Profile fields (age, gender, state, occupation, income, category, disability, student_status, farmer_status)
- Optional top_k

### Processing

- Text normalization and query construction
- Semantic candidate retrieval from FAISS index
- Rule checks for age/gender/category/state/occupation/income/disability
- Weighted scoring + reason generation

### Outputs

- List of scheme objects with:
  - scheme details
  - `match_score` (0-100)
  - recommendation reasons
  - favorite status

### APIs used

- `POST /api/find-eligible`
- `GET /api/recommendations`

### Database interactions

- Reads user profile for `/api/recommendations`
- Reads favorite records to mark `is_favorite`

---

## 4. Chat Assistant Workflow

### Step-by-step workflow

1. User asks a question in chat.
2. Frontend sends request to `/api/chat/stream` (or `/api/chat`).
3. Backend reads conversation state using `conversation_id`.
4. Query is semantically searched using FAISS candidates.
5. Confidence threshold (`FAISS_MIN_SCORE`) is evaluated.
6. If confident match exists:
   - Retrieve top scheme
   - Detect requested section (eligibility/benefits/documents/application/details)
   - Generate answer (section-only or Groq response)
7. If confidence is low:
   - Return no-data prompt and set follow-up state
   - If user replies yes, return relevant schemes (DB first, then web fallback)
8. Response is streamed as SSE events (`token`, `scheme`, `response_type`, `relevant_schemes`, `done`).
9. Frontend updates chat message progressively.
10. Conversation state memory is updated with TTL.

### Flow diagram

```text
+-----------------------+
| User chat question    |
+-----------------------+
           |
           v
+-------------------------------+
| POST /api/chat/stream         |
| query + history + language    |
+-------------------------------+
           |
           v
+-------------------------------+
| semantic_candidates(query)    |
+-------------------------------+
           |
           v
+-------------------------------+
| score >= FAISS_MIN_SCORE ?    |
+-------------------------------+
    | Yes                          | No
    v                              v
+-----------------------------+   +-------------------------------+
| scheme selected             |   | no_data_prompt response       |
| section detect / Groq       |   | pending_relevant_suggestions  |
+-----------------------------+   +-------------------------------+
    |                              |
    v                              v
+-----------------------------+   +-------------------------------+
| stream SSE tokens + scheme  |   | user yes/no follow-up         |
+-----------------------------+   +-------------------------------+
                                      | Yes
                                      v
                           +-------------------------------+
                           | DB relevant schemes           |
                           | else official web fallback    |
                           +-------------------------------+
```

### Search logic

- Retrieves multiple semantic candidates (`top_k`-based).
- Uses top score against threshold to determine confident match.
- Highest-confidence row is used as source scheme.

### Confidence threshold

- `FAISS_MIN_SCORE` from configuration (default 0.2).
- Low-confidence queries trigger no-data prompt + suggestion flow.

### Fallback behavior

- No confident DB match -> ask user if relevant schemes should be suggested.
- On yes:
  - Try DB relevant schemes first.
  - If none, use web search filtered to official domains (`gov.in`, `nic.in`, etc.).
  - Optional Groq summary for web results.

### State management

- Conversation state is in-memory map keyed by `conversation_id`.
- State fields track:
  - pending suggestion status
  - last query
  - update timestamp
- TTL cleanup removes expired states.

### Conversation memory

- Frontend sends recent chat history window.
- Backend passes recent history to Groq prompt.
- Current implementation does not persist chat history in SQL tables.

### APIs/modules involved

- APIs:
  - `POST /api/chat`
  - `POST /api/chat/stream`
- Modules:
  - `chat/processor.py`
  - `chat/groq_client.py`
  - `chat/state.py`
  - `search/semantic.py`
  - `search/web.py`

---

## 5. Voice Assistant Workflow

### Step-by-step workflow

1. User clicks mic and speaks query.
2. Browser records audio (MediaRecorder, enhanced audio constraints).
3. Frontend sends audio to `/api/audio/transcribe`.
4. Backend Whisper converts speech to text.
5. Text query is processed by voice assistant endpoint (`/api/voice-assistant/chat`).
6. Groq generates answer in selected language.
7. Frontend requests `/api/audio/synthesize` for TTS.
8. Backend gTTS returns base64 MP3.
9. Frontend plays audio (with browser TTS fallback if needed).

### Flow diagram

```text
+-----------------------+
| User speaks           |
+-----------------------+
           |
           v
+-------------------------------+
| MediaRecorder audio blob      |
+-------------------------------+
           |
           v
+-------------------------------+
| POST /api/audio/transcribe    |
+-------------------------------+
           |
           v
+-------------------------------+
| Whisper STT -> text query     |
+-------------------------------+
           |
           v
+-------------------------------+
| POST /api/voice-assistant/chat|
| (Groq answer generation)      |
+-------------------------------+
           |
           v
+-------------------------------+
| POST /api/audio/synthesize    |
| gTTS -> base64 mp3            |
+-------------------------------+
           |
           v
+-------------------------------+
| Audio playback to user        |
+-------------------------------+
```

### Whisper usage

- Whisper model is loaded during backend startup.
- STT endpoint decodes base64 audio and transcribes using CPU settings.
- FFmpeg availability is checked for decoding support.

### STT process

- Input: `audio_base64`, `language`, `format`
- Output: `success`, transcribed text, normalized language
- Includes localized error formatting

### TTS process

- Input: text + language
- gTTS generates MP3
- Output: base64 audio for frontend playback
- Browser speech synthesis is used as fallback if server audio fails

### Multilingual support

- Active language set: English (`en`), Hindi (`hi`), Telugu (`te`), Tamil (`ta`)
- Voice flow supports language selection and localized prompts

### APIs/modules involved

- APIs:
  - `POST /api/audio/transcribe`
  - `POST /api/audio/synthesize`
  - `POST /api/voice-assistant/chat`
  - `POST /api/voice-assistant/eligibility-criteria`
- Modules:
  - `voice/whisper.py`
  - `voice/gtts.py`
  - `voice/processor.py`
  - `chat/groq_client.py`

---

## 6. IVR Demo Workflow

### Step-by-step workflow

1. User clicks Take a Call.
2. Greeting/welcome message is played.
3. Language menu is announced.
4. User selects language via keypad.
5. Scheme summary for selected language is prepared.
6. Speech is generated using `/api/ivr/speak` (with browser fallback).
7. Audio playback starts.
8. Secondary menu appears:
   - 1 Benefits
   - 2 Eligibility
   - 3 Documents
   - 4 Application Process
   - 5 Repeat Summary
   - 6 Exit
9. User navigates via keypad.
10. System reads selected content and returns to menu until exit.

### Flow diagram

```text
+--------------------+
| Click Take a Call  |
+--------------------+
          |
          v
+-----------------------------+
| Play multilingual greeting  |
+-----------------------------+
          |
          v
+-----------------------------+
| Language selection keypad   |
+-----------------------------+
          |
          v
+-----------------------------+
| Read scheme summary         |
+-----------------------------+
          |
          v
+-----------------------------+
| Main IVR menu (1..6)        |
+-----------------------------+
   |1     |2       |3      |4      |5       |6
   v      v        v       v       v        v
Benefits Eligibility Docs  Apply  Summary  Exit
   \       |        |       |       |      /
    \______|________|_______|_______|_____/
                 back to menu
```

### Translation flow

- Backend provides `POST /api/ivr/translate` using Groq for text translation.
- IVR demo page currently uses predefined multilingual content and can call translation API when needed.

### Audio generation

- `POST /api/ivr/speak` delegates to shared TTS pipeline.
- If backend speech is unavailable, browser speech synthesis fallback is used.

### Menu navigation

- DTMF-style keypad inputs drive section routing.
- Section is spoken, then control returns to menu.

### Language handling

- Supported IVR language labels: English, Kannada, Hindi, Telugu, Tamil.
- Speech codes and fallback text are language-specific.

### APIs/modules involved

- APIs:
  - `GET /api/ivr/scheme/demo`
  - `GET /api/ivr/languages`
  - `POST /api/ivr/translate`
  - `POST /api/ivr/speak`
- Modules:
  - `ivr/routes.py`
  - `ivr/schemes.py`
  - `voice/gtts.py`

---

## 7. Recommendation Engine Workflow

### Workflow steps

1. Profile analysis
2. Eligibility filtering
3. Semantic relevance shortlist
4. Match score calculation
5. Recommendation reason generation
6. Ranking and response formatting

### Flow diagram

```text
+------------------------+
| User profile           |
+------------------------+
           |
           v
+------------------------+
| profile_to_query()     |
+------------------------+
           |
           v
+------------------------+
| semantic_candidates()  |
+------------------------+
           |
           v
+------------------------+
| strict state prefilter |
+------------------------+
           |
           v
+------------------------+
| is_eligible() rules    |
+------------------------+
           |
           v
+------------------------+
| calculate_match_score  |
+------------------------+
           |
           v
+------------------------+
| sort by match_score    |
+------------------------+
```

### Match percentage logic (implemented weights)

The score is capped at 100.

- State match: 30
- Category match: 20
- Occupation match: 15
- Student status match: 15
- Income eligibility: 10
- Age eligibility: 10

Formula style:

$$
\text{Match\_Score} = \min\left(100, S + C + O + St + I + A\right)
$$

Where:

- $S$ = state contribution
- $C$ = category contribution
- $O$ = occupation contribution
- $St$ = student-status contribution
- $I$ = income contribution
- $A$ = age contribution

### State matching

- Strict pre-filter removes schemes tied to other states.
- National/pan-India schemes are retained.
- User state exact/variant matching is considered.

### Category matching

- Supports SC/ST/OBC/General token-based compatibility checks.

### Income matching

- Income limits parsed from scheme text using regex patterns.
- User income is compared with extracted upper limit (if present).

### User profile scoring

- Combines demographic, socio-economic, and status flags.
- Adds recommendation reasons for explainability.

---

## 8. Saved Favorites Workflow

### Functional flow

- Save favorite scheme
- Retrieve favorites list
- Remove favorite
- Reflect favorite state in recommendation/eligibility cards

### Flow diagram

```text
+-----------------------+
| User clicks heart     |
+-----------------------+
      | save                      | remove
      v                           v
+-----------------------+      +-----------------------+
| POST /api/favorites/* |      | DELETE /api/favorites/*|
+-----------------------+      +-----------------------+
      |                           |
      v                           v
+-----------------------+      +-----------------------+
| favorites table write |      | favorites table delete|
+-----------------------+      +-----------------------+
               \              /
                v            v
             +----------------------+
             | GET /api/favorites   |
             | UI refresh           |
             +----------------------+
```

### APIs/modules involved

- `POST /api/favorites/{scheme_id}`
- `GET /api/favorites`
- `DELETE /api/favorites/{scheme_id}`

### Database storage

- `favorites` table with unique `(user_id, scheme_id)` constraint

---

## 9. Reminder System Workflow

### Functional flow

- Create reminder
- Store reminder
- Edit reminder
- Delete reminder
- Retrieve reminders list

### Flow diagram

```text
+------------------------+
| Reminder form input    |
+------------------------+
      | create/update/delete/list
      v
+------------------------------+
| /api/reminders CRUD endpoints|
+------------------------------+
      |
      v
+------------------------------+
| reminders table operations   |
+------------------------------+
      |
      v
+------------------------------+
| Updated reminder list in UI  |
+------------------------------+
```

### APIs/modules involved

- `POST /api/reminders`
- `GET /api/reminders`
- `PUT /api/reminders/{id}`
- `DELETE /api/reminders/{id}`

---

## 10. Document Management Workflow

### Functional flow

- Upload document
- File validation
- Secure storage path generation
- Retrieval/download
- Deletion

### Flow diagram

```text
+---------------------------+
| User selects file + type  |
+---------------------------+
           |
           v
+---------------------------+
| POST /api/documents       |
+---------------------------+
           |
           v
+---------------------------+
| MIME + size validation    |
| (<= 10 MB)                |
+---------------------------+
           |
           v
+---------------------------+
| Store in uploads/documents|
| save metadata in DB       |
+---------------------------+
           |
           v
+---------------------------+
| List / Download / Delete  |
+---------------------------+
```

### APIs/modules involved

- `POST /api/documents`
- `GET /api/documents`
- `GET /api/documents/{id}/download`
- `DELETE /api/documents/{id}`

### Storage location

- File content: local uploads directory under backend
- Metadata: `user_documents` table

---

## 11. Profile Management Workflow

### Functional flow

- Profile creation during signup
- Profile update from dashboard
- Profile photo upload/delete/retrieve
- Persistent storage in database + filesystem

### Flow diagram

```text
+-------------------------+
| Signup / Profile form   |
+-------------------------+
      | auth profile fields
      v
+-------------------------+
| /auth/signup, /auth/profile|
+-------------------------+
      |
      v
+-------------------------+
| users table updated     |
+-------------------------+

+-------------------------+
| Profile photo upload    |
+-------------------------+
      |
      v
+-------------------------+
| /api/profile/photo      |
+-------------------------+
      |
      v
+-------------------------+
| uploads/profile_photos  |
| + users photo metadata  |
+-------------------------+
```

### APIs/modules involved

- Auth profile:
  - `POST /auth/signup`
  - `GET /auth/me`
  - `PUT /auth/profile`
- Profile photo:
  - `POST /api/profile/photo`
  - `GET /api/profile/photo`
  - `GET /api/profile/photo/file`
  - `DELETE /api/profile/photo`

---

## 12. Multilingual Support Workflow

### Functional flow

- User selects language in chat/voice/IVR
- Language code normalized at backend
- Query/response generation occurs in selected language path
- STT/TTS engines use language-specific codes

### Flow diagram

```text
+---------------------------+
| User selects language     |
+---------------------------+
            |
            v
+---------------------------+
| Frontend sends language   |
| in API payload            |
+---------------------------+
            |
            v
+---------------------------+
| normalize_language_code() |
+---------------------------+
      |           |
      |           |
      v           v
+--------------------+   +--------------------+
| LLM response lang  |   | STT/TTS lang maps  |
+--------------------+   +--------------------+
            \            /
             v          v
            +----------------------+
            | Localized user output|
            +----------------------+
```

### Supported languages

- Chat/Voice core: English, Hindi, Telugu, Tamil
- IVR demo also includes Kannada path

### Language selection points

- Dashboard chat language dropdown
- Dedicated voice page language detection/selection
- IVR keypad-based language option

### Response generation

- Non-English chat requests are prefixed to guide model response language.
- Voice assistant prompt enforces target language name.
- Speech errors are localized.

---

## 13. Database Design

### Overview

Primary database is SQLAlchemy-backed (SQLite by default). Core persistent models are:

- Users
- Favorites
- Reminders
- Documents
- Profile fields/assets (within Users)
- Chat history (logical/session model, currently not persisted as a DB table)

### Users

Purpose:

- Authentication identity and complete profile storage.

Important fields:

- `id`, `username`, `name`, `password_hash`
- profile fields: `age`, `gender`, `state`, `occupation`, `income`, `category`
- eligibility flags: `disability`, `student_status`, `farmer_status`
- photo metadata: `profile_photo_path`, `profile_photo_updated_at`

Relationships:

- One user -> many favorites
- One user -> many reminders
- One user -> many documents

### Profiles

Purpose:

- User profile is embedded in `users` table (no separate profile table in current design).

Important fields:

- demographic + socio-economic + status flags in `users`

Relationships:

- Same as user relationships above

### Favorites

Purpose:

- Persist bookmarked schemes per user.

Important fields:

- `id`, `user_id`, `scheme_id`, `scheme_name`, `created_at`
- unique constraint on `(user_id, scheme_id)`

Relationships:

- Many favorites belong to one user

### Reminders

Purpose:

- Track deadlines/custom events for user actions.

Important fields:

- `id`, `user_id`, `title`, `description`, `reminder_date`
- `related_scheme_name`, `reminder_type`, timestamps

Relationships:

- Many reminders belong to one user

### Documents

Purpose:

- Store metadata of uploaded user documents.

Important fields:

- `id`, `user_id`, `document_type`, `original_name`, `stored_name`
- `mime_type`, `file_size`, `relative_path`, `created_at`

Relationships:

- Many documents belong to one user

### Chat history

Purpose:

- Maintain conversational context for better replies.

Current implementation details:

- Frontend sends recent message history window in API payload.
- Backend keeps lightweight conversation state in memory (`conversation_id` keyed state with TTL).
- No dedicated SQL chat history table is currently defined.

---

## 14. AI Components

### FAISS

Role:

- Fast vector similarity search over scheme embeddings.
- Retrieves candidate schemes for query/profile text.

### Sentence Transformers (semantic encoder)

Role:

- Converts text to dense embeddings used by FAISS.
- Loaded from serialized encoder file at backend startup.

### Groq LLM

Role:

- Generates natural language answers from scheme context.
- Summarizes web fallback results.
- Supports voice assistant responses and dynamic eligibility criteria prompts.

### Whisper

Role:

- Speech-to-text conversion for voice input.
- Handles multiple language codes and audio formats.

### gTTS

Role:

- Text-to-speech synthesis for assistant and IVR playback.
- Returns MP3 audio to frontend for playback.

---

## 15. End-to-End User Journey

### Complete user journey

Register
-> Complete Profile
-> Find Schemes
-> Ask Chatbot
-> Save Favorite
-> Create Reminder
-> Upload Documents
-> Use Voice Assistant
-> Use IVR Demo

### End-to-end flowchart

```text
+-------------------+
| User Registration |
+-------------------+
          |
          v
+-------------------+
| Profile Completion|
+-------------------+
          |
          v
+---------------------------+
| Eligibility + Reco Engine |
+---------------------------+
          |
          v
+---------------------------+
| Chat Assistant (SSE AI)   |
+---------------------------+
          |
          v
+---------------------------+
| Save Favorite Schemes     |
+---------------------------+
          |
          v
+---------------------------+
| Create/Edit Reminders     |
+---------------------------+
          |
          v
+---------------------------+
| Upload & Manage Documents |
+---------------------------+
          |
          v
+---------------------------+
| Voice Assistant (STT/TTS) |
+---------------------------+
          |
          v
+---------------------------+
| IVR Demo Call Flow        |
+---------------------------+
          |
          v
+---------------------------+
| Better Access + Guidance  |
+---------------------------+
```

---

## API and Module Reference Snapshot

### Backend routers

- Auth: `/auth/*`
- Search: `/api/search`, `/api/categories`
- Eligibility + favorites: `/api/find-eligible`, `/api/recommendations`, `/api/favorites/*`
- Chat: `/api/chat`, `/api/chat/stream`
- Voice/STT/TTS: `/api/audio/*`, `/api/voice-assistant/*`
- IVR: `/api/ivr/*`
- Reminders: `/api/reminders/*`
- Documents: `/api/documents/*`
- Profile assets: `/api/profile/photo*`

### Core backend modules

- Startup/app composition: `backend/main.py`
- Eligibility logic: `eligibility/checker.py`
- Semantic search: `search/semantic.py`
- Chat orchestration: `chat/processor.py`
- LLM integration: `chat/groq_client.py`
- Voice processing: `voice/whisper.py`, `voice/gtts.py`, `voice/processor.py`
- IVR logic: `ivr/routes.py`, `ivr/schemes.py`
- Data models: `models/database.py`, `models/schemas.py`

### Frontend integration modules

- Session/auth handling: `lib/useAuthSession.ts`
- Generic API utilities: `services/api.ts`
- Chat API wrapper: `lib/api/chat.ts`
- Voice audio utilities: `lib/audioApi.ts`
- IVR API wrapper: `lib/api/ivr.ts`
- Reminders/documents/profile assets API wrappers: `lib/api/*.ts`

### Data flow summary

- Frontend -> FastAPI (proxy via Next rewrites)
- FastAPI -> AI modules + SQLite + file storage
- FastAPI -> Frontend (JSON/SSE/audio base64)
- Frontend -> user-facing UI cards, chat stream, voice/IVR playback

This completes the internal workflow documentation for implementation understanding, review, and viva preparation.
