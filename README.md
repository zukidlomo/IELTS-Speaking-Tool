# IELTS Speaking Test Simulation Tool

# DEMO VIDEO: https://drive.google.com/file/d/1ZUfhMnmESwiBJ4EqLema8trpi1s0wFte/view?usp=sharing

## Overview
This project is a real-time IELTS Speaking Test simulation tool. It helps users practice and improve their English-speaking skills while receiving feedback based on IELTS scoring criteria: Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, and Pronunciation. The tool is standalone and can run locally or on a hosted server.

### Key Features
- **Real-Time Transcription**: Uses Google Speech-to-Text API for live speech transcription.
- **Conversational AI**: OpenAI GPT-4 is integrated to simulate an IELTS examiner.
- **IELTS Scoring**: Provides detailed feedback and scores for user responses.
- **Session Modes**:
  - Practice Mode: Instant feedback after every response.
  - Test Mode: Full IELTS Speaking Test simulation with all three parts.
- **Custom Feedback**: Sentence corrections, vocabulary suggestions, and pronunciation tips.
- **PDF Report**: Detailed feedback and recommendations in a downloadable PDF.

---

## Setup

### Prerequisites
- Python 3.8+
- Google Cloud Speech-to-Text credentials
- OpenAI API key

### Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:zukidlomo/IELTS-Speaking-Tool.git
   cd IELTS-Speaking-Tool
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Setup Script**
   ```bash
   bash setup.sh
   ```

5. **Run the Tool**
   ```bash
   python main.py
   ```

---

## Usage

### Modes
1. **Practice Mode**:
   - Select "Practice" when prompted.
   - Answer questions and receive instant feedback.

2. **Test Mode**:
   - Select "Test" when prompted.
   - Go through the three parts of the IELTS Speaking Test.
   - Receive a detailed feedback report at the end.

---

## APIs Used

### 1. Google Cloud Speech-to-Text API
- **Purpose**: Transcribes speech to text in real time.
- **Integration**:
  - Configured to capture audio via a microphone.
  - Processes audio chunks and streams them to the API for transcription.

### 2. OpenAI GPT-4 API
- **Purpose**: Simulates an IELTS examiner and provides feedback.
- **Integration**:
  - Generates dynamic questions.
  - Evaluates user responses and provides scores with recommendations.

---

## Scoring System
### Categories:
1. **Fluency & Coherence**:
   - Measures timing, pauses, and logical flow.
   - Feedback includes recommendations for smoother delivery.
2. **Lexical Resource**:
   - Evaluates vocabulary richness and accuracy.
   - Suggests synonyms and advanced word usage.
3. **Grammatical Range & Accuracy**:
   - Assesses sentence structure and grammar.
   - Points out grammatical mistakes and corrections.
4. **Pronunciation**:
   - Analyzes clarity, stress, and phoneme accuracy.
   - Provides phoneme-level tips to improve pronunciation.

---

## Challenges Faced and Solutions

### 1. **Latency in Real-Time Transcription**
   - **Challenge**: Delays in transcription affected the conversational flow.
   - **Solution**: Optimized audio chunk size for faster processing without quality loss.

### 2. **Pronounciation Feedback**
   - **Challenge**: It was hard detecting pronounciation through text.
   - **Solution**: Used Google speech to text confidence scoring.

### 3. **Feedback Consistency**
   - **Challenge**: Ensuring consistent and actionable feedback for diverse responses.
   - **Solution**: Standardized the response evaluation prompts to align with IELTS criteria.

---

## Source Code Explanation

### Key Modules

#### 1. **`transcription.py`**
- Captures audio using the PyAudio library.
- Streams audio to the Google Speech-to-Text API for transcription.

#### 2. **`conversation.py`**
- Handles interaction with OpenAI GPT-4.
- Simulates IELTS examiner's questions and evaluates responses.

#### 3. **`main.py`**
- Orchestrates the entire application.
- Guides users through Practice Mode and Test Mode.
- Manages user interactions, feedback generation, and report creation.

---

## Documentation

### LLM Integration
- OpenAI GPT-4 is used to simulate an examiner and provide dynamic, personalized feedback.
- API calls are optimized with a temperature setting of `0.7` for creative yet consistent responses.

### Scoring Feedback
- Prompts include detailed scoring criteria to generate feedback aligned with IELTS standards.

### PDF Reports
- Feedback from all test sections is compiled into a structured PDF using a dedicated report generation module.

---



