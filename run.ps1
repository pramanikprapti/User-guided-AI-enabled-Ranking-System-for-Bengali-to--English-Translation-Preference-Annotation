# -------------------------------------------
#  run.ps1 - Start FastAPI server
# -------------------------------------------

# 1️⃣ Move to your project folder
cd D:\chatbotlangchain

# 2️⃣ Activate virtual environment
.\venv310\Scripts\Activate.ps1

# 3️⃣ Start FastAPI server with uvicorn
uvicorn api.app:app --reload --host 127.0.0.1 --port 8000
