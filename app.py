from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
from mongodb_utils import get_notes_for_faculty, add_note_for_faculty
from mysql_utils import (
    get_publications_per_year,
    get_top_institutes,
    get_papers_for_faculty,
    mark_reviewed,
    get_reviewed_papers_for_faculty
)
from neo4j_utils import get_all_faculty, get_faculty_profile, get_top_coauthors

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Academic Research Explorer"),
        dcc.Dropdown(
            id="faculty-dropdown",
            options=[{"label": n, "value": n} for n in get_all_faculty()],
            placeholder="Select a faculty member…",
            style={"width": "300px", "margin": "1rem auto 2rem"}
        ),
    ], style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Div([
                html.H3("Faculty Profile"),
                html.Div(id="faculty-profile-div")
            ], className="grid-item"),

            html.Div([
                html.H3("Top Collaborators"),
                dcc.Graph(
                    id="coauthor-chart",
                    style={"height": "400px"}
                )
            ], className="grid-item"),

            html.Div([
                html.H3("Faculty Notes"),
                dcc.Textarea(
                    id="note-input",
                    placeholder="Type your note here…",
                    style={"width": "100%", "height": "80px"}
                ),
                html.Button(
                    "Add Note",
                    id="submit-note",
                    n_clicks=0,
                    style={"marginTop": "0.5rem"}
                ),
                html.Ul(
                    id="notes-list",
                    style={"marginTop": "1rem"}
                )
            ], className="grid-item"),
        ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "20px", "marginBottom": "20px"}),

        html.Div([
            html.Div([
                html.H3("Publications Per Year"),
                dcc.Graph(
                    id="pub-trend-chart",
                    style={"height": "400px"}
                )
            ], className="grid-item"),

            html.Div([
                html.H3("Top Institutes"),
                dcc.Graph(
                    id="institute-chart",
                    style={"height": "400px"}
                )
            ], className="grid-item"),

            html.Div([
                html.H3("Review Papers"),
                dcc.Dropdown(
                    id="paper-dropdown",
                    options=[],
                    placeholder="Select a paper to mark reviewed",
                    style={"width": "100%"}
                ),
                html.Button(
                    "Mark Reviewed",
                    id="review-button",
                    n_clicks=0,
                    style={"marginTop": "0.5rem"}
                ),
                html.Ul(
                    id="reviewed-list",
                    style={"marginTop": "1rem"}
                )
            ], className="grid-item"),
        ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "20px"}),
    ], style={
        "padding": "2rem",
        "maxWidth": "1800px",
        "margin": "0 auto"
    }),
], style={"padding": "2rem"})

@app.callback(
    Output("faculty-profile-div", "children"),
    Input("faculty-dropdown", "value")
)
def update_profile(name):
    if not name:
        return html.Div("Please select a faculty member above.")
    
    try:
        profile = get_faculty_profile(name)
        if not profile:
            return html.Div(f"No data found for {name}.")
        
        return html.Div([
            html.Img(
                src=profile["photoUrl"],
                style={"width": "150px", "borderRadius": "8px"}
            ),
            html.H2(profile["name"], style={"marginTop": "0.5rem"}),
            html.P(profile["position"], style={"fontStyle": "italic"})
        ], style={
            "border": "1px solid #ccc",
            "padding": "1rem",
            "borderRadius": "8px",
            "maxWidth": "400px"
        })
    except Exception as e:
        print(f"Error in update_profile: {str(e)}")
        return html.Div(f"An error occurred: {str(e)}")

@app.callback(
    Output("pub-trend-chart", "figure"),
    Input("faculty-dropdown", "value")
)
def update_pub_trend(name):
    if not name:
        return px.line(title="Select a faculty above")
    
    try:
        trend_data = get_publications_per_year(name)
        if not trend_data:
            return px.line(title="No publication data found")
        
        years, counts = zip(*trend_data)
        fig = px.line(
            x=years, y=counts,
            labels={"x": "Year", "y": "Number of Publications"},
            title=f"Publications by Year for {name}"
        )
        fig.update_traces(mode="lines+markers")
        fig.update_layout(margin={"t": 40, "b": 20, "l": 20, "r": 20})
        return fig
    except Exception as e:
        print(f"Error in update_pub_trend: {str(e)}")
        return px.line(title=f"Error occurred: {str(e)}")

@app.callback(
    Output("coauthor-chart", "figure"),
    Input("faculty-dropdown", "value")
)
def update_coauthor_chart(name):
    if not name:
        return px.bar(title="Select a faculty above")
    
    try:
        coauthors = get_top_coauthors(name, limit=5)
        if not coauthors:
            return px.bar(title="No collaborators found")
        
        names, counts = zip(*coauthors)
        fig = px.bar(
            x=names, y=counts,
            labels={"x": "Co-author", "y": "Joint Publications"},
            title=f"Top 5 Co-Authors for {name}"
        )
        fig.update_layout(margin={"t": 40, "b": 20, "l": 20, "r": 20})
        return fig
    except Exception as e:
        print(f"Error in update_coauthor_chart: {str(e)}")
        return px.bar(title=f"Error occurred: {str(e)}")

@app.callback(
    [Output("notes-list", "children"),
     Output("note-input", "value")],
    [Input("faculty-dropdown", "value"),
     Input("submit-note", "n_clicks")],
    [State("note-input", "value")]
)
def update_notes(name, n_clicks, note_text):
    if not name:
        return [], ""
    
    try:
        notes = get_notes_for_faculty(name)
        notes_list = [html.Li(f"[{note['time'].strftime('%Y-%m-%d %H:%M')}] {note['text']}") for note in notes]
        
        if n_clicks and note_text:
            add_note_for_faculty(name, note_text)
            notes_list.insert(0, html.Li(note_text))
            return notes_list, ""
        
        return notes_list, note_text or ""
    except Exception as e:
        print(f"Error in update_notes: {str(e)}")
        return [html.Li(f"Error: {str(e)}")], ""

@app.callback(
    Output("institute-chart", "figure"),
    Input("faculty-dropdown", "value")
)
def update_institute_chart(_):
    try:
        data = get_top_institutes(limit=10)
        if not data:
            return px.bar(title="No data available")

        inst_names, counts = zip(*data)
        fig = px.bar(
            x=inst_names,
            y=counts,
            labels={"x": "Institute", "y": "Publication Count"},
            title="Top 10 Institutes by Faculty Publications"
        )
        fig.update_layout(margin={"t": 40, "b": 100, "l": 20, "r": 20})
        fig.update_xaxes(tickangle=-45)
        return fig
    except Exception as e:
        print(f"Error in update_institute_chart: {str(e)}")
        return px.bar(title=f"Error occurred: {str(e)}")

@app.callback(
    Output("paper-dropdown", "options"),
    Input("faculty-dropdown", "value")
)
def populate_papers(faculty_name):
    if not faculty_name:
        return []
    papers = get_papers_for_faculty(faculty_name)
    return [{"label": title, "value": pid} for pid, title in papers]

@app.callback(
    Output("reviewed-list", "children"),
    [Input("review-button", "n_clicks"),
     Input("faculty-dropdown", "value")],
    [State("paper-dropdown", "value")]
)
def update_reviewed(n_clicks, faculty_name, paper_id):
    if not faculty_name:
        return [html.Li("Select a faculty first.")]
    if n_clicks and paper_id:
        mark_reviewed(paper_id)
    
    # Get all papers for this faculty first
    all_papers = {str(pid): title for pid, title in get_papers_for_faculty(faculty_name)}
    
    # Get reviewed papers
    reviewed_ids = get_reviewed_papers_for_faculty(faculty_name)
    if not reviewed_ids:
        return [html.Li("No papers reviewed yet.")]
    
    # Create list items with paper titles
    items = []
    for pid in reviewed_ids:
        if pid in all_papers:
            items.append(html.Li(all_papers[pid]))
        else:
            print(f"Warning: Paper ID {pid} not found in faculty's papers")
    
    return items

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .grid-item {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            body {
                background: #f5f5f5;
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            h3 {
                margin-top: 0;
                margin-bottom: 1rem;
                color: #2c3e50;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True, port=8051)