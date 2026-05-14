from utils.core import get_conn, get_summary


def view_transactions(user_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def view_passbook(user_id):
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        "SELECT * FROM passbook WHERE user_id = %s ORDER BY timestamp DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def view_summary(user_id):
    return get_summary(user_id)
