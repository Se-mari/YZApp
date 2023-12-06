#For YZAPP
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate

from app import app

navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                dbc.Col(dbc.NavbarBrand("YZApp", className="ms-2")),
                ],
                align="center",
                className = 'g-0'
            ),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Job-order", href="/modules/job_orders", style=navlink_style),
        dbc.NavLink("Inventory", href="/modules/inventory", style=navlink_style),
        dbc.NavLink("Supplies", href="/modules/supplies", style=navlink_style),
        dbc.NavLink("Analytics", href="/modules/analytics", style=navlink_style),
        dbc.NavLink("Staff", href="/modules/staff", style=navlink_style),
        dbc.NavLink("Customers", href="/modules/customers", style=navlink_style),
        dbc.NavLink("Suppliers", href="/modules/suppliers", style=navlink_style),
        dbc.NavLink("Category", href="/modules/category", style=navlink_style),
        dbc.NavLink("Status", href="/modules/status", style=navlink_style),
        dbc.NavLink("Services", href="/modules/services", style=navlink_style),
        dbc.NavLink("Users", href="/modules/users", style=navlink_style),
        dbc.NavLink("Logout", href="/logout", style=navlink_style),
    ],
    color = 'dark',
    dark = True

)