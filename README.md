# 🧘 MindY - AI-Powered Wellness Assistant 🎥✨

MindY is a GPT-4 powered assistant designed to provide **personalized wellness techniques** and **top YouTube video recommendations** based on user queries.

This project integrates **YouTube metadata retrieval** and **natural language processing (NLP)** with **TF-IDF vectorization** and **cosine similarity** to rank and recommend relevant relaxation and mindfulness content.

---

## Context & Intent

MindY is a concept and exploration project developed as part of a learning journey.
Its purpose is to explore human-centered questions around how people search for and engage with mindfulness and relaxation content, rather than to deliver a production-ready tool.

The project focuses on experimentation, reflection, and design considerations, with attention to language, intent, and ethical use of technology in wellbeing contexts.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [How It Works](#-how-it-works)
4. [Project Structure](#-project-structure)
5. [Requirements](#-requirements)
6. [Usage](#-usage)
7. [Why This System?](#-why-this-system)
8. [Next Steps](#-next-steps)

---

## 📖 Project Overview

MindY consists of **two core functionalities**:

1. **🧠 AI-Powered Chatbot for Personalized Techniques**
   - Uses **GPT-4** to generate **actionable wellness techniques** based on user queries.
   - Allows users to select **wellness categories** for more refined recommendations.

2. **🎥 Intelligent YouTube Video Search**
   - Retrieves **relevant wellness videos** from YouTube API.
   - **Ranks videos by semantic similarity** using **TF-IDF & cosine similarity**.
   - Ensures users get **high-quality, meaningful** video recommendations.

---

## ✨ Key Features

### 🎯 Personalized Recommendations  
- Uses **GPT-4** to suggest **specific techniques** tailored to user queries.  
- Example: A query like _"How can I reduce stress?"_ may generate:
  - **Guided Breathing Exercise**
  - **Mindfulness Meditation for Anxiety Relief**  

### 🔍 Smart Video Search  
- Queries **YouTube API** and **ranks videos** by similarity to the user's query.  
- Prevents generic recommendations by **matching video descriptions to techniques**.

### 📂 Category-Based Suggestions  
- Users can select **predefined wellness categories**, such as:
  - 🧘 **Mindfulness & Meditation**
  - 💨 **Breathing Exercises**
  - 🤸 **Somatic Practices**

---

## 🤔 How It Works

### **Query Processing Pipeline**

1. **💬 User Input**
   - The app collects a query (e.g., _"How do I sleep better?"_).
   - If a **category** is selected, the response is focused on that domain.

2. **🧠 AI Response Generation**
   - GPT-4 generates a **personalized list of techniques**.
   - Extracts **keywords and themes** from the response.

3. **🔗 YouTube Search & Ranking**
   - The system queries **YouTube API** for videos using **refined keywords**.
   - Uses **TF-IDF & cosine similarity** to **re-rank** videos based on relevance.

4. **📜 Results Display**
   - The app presents **AI-generated techniques** alongside **top-ranked videos**.

---

## 📂 Project Structure
### **Key Files & Directories**
- **`app.py`** → Main Streamlit app (chatbot & video recommendations)
- **`requirements/`** → Contains dependencies for different functionalities:
  - `mindy_app.txt` → Dependencies for Streamlit app
  - `genai.txt` → Dependencies for query simulation & clustering
  - `nlp.txt` → Dependencies for data analysis
- **`simulate_queries/`** → Query simulations & GPT data extraction
  - Contains the following key files:
    - **`app_logic.py`**: Implements core logic for GPT-4 recommendations, YouTube video fetching, ranking, and query processing.  
    - **`simulate_queries.py`**: Automates the simulation of user queries using `app_logic.py` to extract GPT-recommended techniques and descriptions. Outputs results to `simulation_results.csv`.
- **`data_analysis/`** → NLP analysis & clustering scripts:
  - Contains scripts for text preprocessing, clustering, and visualization of results.  
  - Includes `simulated_results.csv`, which holds the output of simulated user queries for analysis.
- **`MindyPresentation.pdf`** → Project presentation
- **`README.md`** → Project documentation

---

## ⚙️ Requirements

1. **API Keys**:
   - **YouTube API Key** (store your Key in a `.env` file as `YOUTUBE_API_KEY`).
   - **OpenAI API Key** (store your Key in the `.env` file as `OPENAI_API_KEY`).

2. **Dependencies**:
   - Python libraries: `streamlit`, `openai`, `scikit-learn`, `google-api-python-client`, `python-dotenv`.

3. **Install Dependencies**:
   - To keep dependencies isolated and avoid conflicts, create separate virtual environments for each functional area.
     
   #### 🟢 MindY App (Streamlit)
   1. **Create a virtual environment** for the Streamlit app:
   ```bash
   python3 -m venv mindy_app_env
   source mindy_app_env/bin/activate  # On Windows, use mindy_app_env\Scripts\activate
   ```
   
   2. **Install the dependencies**:
   ```bash
   pip install -r requirements/mindy_requirements.txt
   ```

   ### 🟡 Simulating Queries (GPT Data Extraction & Clustering)
  
   1. **Create a virtual environment** for query simulation and clustering:
   ```bash
   python3 -m venv genai_env
   source genai_env/bin/activate  # On Windows, use genai_env\Scripts\activate
   ```

   2. **Install the dependencies**:
   ```bash
   pip install -r requirements/genai.txt
   ```

   ### 🔵 Data Analysis (Clustering & NLP Processing)
   1. **Create a virtual environment** for data analysis:
   ```bash
   python3 -m venv nlp_env
   source nlp_env/bin/activate  # On Windows, use nlp_env\Scripts\activate
   ```

   2. **Install the dependencies**:
   ```bash
   pip install -r requirements/nlp.txt
   ```

---

## 🚀 Usage

  ### 1️⃣ Run the Application
  - Activate the virtual environment for the MindY App:
  ```bash
  source mindy_app.env/bin/activate  # On Windows: mindy_app.env\Scripts\activate
  ```

  - Launch the chatbot and video recommender:
  ```bash
  streamlit run app.py
  ```

  ### 2️⃣ Input Queries
  - Enter a **wellness-related query** (e.g., *"How can I improve my focus?"*).
  - Optionally, **select a category** for more refined suggestions.

  ### 3️⃣ View AI-Powered Recommendations
  - The app displays **customized techniques** & **top-ranked YouTube videos**.

---

## ❓ Why This System?

### ✅ Traditional YouTube searches lack personalization.
This system improves recommendations by:
- 🎯 **Understanding query intent** (semantic search, not just keywords).
- 🛠️ **Filtering & ranking** YouTube videos for better quality.
- 💡 **Providing AI-powered guidance**, not just links.

---

## 🛠️ Next Steps

### 🚀 Integrate Clusters into GPT’s Workflow
- Leverage clustered techniques to provide more cohesive recommendations.
- Map user queries to cluster themes for more personalized outputs.

### 🔧 Enhance Query Preprocessing
- Improve text preprocessing by refining techniques like removing stop words and applying lemmatization.

### 🎯 Refine Prompt Design
- Shift from a narrow focus on Mindfulness and Relaxation to a broader range of well-being areas.
- Expand prompts to include diverse domains like emotional management and cognitive behavioral therapy (CBT).

### 📚 Broaden Categories
- Introduce new categories (e.g., journaling prompts) to generate more varied and meaningful recommendations.

### 💡 Experiment with Free Models
- Simulate queries using a generalized system, testing a free model like **DeepSeek**.

### 🔄 Evaluate Clustering Impact
- Repeat clustering processes and analyze how the new implementations influence results.
