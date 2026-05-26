# 🔬 PaperMind AI Canvas 

> **An Academic Abstract Summarizer & Keyword Tagging Canvas built with Python and Gemini 2.5 Flash.**

PaperMind AI Canvas is a desktop productivity application designed for researchers and students to instantly conquer dense academic literature (such as dMRI, stroke studies, and medical imaging papers). By simply pasting an abstract, the application leverages **Gemini 2.5 Flash's Structured Outputs API** to dissect complex texts into a beautiful, macaron-colored structural grid within 10 seconds.

---

## ✨ Key Features

* **⚡ AI-Powered Structured Insight**: Enforces Gemini to return a strict Pydantic JSON schema, slicing literature into 4 core sections: *Research Objectives*, *Core Methods*, *Key Metrics/Results*, and *Future Challenges*.
* **🏷️ Intelligent Keyword Tagging**: Automatically extracts domain-specific keywords and renders them in a flowing, text-wrapped visual tag wall (never missing a tag due to window boundaries).
* **🎨 Macaron Dopamine Aesthetic**: Built with a sleek CustomTkinter light-purple theme (`#C69FD5`) paired with a cozy handwritten font styling to reduce academic reading fatigue.
* **🧩 Production-Ready Defenses**: Embedded anti-crash logic for alpha-channel image handling, automated `state="disabled"` UI throttling during active API streams, and zero-flicker frame refreshing.

---

## 🛠️ Tech Stack & Architecture

* **GUI Framework**: `CustomTkinter` (Python 3.10+)
* **LLM Core Engine**: `google-genai` (Official 2025 Google SDK)
* **AI Model**: `gemini-2.5-flash` (Optimized with structured response schema and low temperature for empirical accuracy)
* **JSON Enforcement**: `Pydantic` validation

---

<img width="1221" height="747" alt="image" src="https://github.com/user-attachments/assets/429cb7bf-7fda-4de7-a24b-e0e381003909" />


## 🚀 Getting Started

### Prerequisites

Ensure you have a modern Python environment and your Google AI Studio API Key ready.

```
pip install customtkinter google-genai pydantic pillow
```
### Gemini API
Goto [website (https://aistudio.google.com/)][website] apply a free Gemini API. Then copy the API key and paste in the line 53.


## Run the App
Clone this repository, navigate to the directory, and boot the application:

```python papermind_ai_canvas.py```
