import dash
from dash import dcc, html, Output, Input, State, ALL, callback_context
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import dash_leaflet as dl
import apc_dash.app_reseaupolytech_tools as app_reseaupolytech_tools

COLORS = {
    "primary":    "#0056b3",
    "background": "#f4f7f6",
    "card":       "#ffffff",
    "shadow":     "0 4px 12px rgba(0,0,0,0.08)",
}

# ==============================================================================
# 3. HEADER
# ==============================================================================

def create_app_header():
    return html.Div([
        html.Div([
            html.Div([
                html.Div( className="header-logo-icon"),
                html.Div([
                    html.H1("Learnagement - Tableau de bord", className="header-title"),
                    html.P("Explorez les formations, compétences et débouchés des écoles Polytech",
                           className="header-subtitle"),
                ]),
            ], className="header-logo"),
        ], className="header-content"),
    ],
    className="app-header",
    style={
        "position": "sticky", "top": "0", "zIndex": "9999",
        "backgroundColor": "white", "width": "100%",
    })


# ==============================================================================
# 4. LAYOUT
# ==============================================================================

polytech_analysis_layout = html.Div(
    style={'backgroundColor': COLORS['background'], 'minHeight': '100vh'},
    children=[

        dcc.Store(id="selected-school-store", data="ALL"),

        # Navbar
        html.Div(
            style={
                'backgroundColor': COLORS['primary'],
                'position': 'sticky', 'top': '0', 'zIndex': '9999',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.15)',
            },
            children=[html.Div(
                style={'display': 'flex', 'alignItems': 'stretch',
                       'padding': '0 24px', 'height': '64px'},
                children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'stretch', 'gap': '4px'}, children=[
                        html.Div("Réseau Polytech", id='tab-reseau', n_clicks=0,
                            style={'display': 'flex', 'alignItems': 'center', 'padding': '0 20px',
                                   'cursor': 'pointer', 'fontSize': '14px', 'fontWeight': '600',
                                   'color': 'white', 'borderBottom': '3px solid white'}),
                        html.Div("Polytech Annecy", id='tab-annecy', n_clicks=0,
                            style={'display': 'flex', 'alignItems': 'center', 'padding': '0 20px',
                                   'cursor': 'pointer', 'fontSize': '14px', 'fontWeight': '400',
                                   'color': 'rgba(255,255,255,0.6)',
                                   'borderBottom': '3px solid transparent'}),
                    ]),
                    html.Div(
                        "Explorez les formations, compétences et débouchés des écoles Polytech",
                        style={'marginLeft': 'auto', 'color': 'rgba(255,255,255,0.55)',
                               'fontSize': '12px', 'display': 'flex', 'alignItems': 'center',
                               'fontStyle': 'italic'}
                    ),
                ]
            )]
        ),

        # ── Page Réseau Polytech ──────────────────────────────────────────────
        html.Div(id='page-reseau', children=[
            html.Div(style={'padding': '24px'}, children=[

                html.Div(style={'backgroundColor': COLORS['card'], 'padding': '15px',
                                'borderRadius': '15px', 'boxShadow': COLORS['shadow'],
                                'marginBottom': '20px'}, children=[
                    html.H3("Localisation des écoles",
                            style={'margin': '0 0 12px', 'fontSize': '16px', 'fontWeight': '500'}),
                    dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer-markers")],
                           center=[46.5, 2.5], zoom=6,
                           style={'height': '55vh', 'borderRadius': '10px'}),
                    html.Div("Cliquez sur une école pour explorer ses formations",
                             style={'fontSize': '12px', 'color': '#bbb',
                                    'textAlign': 'center', 'marginTop': '8px'}),
                ]),

                html.Div(id='bloc-filieres', style={'display': 'none'}, children=[
                    html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px 25px',
                                    'borderRadius': '15px', 'boxShadow': COLORS['shadow'],
                                    'marginBottom': '20px'}, children=[
                        html.Div(id='breadcrumb',
                                 style={'fontSize': '14px', 'marginBottom': '16px',
                                        'paddingBottom': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                        html.Div("① Choisissez une filière",
                                 style={'fontSize': '10px', 'color': '#bbb', 'fontWeight': '600',
                                        'textTransform': 'uppercase', 'letterSpacing': '1px',
                                        'marginBottom': '12px'}),
                        html.Div(id='col-filieres',
                                 style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '8px'}),
                    ]),
                ]),

                html.Div(id='bloc-detail', style={'display': 'none'}, children=[
                    html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px 25px',
                                    'borderRadius': '15px', 'boxShadow': COLORS['shadow'],
                                    'marginBottom': '20px'}, children=[
                        html.Div(id='detail-breadcrumb',
                                 style={'fontSize': '14px', 'marginBottom': '20px',
                                        'paddingBottom': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                        html.Div(style={'display': 'flex', 'gap': '30px'}, children=[
                            html.Div(style={'flex': '1', 'minWidth': '0'}, children=[
                                html.Div("② Compétences",
                                         style={'fontSize': '10px', 'color': '#bbb', 'fontWeight': '600',
                                                'textTransform': 'uppercase', 'letterSpacing': '1px',
                                                'marginBottom': '12px'}),
                                html.Ul(id='liste-competences',
                                        style={'paddingLeft': '18px', 'margin': '0',
                                               'fontSize': '13px', 'lineHeight': '1.8'}),
                            ]),
                            html.Div(style={'width': '1px', 'backgroundColor': '#f0f0f0',
                                            'flexShrink': '0'}),
                            html.Div(style={'flex': '1', 'minWidth': '0'}, children=[
                                html.Div("③ Débouchés & Secteurs",
                                         style={'fontSize': '10px', 'color': '#bbb', 'fontWeight': '600',
                                                'textTransform': 'uppercase', 'letterSpacing': '1px',
                                                'marginBottom': '12px'}),
                                html.Div(id='col-metiers',
                                         style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '6px'}),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),

        # ── Page Polytech Annecy ──────────────────────────────────────────────
        html.Div(id='page-annecy', style={'display': 'none'}, children=[
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center',
                            'justifyContent': 'center', 'height': '60vh', 'gap': '16px'}, children=[
                html.Div("🚧", style={'fontSize': '48px'}),
                html.H2("Polytech Annecy",
                        style={'fontSize': '22px', 'fontWeight': '500', 'color': '#333', 'margin': '0'}),
                html.P("Cette section est en cours de construction.",
                       style={'color': '#aaa', 'fontSize': '14px', 'margin': '0'}),
            ])
        ]),

    ]
)


# ==============================================================================
# 5. CALLBACKS
# ==============================================================================

def register_reseau_polytech_callbacks(app):

    @app.callback(
        [Output('page-reseau',  'style'),
         Output('page-annecy',  'style'),
         Output('tab-reseau',   'style'),
         Output('tab-annecy',   'style')],
        [Input('tab-reseau', 'n_clicks'),
         Input('tab-annecy', 'n_clicks')],
    )
    def switch_tab(n_reseau, n_annecy):
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'tab-reseau'
        base     = {'display': 'flex', 'alignItems': 'center', 'padding': '0 20px', 'cursor': 'pointer'}
        active   = {**base, 'fontSize': '14px', 'fontWeight': '600',
                    'color': 'white', 'borderBottom': '3px solid white'}
        inactive = {**base, 'fontSize': '14px', 'fontWeight': '400',
                    'color': 'rgba(255,255,255,0.6)', 'borderBottom': '3px solid transparent'}
        if triggered == 'tab-annecy':
            return {'display': 'none'}, {'display': 'block'}, inactive, active
        return {'display': 'block'}, {'display': 'none'}, active, inactive

    @app.callback(
        Output("layer-markers", "children"),
        Input("layer-markers", "id"),
    )
    def render_markers(_):
        return [
            dl.CircleMarker(center=coords, id={'type': 'marker-ecole', 'index': school},
                            radius=10, color='white', fillColor=COLORS['primary'], fillOpacity=0.9,
                            children=[dl.Tooltip(school)])
            for school, coords in app_reseaupolytech_tools.coords_ecoles.items()
        ]

    @app.callback(
        Output('selected-school-store', 'data'),
        Input({'type': 'marker-ecole', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True,
    )
    def sync_selection(map_clicks):
        ctx = callback_context
        if not ctx.triggered or ctx.triggered[0]['value'] == 0:
            return dash.no_update
        return json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index']

    @app.callback(
        [Output('col-filieres',      'children'),
         Output('breadcrumb',        'children'),
         Output('bloc-filieres',     'style'),
         Output('bloc-detail',       'style'),
         Output('liste-competences', 'children'),
         Output('col-metiers',       'children')],
        Input('selected-school-store', 'data'),
    )
    def update_filieres(selected_school):
        hidden  = {'display': 'none'}
        visible = {'display': 'block'}
        if not selected_school or selected_school == 'ALL':
            return [], "", hidden, hidden, [], []
        filieres = app_reseaupolytech_tools.df_filtered[app_reseaupolytech_tools.df_filtered['Ecole'] == selected_school]['Formation'].tolist()
        boutons = [
            html.Div(f, id={'type': 'filiere-item', 'index': f}, n_clicks=0,
                     style={'padding': '8px 16px', 'borderRadius': '99px', 'cursor': 'pointer',
                            'border': '1px solid #dde6f5', 'fontSize': '13px',
                            'backgroundColor': '#f5f8ff', 'color': '#0056b3',
                            'fontWeight': '500', 'whiteSpace': 'nowrap'})
            for f in filieres
        ]
        breadcrumb = [
            html.Span(selected_school, style={'fontWeight': '600', 'color': COLORS['primary']}),
            html.Span("  ›  sélectionnez une filière", style={'color': '#ccc'}),
        ]
        return boutons, breadcrumb, visible, hidden, [], []

    @app.callback(
        [Output('liste-competences', 'children', allow_duplicate=True),
         Output('col-metiers',       'children', allow_duplicate=True),
         Output('detail-breadcrumb', 'children'),
         Output('bloc-detail',       'style',    allow_duplicate=True)],
        Input({'type': 'filiere-item', 'index': ALL}, 'n_clicks'),
        State('selected-school-store', 'data'),
        prevent_initial_call=True,
    )
    def update_detail(n_clicks_list, selected_school):
        ctx = callback_context
        if not ctx.triggered or ctx.triggered[0]['value'] == 0:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        filiere_name = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index']
        competences, metiers = [], []
        for school in app_reseaupolytech_tools.data:
            for f in app_reseaupolytech_tools.data[school]:
                if app_reseaupolytech_tools.reparer_texte(f['formation'].replace('-', ' ').title()) == filiere_name:
                    competences = [app_reseaupolytech_tools.reparer_texte(c) for c in f.get('competences', [])]
                    raw = (f.get('metiers') or []) + (f.get('secteurs') or [])
                    for item in raw:
                        if isinstance(item, list):
                            metiers.extend(item)
                        elif isinstance(item, str) and len(item) > 3:
                            for part in item.split('  '):
                                p = part.strip()
                                if len(p) > 3:
                                    metiers.append(p[:60])
                    break
        items_comp = [html.Li(c, style={'marginBottom': '5px'}) for c in competences] or \
                     [html.Li("Aucune compétence disponible.",
                              style={'color': '#aaa', 'listStyle': 'none'})]
        metiers_uniques = sorted(set(metiers))
        tags_metiers = [
            html.Span(m, style={'display': 'inline-block', 'fontSize': '12px',
                                'padding': '5px 12px', 'borderRadius': '99px',
                                'border': '1px solid #c5d8f5', 'margin': '3px',
                                'backgroundColor': '#eef4ff', 'color': '#0056b3',
                                'fontWeight': '500'})
            for m in metiers_uniques
        ] or [html.Span("Aucun débouché disponible.", style={'color': '#aaa', 'fontSize': '13px'})]
        detail_bc = [
            html.Span(selected_school or "", style={'fontWeight': '600', 'color': COLORS['primary']}),
            html.Span("  ›  ", style={'color': '#ccc'}),
            html.Span(filiere_name, style={'fontWeight': '600', 'color': '#333'}),
            html.Span(
                f"  —  {len(competences)} compétence{'s' if len(competences) > 1 else ''}"
                f"  ·  {len(metiers_uniques)} débouché{'s' if len(metiers_uniques) > 1 else ''}",
                style={'color': '#aaa', 'fontSize': '12px'}),
        ]
        return items_comp, tags_metiers, detail_bc, {'display': 'block'}


