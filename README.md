# Finance Tracker  
### Role-Based Personal Finance Management System  
Built with **Python · Flask · MySQL**

---

## Project Overview  
Finance Tracker is a full-stack web application designed for managing personal finances with role-based access control.  
The system supports three distinct user roles — Admin, Analyst, and User — each with dedicated dashboards and permissions. All financial data is stored in a **MySQL relational database**, and every action is logged through a per-user passbook system for transparency and auditability.

> ⚠️ **Note:** This project includes demo accounts for all three roles for evaluation and testing purposes. It is not intended for industry-level deployment.

---

## Key Features  
- Role-Based Authentication (Admin / Analyst / User)  
- Income & Expense Tracking  
- Automatic Passbook (Audit Log)  
- Monthly Financial Insights (Chart.js)  
- Admin Panel for User Management  
- Analyst Dashboard for Filtering & Reports  
- Responsive Dark-Themed UI  
- MySQL Database Backend  
- Environment Variable Configuration via `.env`

---

## User Roles & Permissions  
| Role     | Route       | Capabilities |
|----------|------------|-------------|
| Admin   | `/admin`   | Create, update, delete users |
| Analyst | `/analyst` | Filter and analyze transactions |
| User    | `/user`    | Manage personal transactions and view summary |

---

## Demo Accounts  
These accounts are pre-loaded for testing and evaluation purposes:

| Role    | Phone        | Password     |
|---------|-------------|--------------|
| Admin   | 9999999999  | admin123     |
| Analyst | 8888888888  | analyst123   |
| User    | 9876543210  | rohan123      |

---

## Project Structure  
```
finance_tracker/
│
├── app.py
├── .env
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── user.html
│   ├── admin.html
│   └── analyst.html
│
└── utils/
    ├── core.py
    ├── viewers.py
    ├── transactions.py
    ├── records_update.py
    └── filters.py
```

---

## Data Model  
Each user is stored as a record in the MySQL database:

| Field        | Type    | Description                  |
|-------------|---------|------------------------------|
| id          | INT     | Auto-incremented primary key |
| Name        | VARCHAR | Full name                    |
| DOB         | DATE    | Date of birth                |
| Phone       | VARCHAR | Unique login identifier      |
| Password    | VARCHAR | User password                |
| Role        | VARCHAR | admin / analyst / user       |

Transactions, summaries, and passbook entries are stored in related tables.

---

## Core Modules  

### core.py  
- MySQL connection setup  
- Passbook logging  
- Summary calculations  

### transactions.py  
- Add/Delete transactions  
- Automatic summary updates  

### records_update.py  
- Create, update, and delete users  

### viewers.py  
- Fetch transactions, summaries, and passbook  

### filters.py  
- Analyst-level filtering and reporting  

---

## API Routes
| Method   | Route                      | Role    | Description         |
| -------- | -------------------------- | ------- | ------------------- |
| GET/POST | `/`                        | All     | Login               |
| GET      | `/user`                    | User    | User dashboard      |
| POST     | `/add_transaction`         | User    | Add transaction     |
| GET      | `/delete_transaction/<id>` | User    | Delete transaction  |
| GET      | `/admin`                   | Admin   | Admin dashboard     |
| POST     | `/admin/create`            | Admin   | Create user         |
| POST     | `/admin/update`            | Admin   | Update user         |
| POST     | `/admin/delete`            | Admin   | Delete user         |
| GET      | `/analyst`                 | Analyst | Analyst dashboard   |
| POST     | `/filter`                  | Analyst | Filter transactions |
| GET      | `/logout`                  | All     | Logout              |

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- Flask

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd finance_tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=fdinance
DB_PORT=3306
SECRET_KEY=your_secret_key
```

### 4. Set Up the Database
Import your SQL schema:
```bash
mysql -u your_username -p fdinance < schema.sql
```

### 5. Run the App
```bash
python app.py
```
Application runs at:
```
http://127.0.0.1:5000
```

---

## UI & Design
- Dark theme with consistent styling  
- Clean typography using Google Fonts  
- Smooth animations and transitions  
- Chart.js integration for analytics  
- Responsive layout for different screen sizes  

---

## Design Decisions

### Passbook Logging
All actions are recorded to maintain a complete audit trail.

### Real-Time Summary
Summaries are recalculated after every transaction to ensure accuracy.

### Safe Deletion
User deletion requires matching Name, DOB, and Phone.

### Environment-Based Configuration
Sensitive credentials are managed via `.env` and never hardcoded or pushed to version control.

---

## Tech Stack
| Layer    | Technology        |
| -------- | ----------------- |
| Backend  | Python, Flask     |
| Frontend | HTML, CSS, Jinja2 |
| Database | MySQL             |
| Charts   | Chart.js          |
| Fonts    | Google Fonts      |

---

## Future Improvements
- Token-based authentication  
- Export reports (PDF/Excel)  
- Mobile application support  
- Enhanced role permissions  

---

## License
This project is developed for academic and internship submission purposes.

---

## Acknowledgment
Developed as part of a practical implementation of full-stack web development with Flask, focusing on financial tracking and role-based access control with a relational MySQL database backend.