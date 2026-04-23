# MySQL PoC

A minimal Flask app that stores text input to MySQL and displays it as JSON or HTML.

## Project Structure

```
poc/
├── app.py            # Flask backend
├── requirements.txt  # Python deps
├── setup.sql         # MySQL setup
└── templates/
    ├── index.html    # Main input UI
    └── entries.html  # HTML view of entries
```

## Setup

### 1. Install MySQL (if needed)
```bash
sudo apt install mysql-server
sudo systemctl start mysql
```

### 2. Set up the database
```bash
sudo mysql -u root < setup.sql
# Or interactively:
sudo mysql -u root -p < setup.sql
```

### 3. Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

Open http://localhost:5000

## Endpoints

| Route            | Method | Description                        |
|------------------|--------|------------------------------------|
| `/`              | GET    | Main input UI                      |
| `/submit`        | POST   | Save entry to MySQL (JSON body)    |
| `/entries/json`  | GET    | Return all entries as JSON         |
| `/entries/html`  | GET    | Display all entries as HTML table  |

## Environment Variables (optional overrides)

| Variable   | Default       |
|------------|---------------|
| DB_HOST    | localhost     |
| DB_USER    | poc_user      |
| DB_PASS    | poc_password  |
| DB_NAME    | poc_db        |

Example:
```bash
DB_USER=myuser DB_PASS=mypass python app.py
```
