# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

from yzapps import dbconnect as db
from urllib.parse import urlparse, parse_qs

layout = html.Div(
    [
        html.Div([
            dcc.Store(id='profile_toload', storage_type='memory', data=0),
        ]),
        html.H2('Staff Details'), 
        html.Hr(),
        dbc.Alert(id='profile_alert', is_open=False), 
        dbc.Form(
            [
            dbc.Row(
                [
                    dbc.Label("First Name", width=1),
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='profile_fname', #id 1
                            placeholder="First Name"
                        ),
                        width=5
                    )
                ],
                className = 'mb-3'
            ),
            dbc.Row(
                [
                    dbc.Label("Last Name", width=1),
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='profile_lname', #id 1.1
                            placeholder="Last Name"
                        ),
                        width=5
                    )
                ],
                className = 'mb-3'
            ),
            dbc.Row(
                [
                    dbc.Label("Phone number", width=1),
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='profile_phonenumber', #id 2
                            placeholder='Phone number'
                        ),
                        width=5
                    )
                ],
                className = 'mb-3'
            ),
            dbc.Row(
                [
                    dbc.Label("Email", width=1),
                    dbc.Col(
                        dbc.Input(
                            type='text',
                            id='profile_email', #id3
                            placeholder='Email',
                        ),
                        width=5
                    )
                ],
                className = 'mb-3'
            ),
            ]
        ),

        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=1),
                    dbc.Col(
                        dbc.Checklist(
                            id='profile_removerecord', #id4
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'},
                        ),
                        width=5,
                    ),
                ],
                className="mb-3",
            ),
            id='profile_removerecord_div' # id5
        ),


        dbc.Button(
            'Submit',
            id='profile_submit', # id6
            n_clicks=0 
        ),
        dbc.Modal( 
[
            dbc.ModalHeader(
                html.H4('Save Success')
            ),
            dbc.ModalBody(
                id= 'profile_feedback_message'
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Proceed",
                    href='/modules/staff', 
                    id= 'profile_btn_modal'
                )
            )
        ],
        centered=True,
        id='profile_successmodal',
        backdrop='static' 
    )
])
@app.callback(
[
    Output('profile_toload', 'data'),
    Output('profile_removerecord_div', 'style'),
],
[
    Input('url', 'pathname')
],
[
    State('url', 'search')
]
)
def profile_load(pathname, search):
    if pathname == '/modules/staff_profile':
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
        return [to_load, removediv_style]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('profile_alert', 'color'),
        Output('profile_alert', 'children'),
        Output('profile_alert', 'is_open'),
        Output('profile_successmodal', 'is_open'),
        Output('profile_feedback_message', 'children'),
        Output('profile_btn_modal', 'href')

    ],
    [
        Input('profile_submit', 'n_clicks'),
        Input('profile_btn_modal', 'n_clicks'),

    ],
[
State('profile_fname', 'value'),
State('profile_lname', 'value'),
State('profile_phonenumber', 'value'),
State('profile_email', 'value'),
State('url', 'search'),
State('profile_removerecord', 'value'),
]
)
def movieprofile_saveprofile(submitbtn, closebtn, fname, lname, phonenumber, email, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'profile_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage=''
            okay_href=''
            if not fname  : 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please insert your first name.'
            elif not lname  : 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please insert your last name.'
            elif not phonenumber  :
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the phone number.'
            elif not email :
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the email.'
            else: 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    sql = '''
                    insert into staff (staff_fname, staff_lname, staff_phone, staff_email, staff_delete_ind)
                    VALUES (%s, %s, %s, %s, %s)
                    '''
                    values = [fname, lname, phonenumber, email, False]
                    db.modifydatabase(sql, values)
                    feedbackmessage= "staff detail has been saved"
                    okay_href='/modules/staff'
                    modal_open = True
                
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    staffid = parse_qs(parsed.query)['id'][0]
                    sqlcode = """
                    UPDATE staff SET staff_fname = %s, staff_lname = %s, staff_phone= %s, staff_email =%s, staff_delete_ind = %s
                    WHERE staff_id = %s
                    """
                    to_delete = bool(removerecord)
                    values = [fname, lname, phonenumber, email ,to_delete, staffid]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "Staff details has been updated."
                    okay_href = '/modules/staff'
                    modal_open = True
                    
                else:
                    raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
        else: 
            
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
[
    Output('profile_fname', 'value'),
    Output('profile_lname', 'value'),
    Output('profile_phonenumber', 'value'),
    Output('profile_email', 'value'),
],
[
    Input('profile_toload', 'modified_timestamp')
],
[
    State('profile_toload', 'data'),
    State('url', 'search'),
]
)
def profile_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        staffid = parse_qs(parsed.query)['id'][0]
        sql = """
        Select staff_fname, staff_lname, staff_phone, staff_email
        from staff
		where staff_id = %s
        """
        values = [staffid]
        col = ['fname', 'lname', 'phonenumber', 'email']
        df = db.querydatafromdatabase(sql, values, col)
        fname = df['fname'][0]
        lname = df['lname'][0]
        phonenumber = df['phonenumber'][0]
        email = df['email'][0]
        return [fname, lname, phonenumber, email]
    else:
        raise PreventUpdate

