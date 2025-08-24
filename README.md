# 📝 Journal App with Qdrant Search

A simple Django application to create, update, delete, and search journal entries.
The app integrates with **Qdrant Vector Database** for semantic search functionality.

---

## 🚀 Features

* Create, update, and delete journal entries
* Store entries in **SQLite**
* Vectorize and upsert entries into **Qdrant** for semantic search
* Search entries using natural language queries
* Simple web interface for managing entries

---

## Demo
![Demo](Journal-app-demo.gif)

---

## 🛠️ Tech Stack

* **Backend:** Django
* **Database:** SQLite
* **Vector DB:** Qdrant
* **Frontend:** Django templates + Tailwind

---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/journal-app.git
cd advanced-journal-app
```

### 2. Create & activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

fill up the config with appropriate values
Huggingface token is required for embedding model

```env
QDRANT_URL=http://qdrant:6333
QDRANT_COLLECTION=journal_entries
HF_TOKEN=your_huggingface_token_here
DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_DEBUG=True
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Qdrant

If running via Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or use a managed Qdrant instance.

### 7. Run the app

```bash
python manage.py runserver
```

Visit: 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔍 Usage

* **Create an entry:** Add new journal entries from the UI
* **Update an entry:** Edit existing entries
* **Delete an entry:** Removes from both DB and Qdrant
* **Search:** Use the search bar to query entries semantically

---

## 📌 Future Enhancements

* Authentication (user-specific journals)
* Tagging and categorization
* API endpoints for external apps

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add new feature"`)
4. Push branch (`git push origin feature-name`)
5. Open a Pull Request

---

## 📜 License

MIT License.

---
