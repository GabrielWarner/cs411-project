from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from neo4j_utils import (
    get_all_faculty,
    get_faculty_profile,
    get_top_coauthors
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Academic Research Explorer"),

    dcc.Dropdown(
        id="faculty-dropdown",
        options=[{"label": n, "value": n} for n in get_all_faculty()],
        placeholder="Select a faculty member…",
        style={"width": "300px"}
    ),

    html.Div(id="faculty-profile-div", style={"marginTop": "1rem"}),

    html.H3("Top Collaborators", style={"marginTop": "2rem"}),
    dcc.Graph(id="coauthor-chart", style={"width": "500px", "height": "400px"}),

], style={"padding": "2rem"})


@app.callback(
    Output("faculty-profile-div", "children"),
    Output("coauthor-chart", "figure"),
    Input("faculty-dropdown", "value")
)
def update_faculty_info(name):
    if not name:
        empty_fig = px.bar(title="Select a faculty above")
        return (
            html.Div("Please select a faculty member above."),
            empty_fig
        )

    profile = get_faculty_profile(name)
    if not profile:
        profile_div = html.Div(f"No data found for {name}.")
    else:
        profile_div = html.Div([
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

    coauthors = get_top_coauthors(name, limit=5)
    if not coauthors:
        fig = px.bar(title="No collaborators found")
    else:
        names, counts = zip(*coauthors)
        fig = px.bar(
            x=names, y=counts,
            labels={"x": "Co-author", "y": "Joint Publications"},
            title=f"Top 5 Co-Authors for {name}"
        )
        fig.update_layout(margin={"t": 40, "b": 20, "l": 20, "r": 20})

    return profile_div, fig


if __name__ == "__main__":
    app.run(debug=True, port=8051)