# 🤖 SRI AI Agent

A sophisticated, voice-enabled AI personal assistant built with **LiveKit Agents** and **Google Gemini's Realtime API**. Sri speaks like a classy (and delightfully sarcastic) butler, and can search the web, check the weather, tell you the time, and even send emails on your behalf — all through natural voice conversation.

---

## ✨ Features

- 🎙️ **Real-time Voice Interaction** — Powered by LiveKit's agent framework with noise cancellation
- 🌦️ **Weather Lookup** — Get current weather for any city
- 🕐 **Date & Time** — Accurate IST date/time via a dedicated tool
- 🔍 **Web Search** — Live web search powered by the [Serper.dev](https://serper.dev) API
- 📧 **Send Emails** — Compose and send emails via Gmail SMTP
- 🎭 **Unique Persona** — Responds in one sentence, like a classy, sarcastic butler

---

## 🗂️ Project Structure
├── **agent.py**                —Main agent definition and LiveKit entrypoint  
├── **prompts.py**          —Agent persona and session instructions)  
├── **tools.py**           —Tool implementations (weather, search, email, datetime)  
├── **requirements.txt**   — Python dependencies  
├── **.env**               — 🔒 Local only — NOT pushed to GitHub (contains API keys)  
└── **README.md**  

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Naga-Vikram/SRI_AI_AGENT.git
cd sri-ai-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory (this file is **not** included in the repo as it contains sensitive keys):

```env
# LiveKit Configuration
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# Google Gemini (Realtime API)
GOOGLE_API_KEY=your_google_api_key

# Serper.dev Web Search
SERPER_API_KEY=your_serper_api_key

# Gmail SMTP (use an App Password, not your regular password)
GMAIL_USER=your_gmail_address@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
```

> ⚠️ **Never commit your `.env` file to GitHub.** Make sure it's listed in your `.gitignore`.

### 4. Run the Agent

```bash
python agent.py start
```

---

## 🔑 API Keys & Services

| Service | Purpose | Link |
|---|---|---|
| LiveKit | Real-time voice/video infrastructure | [livekit.io](https://livekit.io) |
| Google Gemini Realtime | LLM + voice synthesis | [Google AI Studio](https://aistudio.google.com) |
| Serper.dev | Web search API | [serper.dev](https://serper.dev) |
| Gmail SMTP | Sending emails | [Google App Passwords](https://myaccount.google.com/apppasswords) |
| wttr.in | Weather data (no key needed) | [wttr.in](https://wttr.in) |

---

## 🛠️ Tools Overview

### `get_weather(city)`
Fetches current weather conditions for any city using the `wttr.in` service.

### `get_current_datetime()`
Returns the current date and time in **Indian Standard Time (IST)**.

### `search_web(query)`
Performs a live web search via Serper.dev and returns the top 3 results with snippets.

### `send_email(to_email, subject, message, cc_email?)`
Sends an email via Gmail SMTP. Requires all three core fields (recipient, subject, body). CC is optional.

---

## 💬 Example Interactions

> **User:** "What's the weather in Mumbai?"
> **Sri:** "Checking the current conditions, if you insist — Mumbai is experiencing 32°C with humid skies, as one might expect."

> **User:** "Search for the latest AI news."
> **Sri:** "Right away, searching for that now, sir — the latest headlines suggest AI is, once again, taking over everything."

> **User:** "Send an email to my colleague."
> **Sri:** "I shall require the recipient's email address, a subject, and the body of the message — do try to be thorough."

---

## 📋 Requirements

- Python 3.10+
- A LiveKit server (cloud or self-hosted)
- Google Cloud account with Gemini API access
- Gmail account with [App Password](https://myaccount.google.com/apppasswords) enabled (2FA required)
- Serper.dev account for web search

---

## 🔒 Security Notes

- The `.env` file is excluded from version control — **do not push it to GitHub**
- Gmail authentication uses **App Passwords**, not your account password
- All API keys are loaded via environment variables using `python-dotenv`

---

## 📄 License

This project is open source. Feel free to fork, modify, and make Sri your own — though he may have opinions about your choices.
