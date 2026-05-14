import pymysql
import pymysql.cursors
pymysql.install_as_MySQLdb()
import os
from dotenv import load_dotenv
# ------------------------------------------------------------
# Update these credentials to match your MySQL setup
# ------------------------------------------------------------
load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port":     int(os.getenv("DB_PORT", 3306))
}
def get_conn():
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)


# ------------------------------------------------------------
# PASSBOOK / AUDIT LOG
# ------------------------------------------------------------

def log_action(user_id, action, details=""):
    """Insert a passbook entry and nothing else."""
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO passbook (user_id, action, details) VALUES (%s, %s, %s)",
        (user_id, action, details)
    )
    conn.commit()
    cur.close()
    conn.close()


def recent_transactions(user_id, n=5):
    """Return the last n passbook entries for a user."""
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "SELECT * FROM passbook WHERE user_id = %s ORDER BY timestamp DESC LIMIT %s",
        (user_id, n)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ------------------------------------------------------------
# SUMMARY  (computed live from transactions table)
# ------------------------------------------------------------

def get_summary(user_id):
    conn = get_conn()
    cur  = conn.cursor()

    # totals
    cur.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'Income'  THEN amount ELSE 0 END), 0) AS TotalIncome,
            COALESCE(SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END), 0) AS TotalExpense
        FROM transactions
        WHERE user_id = %s
    """, (user_id,))
    totals = cur.fetchone()
    totals["CurrentBalance"] = totals["TotalIncome"] - totals["TotalExpense"]

    # category breakdown
    cur.execute("""
        SELECT category,
               SUM(CASE WHEN type = 'Income'  THEN  amount ELSE 0 END) -
               SUM(CASE WHEN type = 'Expense' THEN  amount ELSE 0 END) AS net
        FROM transactions
        WHERE user_id = %s
        GROUP BY category
    """, (user_id,))
    totals["CategoryBreakdown"] = {r["category"]: float(r["net"]) for r in cur.fetchall()}

    # monthly totals
    cur.execute("""
        SELECT DATE_FORMAT(date, '%%Y-%%m') AS month,
               SUM(CASE WHEN type = 'Income'  THEN  amount ELSE 0 END) -
               SUM(CASE WHEN type = 'Expense' THEN  amount ELSE 0 END) AS net
        FROM transactions
        WHERE user_id = %s
        GROUP BY month
        ORDER BY month
    """, (user_id,))
    totals["MonthlyTotals"] = {r["month"]: float(r["net"]) for r in cur.fetchall()}

    cur.close()
    conn.close()
    return totals


# ------------------------------------------------------------
# USER LOOKUP  (used by login + every route)
# ------------------------------------------------------------

def get_user_by_phone(phone):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM users WHERE phone = %s", (phone,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def get_all_users():
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users
