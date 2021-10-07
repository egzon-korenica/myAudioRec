import sqlite3

def rows():
    conn = sqlite3.connect('qdas/site.db')
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date_posted), id, q1, q2, q3 FROM Questions")
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    rows()
