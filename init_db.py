from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "12345678")
)

def create_faculty(tx, name, position, photoUrl):
    tx.run("""
        CREATE (f:FACULTY {name: $name, position: $position, photoUrl: $photoUrl})
    """, name=name, position=position, photoUrl=photoUrl)

def main():
    with driver.session() as session:
        session.run("MATCH (n:FACULTY) DETACH DELETE n")
        
        for faculty in faculty_data:
            session.execute_write(create_faculty, 
                                faculty["name"], 
                                faculty["position"], 
                                faculty["photoUrl"])
        
        print("Database initialized with faculty data")

if __name__ == "__main__":
    main()
    driver.close()