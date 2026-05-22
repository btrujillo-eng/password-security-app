# password-security-app

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL running locally on port 5432

---

### Environment Variables

Create a `.env` file in the root of the project with the following variables:

```env
POSTGRESQL_DATABASE_URL=postgresql://postgres:your_password@localhost:5432/password_security_app
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### Backend

1. Create and activate the virtual environment:

```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requeriments.txt
```

3. Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`  
Interactive docs at `http://127.0.0.1:8000/docs`

---

### Frontend

1. Navigate to the frontend directory:

```bash
cd fronted/vite-project
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

---

### ⚠️ Important

Both servers must be running simultaneously for the app to work.
Open two terminals — one for the backend and one for the frontend.