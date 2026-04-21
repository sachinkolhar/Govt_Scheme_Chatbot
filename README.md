# Government Scheme Chatbot

A full-stack AI-powered assistant that helps citizens discover, search, and understand Indian government schemes — with personalized recommendations, eligibility filtering, and a conversational AI interface powered by Groq.

---

## Features

- **JWT Authentication** — Secure signup & login with password policy enforcement
- **User Profile** — Store age, gender, state, occupation, income, category, disability, and student/farmer status
- **Personalized Recommendations** — FAISS semantic search + rule-based eligibility engine surfaces the most relevant schemes for each user
- **Eligibility Finder** — Ad-hoc profile input to find matching schemes without saving
- **AI Assistant (RAG)** — Natural language questions answered using Groq LLM with real-time streaming (typewriter effect), structured output, and a source scheme card
- **Multilingual Support** — 4 languages supported: English, हिंदी (Hindi), తెలుగు (Telugu), தமிழ் (Tamil) with runtime language switching
- **Smart Follow-up System** — When the assistant can't find results initially, it asks yes/no to clarify intent, with auto-hide badge detection
- **Web Fallback Search** — If scheme database has no matches, the system automatically searches official government websites (`.gov.in`) and summarizes results
- **Section-Specific Answers** — Detect when users ask for specific sections (eligibility, benefits, application process, documents required) and return targeted information
- **Browse by Category** — Explore top scheme categories at a glance
- **3,400+ Schemes** — Dataset covering Central and State schemes across agriculture, education, health, housing, and more
- **Automated Testing** — Comprehensive pytest coverage for all chat decision tree branches

---

## Tech Stack

| Layer           | Technology                                          |
| --------------- | --------------------------------------------------- |
| Frontend        | Next.js 15, TypeScript, Tailwind CSS                |
| Backend         | FastAPI (Python), SQLAlchemy, SQLite                |
| Semantic Search | FAISS + SentenceTransformers                        |
| LLM             | Groq API (`llama-3.3-70b-versatile`)                |
| Auth            | JWT (`python-jose`), PBKDF2-SHA256 password hashing |
| Config          | `python-dotenv`                                     |
| Testing         | pytest with monkeypatching                          |
| Web Search      | duckduckgo-search API                               |

---

## Design Approach

- **Grounded answers over free-form AI** — The assistant uses retrieval-first behavior so responses are anchored to actual scheme records instead of relying only on the language model.
- **Intelligent fallback chain** — DB-first search, then web fallback if no results, then LLM summarization for multi-language government content.
- **Conversational intent detection** — The system detects yes/no follow-up responses to clarify intent when initial search yields no results, with visual feedback (badge).
- **Section-aware extraction** — Keywords like "eligibility", "benefits", "application", "documents" trigger targeted scheme section retrieval instead of full LLM generation.
- **Multilingual at scale** — Support for 4 Indian languages (English, Hindi, Telugu, Tamil) with automatic query prefixing for language-aware LLM responses.
- **Profile-driven discovery** — User profile fields such as age, state, occupation, income, category, disability, and student/farmer status are used to improve recommendation quality and eligibility matching.
- **Separation of concerns** — The Next.js frontend handles UI, state, and localization, while FastAPI owns authentication, profile management, scheme retrieval, chat orchestration, and recommendation logic.
- **Fast local development** — The project defaults to SQLite and file-based assets (`govt_schemes.csv`, FAISS index, encoder pickle) so it can run locally with minimal setup.
- **Practical RAG pipeline** — Semantic search narrows relevant schemes first, then Groq generates the final natural-language answer using the retrieved scheme context.

---

## Architecture

### High-level components

- **Frontend (`frontend/`)** — Next.js App Router application that provides authentication screens, profile management, recommendation views, eligibility search, and streaming chat UI.
- **Backend (`backend/main.py`)** — FastAPI service that exposes auth and scheme endpoints, loads the model assets at startup, and coordinates retrieval and LLM responses.
- **Data layer (`dataset/`, `model/`)** — CSV scheme dataset, FAISS vector index, and semantic encoder used for search and retrieval.
- **Persistence layer** — SQLite by default for users and profiles, with optional PostgreSQL support through `DATABASE_URL`.
- **LLM layer** — Groq API is used only after retrieval to generate grounded answers for scheme-related questions.

### Request flow

```text
Browser
	-> Next.js frontend
	-> Next.js rewrites (`/api`, `/auth`, `/health`)
	-> FastAPI backend
		 -> SQLite/PostgreSQL for auth + profile data
		 -> FAISS + semantic encoder + CSV dataset for search/recommendations
		 -> Groq API for RAG chat responses
	-> JSON / streaming response back to frontend
```

### Functional flow by feature

1. **Authentication**: The frontend calls `/auth/signup`, `/auth/login`, and `/auth/me`; FastAPI validates credentials, hashes passwords with PBKDF2, and returns JWTs.
2. **Recommendations**: The backend reads the authenticated user's saved profile, applies eligibility-oriented logic, and combines it with semantic retrieval to rank relevant schemes.
3. **Eligibility Finder**: The frontend submits ad-hoc profile filters to `/api/find-eligible` without requiring profile persistence.
4. **Search and Chat**: Query text is cleaned, embedded, and searched against the FAISS index; the top results are returned directly for search or passed into Groq as context for RAG chat.
5. **Streaming AI replies**: `/api/chat/stream` returns incremental output so the frontend can render a typewriter-style assistant response.

---

## Project Structure

```
Govt_Scheme_Chatbot/
├── backend/
│   ├── main.py            # FastAPI app — auth, search, chat, recommendations
│   ├── requirements.txt   # Python dependencies
│   ├── tests/
│   │   └── test_chat_flow.py  # Automated tests for chat decision branches
│   ├── .env               # API keys & secrets (not committed)
│   └── .env.example       # Template for environment variables
├── frontend/
│   ├── app/
│   │   └── page.tsx       # Main dashboard (auth, profile, chat, recommendations)
│   ├── components/
│   │   ├── SchemeCard.tsx
│   │   └── SearchBar.tsx
│   └── next.config.ts     # Proxy rewrites → backend
├── dataset/
│   └── govt_schemes.csv   # 3,400+ government schemes
├── model/
│   ├── scheme_index.faiss # FAISS vector index
│   └── scheme_embeddings.npy
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Groq API key](https://console.groq.com)

---

### Quick Start (Windows)

For a faster setup, use the included PowerShell script to start both backend and frontend simultaneously:

```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Run the dev script (starts both backend on port 8000 and frontend on port 3000)
.\start-dev.ps1
```

Alternatively, using npm:

```bash
npm run dev
```

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Govt_Scheme_Chatbot.git
cd Govt_Scheme_Chatbot
```

---

### 2. Backend setup

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies (includes pytest for testing)
pip install -r backend/requirements.txt
```

Copy the example env file and fill in your keys:

```powershell
Copy-Item backend/.env.example backend/.env
```

Edit `backend/.env`:

```env
JWT_SECRET=your-strong-random-secret
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
# DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/govt_schemes
```

Start the backend:

```powershell
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 3. Frontend setup

```powershell
cd frontend
npm install
npm run dev
```

The app will be available at [http://localhost:3000](http://localhost:3000).

---

## API Endpoints

| Method | Endpoint               | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| `POST` | `/auth/signup`         | Register a new user                |
| `POST` | `/auth/login`          | Login and receive JWT              |
| `GET`  | `/auth/me`             | Get current user profile           |
| `PUT`  | `/auth/profile`        | Update user profile                |
| `POST` | `/api/search`          | Semantic scheme search             |
| `POST` | `/api/chat`            | Single-response RAG chat           |
| `POST` | `/api/chat/stream`     | Streaming RAG chat (SSE)           |
| `POST` | `/api/find-eligible`   | Find schemes by ad-hoc profile     |
| `GET`  | `/api/recommendations` | Personalized recommendations (JWT) |
| `GET`  | `/api/categories`      | Top 15 scheme categories           |
| `GET`  | `/health`              | Health check                       |

---

## Password Policy

Passwords must meet all of the following:

- Minimum **8 characters**
- At least **1 uppercase** letter
- At least **1 number**
- At least **1 special character** (`!@#$%^&*` etc.)

---

## Environment Variables

| Variable       | Required | Description                                        |
| -------------- | -------- | -------------------------------------------------- |
| `JWT_SECRET`   | Yes      | Secret key for signing JWT tokens                  |
| `GROQ_API_KEY` | Yes      | Groq API key from console.groq.com                 |
| `GROQ_MODEL`   | No       | Groq model ID (default: `llama-3.3-70b-versatile`) |
| `DATABASE_URL` | No       | PostgreSQL URL (default: SQLite `app.db`)          |

---

## Multilingual Support

The chatbot supports **4 Indian languages**:

| Language | Code | Available UI                  |
| -------- | ---- | ----------------------------- |
| English  | `en` | ✅ All UI elements translated |
| हिंदी    | `hi` | ✅ All UI elements translated |
| తెలుగు   | `te` | ✅ All UI elements translated |
| தமிழ்    | `ta` | ✅ All UI elements translated |

### Language Switching

- Use the **Language** dropdown selector in the chat section header
- Selection is applied immediately to all UI text
- Non-English queries are automatically prefixed with language context for the LLM
- Example: Query in Hindi → Backend receives "Please answer in हिंदी. Question: [original query]"

### Localized Strings

The following UI elements are fully localized:

- Chat interface title and subtitle
- Empty state message
- Search placeholder text and button labels
- Loading states
- Yes/no follow-up badge
- Language selector label

---

## Chat Features

### Smart Yes/No Follow-up

When the AI assistant cannot find relevant schemes in the database:

1. It prompts the user with "Would you like me to search the web?"
2. A **pulsing badge** appears below the input box showing "Awaiting your yes/no reply"
3. The badge automatically hides when you start typing a yes/no response
4. Typing **"yes"** (or variations: y, yeah, yep, sure, ok) triggers web search
5. Typing **"no"** (or variations: n, nope, nah) cancels the follow-up and returns to chat

### Web Fallback Search

When database search returns no results and user agrees:

1. System searches official government websites (`.gov.in` domain) using DuckDuckGo
2. Retrieved web content is automatically summarized by Groq LLM
3. Results are presented with scheme cards in the chat

### Section-Specific Answers

Users can ask for specific scheme information:

- **Eligibility**: "What is the eligibility for this scheme?"
- **Benefits**: "What benefits does this scheme provide?"
- **Application**: "How do I apply for this scheme?"
- **Documents**: "What documents are needed?"
- **Details**: "Tell me more details about..."

The system detects these keywords and returns only the requested section without full LLM generation, improving response speed.

---

## Testing

### Run Backend Tests

```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Run all tests
python -m pytest backend/tests/ -v

# Run with coverage
python -m pytest backend/tests/ --cov=backend --cov-report=html
```

### Test Coverage

The `test_chat_flow.py` file includes **6 comprehensive tests** covering:

1. **DB Miss Scenario** — Verifies pending state when no schemes found
2. **Yes Follow-up** — Confirms yes response uses database results
3. **Web Fallback** — Tests fallback to web search when DB is empty
4. **No Follow-up** — Validates that no response clears pending mode
5. **Section-Only Answers** — Tests section-specific retrieval
6. **Unrelated Yes** — Ensures yes is treated as normal query when not awaiting follow-up

All tests use monkeypatching for deterministic execution without external API calls.

---

## Troubleshooting

### Backend Issues

**AttributeError: module 'torch' has no attribute 'load'**

- Clear Python cache: `python -m compileall -b backend/`
- Reinstall torch: `pip install --force-reinstall torch`
- Ensure `CUDA_VISIBLE_DEVICES=-1` is set before starting the server

**FAISS index not found**

- Verify `model/scheme_index.faiss` exists
- Ensure you're running the backend from the project root directory
- Check file paths: MODEL_DIR should be `<root>/model`

**"Invalid JWT token" or session expiration**

- Clear cookies in your browser
- JWT tokens expire after 24 hours; log in again
- Verify `JWT_SECRET` is set consistently in `.env`

**Groq API rate limits or quota exceeded**

- Check your Groq API usage at https://console.groq.com
- Rate limit: 30 requests per minute (default tier)
- Consider upgrading your Groq plan or implement request throttling

**PostgreSQL connection failed**

- If using PostgreSQL, verify `DATABASE_URL` format: `postgresql+psycopg2://user:pass@host:port/dbname`
- Ensure PostgreSQL service is running and accessible
- Default is SQLite (`app.db`) if `DATABASE_URL` is not set

### Frontend Issues

**"Cannot GET /api/something" errors**

- Verify backend is running on `http://localhost:8000`
- Check Next.js rewrites in `frontend/next.config.ts`
- Ensure CORS is enabled on the backend (it is by default)

**Language selector not working**

- Clear browser cache and cookies
- Verify all 4 language constants are defined in `frontend/app/page.tsx`
- Check that language query parameter is passed to API calls

**Streaming chat response incomplete**

- SSE connection may have timed out
- Check browser console for network errors
- Verify backend is using `--reload` for development

### Common Setup Issues

**"Python venv not found"**

- Create venv: `python -m venv venv`
- On Windows: `.\venv\Scripts\Activate.ps1`
- On macOS/Linux: `source venv/bin/activate`

**"npm: command not found"**

- Install Node.js from https://nodejs.org (18+)
- Verify with: `node -v && npm -v`

**Port 3000 or 8000 already in use**

- Kill existing process: `netstat -ano | findstr :3000` (Windows)
- Or change port in backend: `--port 8001`
- Or change frontend port in `frontend/package.json`

**Module not found errors**

- Reinstall dependencies: `pip install -r backend/requirements.txt`
- Or: `cd frontend && npm install`
- Clear pip cache: `pip cache purge`

---

## Known Limitations

- **Dataset size**: Currently limited to ~3,400 schemes from the CSV dataset
- **Vector search latency**: First query takes ~2-3 seconds (FAISS index load); subsequent queries are ~200ms
- **Concurrent sessions**: SQLite supports limited concurrent writes; use PostgreSQL for production with many users
- **LLM context**: Groq model has a token limit (~8k); very long scheme descriptions may be truncated
- **Web search fallback**: Only searches `.gov.in` domains; may not cover all government resources
- **Language models**: LLM responses are generated by Groq; not fine-tuned on Indian scheme nomenclature—may hallucinate details
- **Encoding**: SentenceTransformer model requires ~500MB RAM; CPU-only mode is slower but works
- **Browser support**: Tested on Chrome, Firefox, Safari; Edge may have minor UI issues

---

## Deployment

### Docker (Optional)

To containerize the application:

1. **Create `Dockerfile` in project root:**

```dockerfile
FROM python:3.10-slim as backend-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM python:3.10-slim
WORKDIR /app
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY backend/ ./backend
COPY model/ ./model
COPY dataset/ ./dataset
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
EXPOSE 8000 3000
CMD ["python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
```

2. **Build and run:**

```bash
docker build -t govt-scheme-chatbot .
docker run -p 3000:3000 -p 8000:8000 --env-file backend/.env govt-scheme-chatbot
```

### Production Recommendations

- **Database**: Use PostgreSQL instead of SQLite for concurrent users
- **Secrets**: Store `JWT_SECRET` and `GROQ_API_KEY` in environment variables or secret manager (AWS Secrets Manager, GitHub Secrets, etc.)
- **Reverse Proxy**: Use Nginx or Caddy to proxy requests to FastAPI backend
- **SSL/TLS**: Enable HTTPS using Let's Encrypt certificates
- **Caching**: Add Redis for session caching and rate limiting
- **Monitoring**: Use tools like Sentry, DataDog, or ELK stack for logging and error tracking
- **Vector Search**: Pre-compute and cache FAISS search results for popular queries

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and write tests
4. Run tests: `pytest backend/tests/ -v`
5. Commit with clear messages: `git commit -m "Add feature X"`
6. Push to your fork and open a Pull Request

### Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code (no plain JavaScript)
- Add tests for new backend features
- Update README if adding new features
- Keep commits atomic and focused

---

## Screenshots

> Dashboard, chat interface, recommendations view, and eligibility finder screenshots coming soon.

---

## License

MIT
#   G o v e r n m e n t _ S c h e m e _ C h a t B o t  
 