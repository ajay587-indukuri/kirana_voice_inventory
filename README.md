# ManaKirana AI 🛒
### AI-Powered Voice-Based Inventory & Grocery Management

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)](https://flask.palletsprojects.com/)
[![Gnani AI](https://img.shields.io/badge/STT-Gnani%20Prisma%20v3.0-orange.svg)](https://gnani.ai/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%20v1beta-8E75B2.svg)](https://ai.google.dev/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Vercel-black.svg)](https://vercel.com/)
[![Demo Video](https://img.shields.io/badge/Demo%20Video-Google%20Drive-E53935.svg?logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1zKFwkYEx4VQrbj8Z9kZml78_npoQXGl_/view?usp=sharing)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

> **Great Indian AI Internship Challenge Submission — Gnani AI**  
> **Vision:** Making neighbourhood kirana stores smarter through regional voice AI and automation.  
> 🎥 **Demo Video:** [**Watch Live Video Demonstration**](https://drive.google.com/file/d/1zKFwkYEx4VQrbj8Z9kZml78_npoQXGl_/view?usp=sharing)  
> 📄 **Complete Solution Blueprint:** Detailed challenge vision, problem analysis, and architectural roadmap available in [**solution.md**](solution.md).

---

## 📑 Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Problem Statement](#2-problem-statement)
- [3. Proposed Solution](#3-proposed-solution)
- [4. Key Capabilities](#4-key-capabilities)
- [5. System Architecture & Workflow](#5-system-architecture--workflow)
- [6. Technology Stack](#6-technology-stack)
- [7. Project Structure](#7-project-structure)
- [8. Installation & Setup](#8-installation--setup)
- [9. Deployment (Vercel)](#9-deployment-vercel)
- [10. Challenge Deliverables](#10-challenge-deliverables)

---

## 1. Project Overview

**ManaKirana AI** is a regional-language voice ordering and smart cart management platform designed specifically for Indian neighbourhood grocery (*kirana*) stores.

Local shopkeepers and customers interact naturally in **Telugu**, **Tanglish**, or **English**. The platform captures spoken voice orders via microphone or audio upload, transcribes the speech with **Gnani AI Prisma STT**, extracts structured grocery items and quantities using **Google Gemini AI**, and automatically populates an interactive, editable cart with pre-saved shopkeeper price presets.

---

## 2. Problem Statement

Across India, millions of traditional kirana stores manage customer orders, inventory pricing, and billing manually on paper slips. This presents several operational bottlenecks:
- **Language & Literacy Barriers:** Conversational orders are spoken in local regional dialects (e.g., Telugu), making manual transcription tedious.
- **Ambiguous Quantities & Units:** Spoken quantities (e.g., *"రెండు కిలోలు"*, *"అర లీటర్"*, *"ఒక ప్యాకెట్"*) are prone to mishearing or calculation errors.
- **Time-Consuming Billing:** Shopkeepers must repeatedly recall unit prices, manually multiply quantities, and tally grand totals during peak rush hours.
- **Inventory & Pricing Mismatches:** Lack of instant price presets leads to inconsistent billing and lost store margins.

For full problem breakdown, see [**solution.md**](solution.md#problem).

---

## 3. Proposed Solution

ManaKirana AI bridges traditional Indian retail with modern voice AI by providing:
1. **Hands-Free Voice Ordering:** One-tap microphone recording directly in the browser with live recording timer and playback preview.
2. **High-Accuracy Telugu STT:** Grounded transcription powered by **Gnani AI Prisma** (`te-IN`), recognizing colloquial grocery names.
3. **Structured Entity Extraction:** **Google Gemini** converts spoken transcripts into validated JSON objects with normalized units and null-safe quantity validation.
4. **Editable Smart Cart:** Live subtotal and grand total recalculation with focus-preserving inputs.
5. **Shopkeeper Price Presets:** Local catalog auto-fill that remembers custom store pricing for staple goods across sessions.

Read the complete vision in [**solution.md**](solution.md#proposed-solution).

---

## 4. Key Capabilities

| Feature | Description |
| :--- | :--- |
| 🎙️ **Live Mic Recording** | In-browser MediaRecorder audio capture with pulsing record indicator, live timer (`00:00`), and instant playback preview. |
| 📁 **Multi-Format Upload** | Supports `.m4a`, `.wav`, `.mp3`, `.ogg`, `.flac`, and `.webm` with automatic 16 kHz conversion via `imageio-ffmpeg`. |
| 🗣️ **Prisma Speech-to-Text** | Integrates Gnani's speech recognition engine optimized for Indian English and Telugu regional accents. |
| 🧠 **Gemini Order Understanding** | Uses structured response schemas (`v1beta`) to extract product names, quantities, normalized units, and clarifications. |
| 🛒 **Interactive Editable Cart** | Add, edit, or remove items on the fly. Real-time subtotal & grand total calculation without losing input focus. |
| 💾 **Shopkeeper Price Presets** | Saves unit prices to browser `localStorage` for automatic auto-filling on future customer orders. |
| 📋 **Preset Catalogue Drawer** | Preloaded with 30+ staple Indian grocery items (both in English and Telugu) with one-click restore to defaults. |
| ☁️ **Serverless Ready** | Fully optimized for Vercel deployment with zero external FFmpeg binary installation requirements. |

---

## 5. System Architecture & Workflow

```text
       ┌───────────────────────────────┐
       │   Customer / Shopkeeper Voice │
       │     (Telugu / Tanglish / Eng) │
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │   Browser MediaRecorder / Mic │
       │   (WebM / M4A / WAV Upload)   │
       └──────────────┬────────────────┘
                      │ POST /transcribe
                      ▼
       ┌───────────────────────────────┐
       │     Flask Backend (api.py)    │
       │   FFmpeg 16kHz Audio Stream   │
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │     Gnani AI Prisma (STT)     │
       │    Telugu Speech Recognition  │
       └──────────────┬────────────────┘
                      │ Telugu Transcript
                      ▼
       ┌───────────────────────────────┐
       │    Google Gemini (v1beta)     │
       │  Structured JSON Order Schema │
       └──────────────┬────────────────┘
                      │ Extracted Items JSON
                      ▼
       ┌───────────────────────────────┐
       │    Interactive Grocery Cart   │
       │  Auto-filled Price Presets    │
       │  Live Subtotals & Total (₹)   │
       └───────────────────────────────┘
```

---

## 6. Technology Stack

- **Backend:** Python 3.10+, Flask 3.1
- **Speech Recognition:** Gnani AI Prisma STT (`gnani-vachana` SDK)
- **Generative AI:** Google GenAI SDK (`google-genai` v1beta)
- **Audio Processing:** `imageio-ffmpeg` (bundled static FFmpeg binary)
- **Frontend:** Vanilla HTML5, CSS3 (CSS Variables, Flexbox, Keyframe Animations), JavaScript (ES6+, Web Audio / MediaRecorder API)
- **Storage & State:** HTML5 `localStorage` (Shopkeeper Price Presets)
- **Deployment:** Vercel Serverless Functions

---

## 7. Project Structure

```text
ManaKirana-AI/
├── api.py              # Gnani STT client, FFmpeg PATH configuration & Gemini extraction
├── app.py              # Flask server routes (/transcribe, /extract, /)
├── requirements.txt    # Production dependencies (Flask, gnani-vachana, google-genai, imageio-ffmpeg)
├── solution.md         # Official Challenge Solution Blueprint & Roadmap
├── README.md           # Project documentation & setup guide
├── .gitignore          # Keeps secrets (.env) and cache out of git
├── telugu_order.m4a    # Sample Telugu audio order for testing
└── templates/
    └── index.html      # Responsive UI with Live Mic, Transcript & Editable Cart
```

---

## 8. Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/ajay587-indukuri/kirana_voice_inventory.git
cd kirana_voice_inventory
```

### 2. Create virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the root directory:
```env
GNANI_API_KEY=your_gnani_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run locally
```bash
python3 app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 9. Deployment (Vercel)

This repository includes bundled `imageio-ffmpeg` and relative path configuration for zero-dependency Vercel deployment:

1. Push your repository to GitHub.
2. Import the project in your [Vercel Dashboard](https://vercel.com/).
3. Add your Environment Variables under **Settings > Environment Variables**:
   - `GNANI_API_KEY`: Your Gnani Prisma API key.
   - `GEMINI_API_KEY`: Your Google Gemini API key.
4. Deploy! Vercel will install dependencies and serve the Flask application automatically.

---

## 10. Challenge Deliverables

- 🎥 **Video Demonstration:** [**Watch Live Demo on Google Drive**](https://drive.google.com/file/d/1zKFwkYEx4VQrbj8Z9kZml78_npoQXGl_/view?usp=sharing)
- 📄 **Vision & Specification:** [**solution.md**](solution.md)
- 🎙️ **Sample Audio File:** [`telugu_order.m4a`](telugu_order.m4a)
- 💻 **Live Application Code:** [`app.py`](app.py), [`api.py`](api.py), [`templates/index.html`](templates/index.html)

**Built with ❤️ for the Great Indian AI Internship Challenge by Gnani AI.**