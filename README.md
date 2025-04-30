# Title
Academic Research Explorer

## Purpose
**Scenario:** Department chairs and librarians need a unified dashboard to explore faculty publication data from the Academic World dataset.

**Target Users:** Chairs, deans, research coordinators, and librarians managing faculty research outputs.

**Objectives:**
- Inspect individual faculty profiles and publication records
- Visualize co-author networks and annual publication trends
- Add private notes and mark papers as reviewed for personal tracking

## Demo
Watch the 5–10 minute video demo here: 

## Installation
1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/GabrielWarner/cs411-project
   cd cs411-project
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the following databases are populated with the Academic World data and running locally:
   - **Neo4j** at bolt://localhost:7687
   - **MongoDB** at mongodb://localhost:27017
   - **MySQL** at localhost:3306
5. Update credentials in `neo4j_utils.py`, `mongodb_utils.py`, and `mysql_utils.py` as needed.
6. Launch the dashboard:
   ```bash
   python app.py
   ```
7. Open your browser to http://127.0.0.1:8051

## Usage
1. Select a faculty member from the centered dropdown.
2. View their profile card and top 5 co-author chart.
3. Read or add personal notes in the "Faculty Notes" widget.
4. Observe yearly publication trends in the line chart.
5. Review top 10 institutes by publication count.
6. Mark individual papers as reviewed and see your reviewed list update.

## Design
- **Layout:** Centered title and dropdown; two grid rows with three widgets each.
- **Widgets:**
  1. Faculty Profile (Neo4j)
  2. Top Collaborators (Neo4j)
  3. Faculty Notes (MongoDB)
  4. Publications per Year (MySQL)
  5. Top Institutes (MySQL)
  6. Mark Reviewed (MySQL)
- **Styling:** Dark-mode theme with custom CSS in `assets/style.css`.

## Implementation
- **Language:** Python 3.10+
- **Frameworks & Libraries:**
  - Dash Plotly (frontend)
  - Plotly Express (`plotly_dark` theme)
  - `mysql-connector-python`, PyMongo, Neo4j Python Driver (backend)
- **Structure:**
  - `app.py`: Dash app and callbacks
  - `neo4j_utils.py`, `mongodb_utils.py`, `mysql_utils.py`: database access modules

## Database Techniques
- **MySQL:**
  - Indexed columns (`Paper.year`, `Paper.venue_id`)
  - `VIEW` for repeated publication queries
  - Idempotent review table with `INSERT IGNORE`
- **MongoDB:**
  - Index on `faculty_notes.faculty`
  - Atomic inserts for note creation
- **Neo4j:**
  - Constraints on `FACULTY(id)` and `PUBLICATION(id)`
  - Parameterized Cypher for safe queries

## Extra-Credit Capabilities
None implemented.

## Contributions
**Gabriel Warner (solo, ~40 hours)**
- Full-stack development: dashboard layout, styling, and callbacks
- Neo4j widgets: Profile, Co-author chart
- MongoDB widget: Faculty Notes
- MySQL widgets: Publication Trend, Top Institutes, Mark Reviewed
- README authoring and demo video production

