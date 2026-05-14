from utils.core import get_conn


def filter_transactions(user_id, start_date=None, end_date=None, category=None, txn_type=None):
    conn   = get_conn()
    cur    = conn.cursor()

    query  = "SELECT * FROM transactions WHERE user_id = %s"
    params = [user_id]

    if start_date:
        query += " AND date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND date <= %s"
        params.append(end_date)

    if category and category.strip():
        query += " AND LOWER(category) = LOWER(%s)"
        params.append(category.strip())

    if txn_type and txn_type.strip():
        query += " AND LOWER(type) = LOWER(%s)"
        params.append(txn_type.strip())

    query += " ORDER BY date DESC"

    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def filter_summary(txns):
    if not txns:
        return {"TotalIncome": 0, "TotalExpense": 0, "Balance": 0}

    total_income  = sum(float(t["amount"]) for t in txns if t["type"].lower() == "income")
    total_expense = sum(float(t["amount"]) for t in txns if t["type"].lower() == "expense")

    return {
        "TotalIncome":  total_income,
        "TotalExpense": total_expense,
        "Balance":      total_income - total_expense
    }
