from utils.core import get_conn, log_action


def new_person(name, dob, phone, password, db=None):
    """db param kept for API compatibility but ignored — MySQL is the source of truth."""
    conn = get_conn()
    cur  = conn.cursor()

    cur.execute("SELECT id FROM users WHERE phone = %s", (phone,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return "User already exists"

    cur.execute(
        "INSERT INTO users (name, dob, phone, password, role) VALUES (%s, %s, %s, %s, %s)",
        (name, dob, phone, password, "user")
    )
    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()

    log_action(user_id, "Person Created", f"{name} registered")
    return user_id


def update_records(field, new_value, user_id, db=None):
    field_map = {"name": "name", "dob": "dob", "phone_number": "phone"}
    col = field_map.get(field.lower())

    if not col:
        return False

    conn = get_conn()
    cur  = conn.cursor()
    cur.execute(f"UPDATE users SET {col} = %s WHERE id = %s", (new_value, user_id))
    conn.commit()
    cur.close()
    conn.close()

    log_action(user_id, "Person Updated", f"{col} changed to {new_value}")
    return True


def delete_person(name, dob, phone, db=None):
    conn = get_conn()
    cur  = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE name = %s AND dob = %s AND phone = %s",
        (name, dob, phone)
    )
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return False

    user_id = user["id"]
    log_action(user_id, "Person Deleted", f"{name} with DOB {dob} and phone {phone} deleted")

    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True
