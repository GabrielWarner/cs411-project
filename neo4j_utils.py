from neo4j import GraphDatabase

# 1. Configure your connection
_driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "12345678")
)

def _get_session():
    # explicitly target your Academic World database
    return _driver.session(database="academicworld")

def get_all_faculty():
    """Return a list of all faculty names, sorted alphabetically."""
    query = "MATCH (f:FACULTY) RETURN f.name AS name ORDER BY name"
    with _get_session() as session:
        result = session.run(query)
        return [record["name"] for record in result]

def get_faculty_profile(name: str):
    """Return a dict with name, position, photoUrl for one faculty member."""
    query = """
    MATCH (f:FACULTY {name: $name})
    RETURN f.name AS name, f.position AS position, f.photoUrl AS photoUrl
    """
    with _get_session() as session:
        rec = session.run(query, name=name).single()
        if not rec:
            return None
        return {
            "name":     rec["name"],
            "position": rec["position"],
            "photoUrl": rec["photoUrl"]
        }

def get_top_coauthors(faculty_name: str, limit: int = 5):
    """
    Returns a list of (coauthor_name, joint_publications) tuples for the
    top collaborators of the given faculty member.
    """
    query = """
    MATCH (f:FACULTY {name: $name})-[:PUBLISH]->(:PUBLICATION)<-[:PUBLISH]-(co:FACULTY)
    RETURN co.name AS coauthor, COUNT(*) AS jointCount
    ORDER BY jointCount DESC
    LIMIT $limit
    """
    with _get_session() as session:
        result = session.run(query, name=faculty_name, limit=limit)
        return [(r["coauthor"], r["jointCount"]) for r in result]