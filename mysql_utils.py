import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="academicworld"
    )
    try:
        yield conn
    finally:
        conn.close()

def get_publications_per_year(faculty_name: str):
    """
    Returns a list of (year, count) for how many papers that faculty member has per year.
    """
    with get_db_connection() as conn:
        query = """
        SELECT p.year AS yr, COUNT(*) AS cnt
        FROM publication p
          JOIN faculty_publication fp ON p.id = fp.publication_id
          JOIN faculty f ON fp.faculty_id = f.id
        WHERE f.name = %s
        GROUP BY p.year
        ORDER BY p.year
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query, (faculty_name,))
            return cursor.fetchall()
        finally:
            cursor.close()

def get_top_institutes(limit: int = 10):
    """
    Returns a list of (institute_name, pub_count) tuples for the top institutes
    by total faculty publications.
    """
    with get_db_connection() as conn:
        query = """
        SELECT u.name AS inst, COUNT(*) AS cnt
        FROM university u
          JOIN faculty f ON f.university_id = u.id
          JOIN faculty_publication fp ON fp.faculty_id = f.id
          JOIN publication p ON p.id = fp.publication_id
        GROUP BY u.name
        ORDER BY cnt DESC
        LIMIT %s
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        finally:
            cursor.close()