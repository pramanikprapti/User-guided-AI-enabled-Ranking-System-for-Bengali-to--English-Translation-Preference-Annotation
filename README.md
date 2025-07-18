## BD Bangla ➝ English Translation Ranker

An AI-powered application for automatically translating Bengali sentences into English, generating multiple candidate translations, and **ranking them** based on a user-provided reference using neural evaluation metrics. This tool is built for researchers and developers working on Bengali-English machine translation and large-scale data annotation.

---

## 🚀 Features

- 🔄 **Multi-Candidate Translation** using MarianMT
- 📊 **COMET-based Automatic Ranking** of translation quality
- 📥 Input: Bengali sentence + reference English translation
- 🧾 Output: Ranked English translations
- 💾 Local storage of translations in SQLite (`translations.db`)
- ⚙️ Fully local pipeline — **no API keys or external dependencies**

---

## 🧠 How It Works

1. **User inputs** a Bengali sentence and a reference English translation.
2. The system generates **multiple English translations** using MarianMT.
3. Translations are **scored using COMET** against the reference.
4. Results are **ranked and displayed** in the UI.
5. The data is stored locally for future reference.

---

## 🛠 Tech Stack

| Component    | Tool/Library                     |
|--------------|----------------------------------|
| UI           | [Streamlit](https://streamlit.io) |
| Translation  | [MarianMT (bn-en)](https://huggingface.co/Helsinki-NLP/opus-mt-bn-en) |
| Evaluation   | [COMET](https://github.com/Unbabel/COMET) |
| Storage      | SQLite (`sqlite3`)               |
| Language     | Python 3.8+                       |

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bd-bangla-en-ranker.git
   cd bd-bangla-en-ranker

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt


## Run the App
streamlit run app.py
Once running, open your browser at: http://localhost:8501

## Screenshots
![Screenshot 2025-01-13 133330](<img width="1600" height="673" alt="image" src="https://github.com/user-attachments/assets/327991a0-9517-42d7-b996-ea148e0854fb" />
)
![Screenshot 2025-01-13 133330](<img width="1516" height="658" alt="image" src="https://github.com/user-attachments/assets/cb794fca-ebca-4953-b5de-85b9325f2a4a" />
)
![Screenshot 2025-01-13 133330](<img width="1473" height="653" alt="image" src="https://github.com/user-attachments/assets/0d2b8914-eae2-40ba-9bec-cc5e86fc0b9b" />
)

📈 Use Case
This tool is particularly useful for:

🔬 NLP research and model evaluation

🏷️ Semi-automated translation annotation

🧪 Quality assessment in machine translation pipelines

📜 License
This project is licensed under the MIT License. Feel free to use, modify, and share it.

🙋 Author
Prapti Pramanik
NLP Developer | Bengali Language Tech Enthusiast








