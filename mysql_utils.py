import mysql.connector
from contextlib import contextmanager
from config import MYSQL_CONFIG

@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
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

def get_papers_for_faculty(faculty_name: str):
    """
    Returns a list of (paper_id, title) tuples for a given faculty member.
    """
    with get_db_connection() as conn:
        query = """
        SELECT p.id, p.title
        FROM publication p
          JOIN faculty_publication fp ON p.id = fp.publication_id
          JOIN faculty f ON fp.faculty_id = f.id
        WHERE f.name = %s
        ORDER BY p.year DESC, p.title
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query, (faculty_name,))
            results = cursor.fetchall()
            print(f"Paper IDs and titles: {results}")
            return results
        finally:
            cursor.close()

def mark_reviewed(paper_id):
    """
    Mark a paper as reviewed.
    """
    print(f"Attempting to mark paper_id: {paper_id} (type: {type(paper_id)})")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Create table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS reviewed_papers (
                paper_id VARCHAR(255) PRIMARY KEY,
                faculty_id INT,
                reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (faculty_id) REFERENCES faculty(id)
            )
            """
            cursor.execute(create_table_query)

            # Get faculty_id for the current paper
            get_faculty_query = """
            SELECT DISTINCT f.id 
            FROM faculty f
            JOIN faculty_publication fp ON f.id = fp.faculty_id
            WHERE fp.publication_id = %s
            LIMIT 1
            """
            cursor.execute(get_faculty_query, (str(paper_id),))
            faculty_id = cursor.fetchone()[0]

            insert_query = """
            INSERT INTO reviewed_papers (paper_id, faculty_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE reviewed_at = CURRENT_TIMESTAMP
            """
            cursor.execute(insert_query, (str(paper_id), faculty_id))
            conn.commit()
        finally:
            cursor.close()

def get_reviewed_papers_for_faculty(faculty_name: str):
    """
    Returns a list of paper IDs that have been reviewed for a given faculty.
    """
    with get_db_connection() as conn:
        query = """
        SELECT DISTINCT rp.paper_id, rp.reviewed_at
        FROM reviewed_papers rp
        JOIN faculty f ON f.id = rp.faculty_id
        WHERE f.name = %s
        ORDER BY rp.reviewed_at DESC
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query, (faculty_name,))
            results = [row[0] for row in cursor.fetchall()]  # Only take the paper_id from the result
            print(f"Retrieved reviewed paper IDs for {faculty_name}: {results}")
            return results
        finally:
            cursor.close()