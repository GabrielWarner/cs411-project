import mysql.connector
import os

_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="academicworld"
)

def get_publications_per_year(faculty_name: str):
    """
    Returns a list of (year, count) for how many papers that faculty member has per year.
    """
    query = """
    SELECT p.year AS yr, COUNT(*) AS cnt
    FROM publication p
      JOIN faculty_publication fp ON p.id = fp.publication_id
      JOIN faculty f ON fp.faculty_id = f.id
    WHERE f.name = %s
    GROUP BY p.year
    ORDER BY p.year
    """
    cursor = _conn.cursor()
    cursor.execute(query, (faculty_name,))
    results = cursor.fetchall()
    cursor.close()
    return results