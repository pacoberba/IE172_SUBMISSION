import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app

# Top Navbars
from apps.navbars import headnfootTemplate as hft
from apps.navbars import adminTopNavbar, customerTopNavbar

# Side Navbars
from apps.navbars import adminSideNavbar, customerSideNavbar

# Import your pages
from apps import home
from apps.adopt import adopt, adoptionForm
from apps.companyInfo import contactUs, faqs, ourStory
from apps.donate import donate
from apps.logout import logout
from apps.MeetTheRescues import meetTheRescues, mtrCat, mtrDog
from apps.register import register
from apps.signIn import signIn
from apps.signIn.customer import accountProfile, adoptionApp
from apps.signIn.customer.accountProfileEdit import accountProfileEdit, accountProfileEditDwelling, accountProfileEditPassword
from apps.signIn.admin import graphs, rescueManagement, rescueManagementProfile, viewAdoptions, viewAdoptionsComplete

app.layout = html.Div(
    [
        # Top Nav Container (guest/user/admin)
        html.Div(id='header-container'),

        # Primary location for page routing
        dcc.Location(id='url', refresh=True),

        # Separate hidden locations for adopt
        dcc.Location(id='adopt-loc', refresh=True),

        # Session store for user info
        dcc.Store(id='user-session', storage_type='session'),

        # The main container for side navbar + page content
        html.Div(id='main-content', style={"paddingTop": "10px"}),

        hft.create_footer()
    ],
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100vh',
        'justifyContent': 'space-between',
        'paddingTop': '120px',  # offset for top navbar
    }
)

################### CALLBACKS ###################

@app.callback(
    [Output("adopt-modal", "is_open"),
     Output("adopt-loc", "href")],  # separate dcc.Location for adopt
    [Input("adopt-button", "n_clicks"),
     Input("adopt-register", "n_clicks"),
     Input("adopt-signin", "n_clicks")],
    [State("user-session", "data"),
     State("adopt-modal", "is_open")],
    prevent_initial_call=True
)
def handle_adopt_click(adopt_clicks, register_clicks, signin_clicks, user_session, is_open):
    """
    Handles the adopt button click:
    - If logged in => redirect to /adopt
    - If not logged in => toggle adopt-modal open
    Handles modal close when cancel, register, or sign-in buttons are clicked.
    """
    # If the main adopt button was clicked
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "adopt-button":
        if user_session:
            # User is logged in => redirect to /adopt
            return [False, "/adopt"]
        else:
            # Not logged in => open adopt modal
            return [not is_open, dash.no_update]

    # If any modal button was clicked, close the modal
    if triggered_id in ["adopt-register", "adopt-signin"]:
        return [False, dash.no_update]

    raise PreventUpdate


@app.callback(
    Output('header-container', 'children'),
    Input('user-session', 'data'),
    prevent_initial_call=True
)
def update_top_navbar(user_session):
    """
    Dynamically choose which top navbar to display:
    - If user_session not set => default guest navbar
    - If accountType='admin' => adminTopNavbar
    - If accountType='user' => customerTopNavbar
    """
    if not user_session:
        # Guest navbar
        return hft.create_header()

    account_type = user_session.get("accountType", None)
    
    if account_type == 'admin':
        return adminTopNavbar.create_header_admin()
    else:
        return customerTopNavbar.create_header_user()


@app.callback(
    Output('main-content', 'children'),
    Input('url', 'pathname'),
    State('user-session', 'data')
)
def display_page_and_sidebar(pathname, user_session):
    """
    This callback returns a layout that includes:
      - The side navbar (admin or user) if logged in
      - The main page content
    """
    # 1) Determine the page content
    page_layout = route_page(pathname, user_session)

    # 2) If not logged in => no side navbar
    if not user_session:
        return page_layout

    account_type = user_session.get("accountType")
    if account_type == 'admin':
        return html.Div([
            html.Div(adminSideNavbar.adminSidebar(user_session), style={"width":"250px","flexShrink":0}),
            html.Div(page_layout, style={"flexGrow":1,"padding":"20px"})
        ], style={"display":"flex","flexDirection":"row"})

    elif account_type == 'user':
        return html.Div([
            html.Div(customerSideNavbar.customerSidebar(user_session), style={"width":"250px","flexShrink":0}),
            html.Div(page_layout, style={"flexGrow":1,"padding":"20px"})
        ], style={"display":"flex","flexDirection":"row"})

    return page_layout


def route_page(pathname, user_session):
    """
    Also includes access restrictions by account type if needed.
    """
    # Public pages
    if pathname in ['/', '/home']:
        return home.layout
    elif pathname == '/donate':
        return donate.layout
    elif pathname == '/meettherescues':
        return meetTheRescues.layout
    elif pathname == '/meettherescues/dogs':
        return mtrDog.layout
    elif pathname == '/meettherescues/cats':
        return mtrCat.layout
    elif pathname == '/ourstory':
        return ourStory.layout
    elif pathname == '/faqs':
        return faqs.layout
    elif pathname == '/contactus':
        return contactUs.layout
    elif pathname == '/signin':
        return signIn.layout
    elif pathname == '/register':
        return register.layout

    # CUSTOMER SIDE
    elif pathname == '/accountProfile':
        if not user_session or user_session.get('accountType') != 'user':
            return dbc.Alert("Access Denied: Users Only.", color="danger")
        return accountProfile.layout
    elif pathname == '/accountProfile/edit/personal':
        if not user_session or user_session.get('accountType') != 'user':
            return dbc.Alert("Access Denied: Users Only.", color="danger")
        return accountProfileEdit.layout
    elif pathname == '/accountProfile/edit/dwelling':
        if not user_session or user_session.get('accountType') != 'user':
            return dbc.Alert("Access Denied: Users Only.", color="danger")
        return accountProfileEditDwelling.layout
    elif pathname == '/accountProfile/edit/password':
        if not user_session or user_session.get('accountType') != 'user':
            return dbc.Alert("Access Denied: Users Only.", color="danger")
        return accountProfileEditPassword.layout
    elif pathname == '/adoptionApp':
        if not user_session or user_session.get('accountType') != 'user':
            return dbc.Alert("Access Denied: Users Only.", color="danger")
        return adoptionApp.layout

    # ADMIN SIDE
    elif pathname == '/viewAdoptions':
        if not user_session or user_session.get('accountType') != 'admin':
            return dbc.Alert("Access Denied: Admins Only.", color="danger")
        return viewAdoptions.layout
    elif pathname == '/viewAdoptions/fullview':
        if not user_session or user_session.get('accountType') != 'admin':
            return dbc.Alert("Access Denied: Admins Only.", color="danger")
        return viewAdoptionsComplete.layout
    elif pathname == '/rescuesManagement':
        if not user_session or user_session.get('accountType') != 'admin':
            return dbc.Alert("Access Denied: Admins Only.", color="danger")
        return rescueManagement.layout
    elif pathname == '/rescuesManagementProfile':
        if not user_session or user_session.get('accountType') != 'admin':
            return dbc.Alert("Access Denied: Admins Only.", color="danger")
        return rescueManagementProfile.layout
    elif pathname == '/graphs':
        if not user_session or user_session.get('accountType') != 'admin':
            return dbc.Alert("Access Denied: Admins Only.", color="danger")
        return graphs.layout

    # Restrict everything under /adopt to signed in
    elif pathname.startswith("/adopt"):
        if not user_session:
            return dbc.Alert("Access Denied: Please Sign In to Adopt.", color="danger")
        # user is signed in => show adopt sub-routes
        if pathname == '/adopt':
            return adopt.layout
        elif pathname == '/adopt/adoptionForm':
            return adoptionForm.layout
        else:
            return dbc.Alert("404 Not Found under /adopt", color="danger")
    
    elif pathname == '/logout':
        if not user_session:
            return dbc.Alert("You must be logged in to access this page.", color="danger")
        return logout.layout

    else:
        return html.H1("404: Page Not Found", style={'textAlign':'center'})


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)
