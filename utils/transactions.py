from utils.core import get_conn, log_action


def new_transaction(user_id, category, amount, notes, txn_type, date):
    amount = abs(amount)  # always store positive; type column carries direction

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO transactions (user_id, amount, type, category, date, notes)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (user_id, amount, txn_type, category, date, notes)
    )
    conn.commit()
    txn_id = cur.lastrowid
    cur.close()
    conn.close()

    log_action(user_id, "Transaction Added", f"{txn_type} of {amount} in {category}")
    return txn_id


def delete_transaction(user_id, txn_id):
    conn = get_conn()
    cur  = conn.cursor()

    # fetch before deleting so we can log meaningful details
    cur.execute("SELECT * FROM transactions WHERE id = %s AND user_id = %s", (txn_id, user_id))
    txn = cur.fetchone()

    if not txn:
        cur.close()
        conn.close()
        return False

    cur.execute("DELETE FROM transactions WHERE id = %s", (txn_id,))
    conn.commit()
    cur.close()
    conn.close()

    log_action(user_id, "Transaction Deleted",
               f"Removed {txn['type']} of {txn['amount']} in {txn['category']} on {txn['date']}")
    return True
