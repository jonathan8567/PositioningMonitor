from Interactive import Dash, dash_table,Input,Output,html,dcc,State,dbc,px,go,pd,JupyterDash,date, timedelta,datetime


class PositionReporting:
    def __init__(self, fund):     
        self.fund = fund
        self.rates = pd.read_csv("P:\\Product Specialists\\Tools\\Weekly Report Tool\\Rates\\" + fund + ".csv")
        self.eurorates = pd.read_csv("P:\\Product Specialists\\Tools\\Weekly Report Tool\\Euro Rates\\" + fund + ".csv")
        self.fx = pd.read_csv("P:\\Product Specialists\\Tools\\Weekly Report Tool\\Currency\\" + fund + ".csv")
        
        self.rates["index"] =  pd.to_datetime(self.rates["index"], format="%Y-%m-%d").dt.date
        self.eurorates["index"] =  pd.to_datetime(self.eurorates["index"], format="%Y-%m-%d").dt.date
        self.fx["index"] =  pd.to_datetime(self.fx["index"], format="%Y-%m-%d").dt.date
                
        for i in range(2, len(self.rates.columns)):
            self.rates.iloc[:, [i]] = self.rates.iloc[:, [i]] *100
        for i in range(2, len(self.eurorates.columns)):
            self.eurorates.iloc[:, [i]] = self.eurorates.iloc[:, [i]] *100
        for i in range(1, len(self.fx.columns)):    
            self.fx.iloc[:, [i]] = self.fx.iloc[:, [i]] *100
                            
        self.available_rates = self.rates.columns[2:]
        self.available_eurorates = self.eurorates.columns[2:]
        self.available_fx = self.fx.columns[2:]
        
    def plot(self, start_date=None, end_date=None, rates_targets=None, rates_target_year=None, eurorates_targets=None, eurorates_target_year=None, fx_targets=None):

        ## Change type for start & end date
        if start_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            
            df_rates = self.rates[self.rates['index'] >= start_date]
            df_eurorates = self.eurorates[self.eurorates['index'] >= start_date]
            df_fx = self.fx[self.fx['index'] >= start_date]
        if end_date:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            
            df_rates = df_rates[df_rates['index'] <= end_date]
            df_eurorates = df_eurorates[df_eurorates['index'] <= end_date]
            df_fx = df_fx[df_fx['index'] >= start_date]
                  
                
        ## Get main rates  
        
        # Select year segment    
        if rates_target_year == "2Y":
            df_rates = df_rates[df_rates['Year'] == "2Y"]
        elif rates_target_year == "5Y":
            df_rates = df_rates[df_rates['Year'] == "5Y"]
        elif rates_target_year == "10Y":
            df_rates = df_rates[df_rates['Year'] == "10Y"]
        elif rates_target_year == "20Y":
            df_rates = df_rates[df_rates['Year'] == "20Y"]
        elif rates_target_year == "Unknown":
            df_rates = df_rates[df_rates['Year'] == "Unknown"]
        elif rates_target_year == "Total":
            df_rates = df_rates.groupby(['index']).aggregate('sum').reset_index()

        # Build chart
        '''fig_rates = go.Figure(
            data=[
                go.Scatter(x=df_rates["index"], y=df_rates[rates_target], name=rates_target_year)
            ],
            layout=dict(
                title="Rates - Main",
                height=400,
            ),
        )'''
        fig_rates = go.Figure(layout=dict(
                    title="Rates - Main",
                ))

        for rates_target in rates_targets:
            fig_rates.add_trace(go.Scatter(x=df_rates["index"], y=df_rates[rates_target], name=rates_target))
       
        
        ## Get euro rates                      
        
        # Select year segment
        if eurorates_target_year == "2Y":
            df_eurorates = df_eurorates[df_eurorates['Year'] == "2Y"]
        elif eurorates_target_year == "5Y":
            df_eurorates = df_eurorates[df_eurorates['Year'] == "5Y"]
        elif eurorates_target_year == "10Y":
            df_eurorates = df_eurorates[df_eurorates['Year'] == "10Y"]
        elif eurorates_target_year == "20Y":
            df_eurorates = df_eurorates[df_eurorates['Year'] == "20Y"]
        elif eurorates_target_year == "Unknown":
            df_eurorates = df_eurorates[df_eurorates['Year'] == "Unknown"]
        elif eurorates_target_year == "Total":
            df_eurorates = df_eurorates.groupby(['index']).aggregate('sum').reset_index()

        # Build chart
        '''fig_eurorates = go.Figure(
            data=[
                go.Scatter(x=df_eurorates["index"], y=df_eurorates[eurorates_target], name=eurorates_target_year)
            ],
            layout=dict(
                title="Rates - Euro",
            ),
        )'''
        fig_eurorates = go.Figure(layout=dict(
                    title="Rates - Euro",
                ))

        for eurorates_target in eurorates_targets:
            fig_eurorates.add_trace(go.Scatter(x=df_eurorates["index"], y=df_eurorates[eurorates_target], name=eurorates_target))
       
        ## Get fx
        
        # Chart Initialize
        fig_fx = go.Figure(layout=dict(
                    title="FX (%)",
                    yaxis_range=[-8,8]
                ))

        if '  ALL' in fx_targets:
            for fx_target in self.available_fx:
                fig_fx.add_trace(go.Scatter(x=df_fx["index"], y=df_fx[fx_target], name=fx_target))
        else:
            for fx_target in fx_targets:
                fig_fx.add_trace(go.Scatter(x=df_fx["index"], y=df_fx[fx_target], name=fx_target))


        return fig_rates, fig_eurorates, fig_fx
        
    def run_dash(self):
            # Build App            
            app = JupyterDash(__name__)
            app.layout = html.Div([ 
                html.Div([                
                    html.H1("Positioning: " + self.fund),
                    
                    html.Div([
                        html.H2("Date Range:"),
                    ],
                        style={'width': '15%', 'display': 'inline-block'}),
                    
                    html.Div([
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=date(2023,8,29),
                            max_date_allowed=date.today(),                    
                            initial_visible_month=(date.today()-timedelta(days=7)).replace(day=1),
                            start_date=date.today()-timedelta(days=7),
                            end_date=date.today(),
                            display_format='DD-MM-YYYY',
                        )
                    ],
                        style={'display': 'inline-block'}),
                    
                    html.Div([
                        dcc.Checklist(
                            id='rates_currency',
                            options=self.available_rates,
                            value=['Total'],
                            labelStyle = {'cursor': 'pointer', 'margin-left':'20px'}
                        ),
                    ],
                        style={'marginRight': 20, 'marginLeft': 20}),
                    
                    html.Div([
                        dcc.RadioItems(
                            options=['Total', '2Y', '5Y', '10Y', '20Y', 'Unknown'],
                            value='Total',
                            id="checklist-rates-maturity",
                            labelStyle = {'cursor': 'pointer', 'margin-left':'20px'}
                        ),
                        dcc.Graph(id="rates")
                    ],
                        style={'marginRight': 20, 'marginLeft': 20}),
                    
                    html.Div([
                        dcc.Checklist(
                            id='eurorates_currency',
                            options=self.available_eurorates,
                            value=['Total'],
                            labelStyle = {'cursor': 'pointer', 'margin-left':'20px'}
                        ),
                    ],
                        style={'marginRight': 20, 'marginLeft': 20}),
                    
                    html.Div([
                        dcc.RadioItems(
                            options=['Total', '2Y', '5Y', '10Y', '20Y', 'Unknown'],
                            value='Total',
                            id="checklist-eurorates-maturity",
                            labelStyle = {'cursor': 'pointer', 'margin-left':'20px'}
                        ),
                        dcc.Graph(id="eurorates")
                    ],
                        style={'marginRight': 20, 'marginLeft': 20}),
                    
                    html.Div([
                        dcc.Checklist(
                            id='fx_currency',
                            options=self.available_fx.union(['  ALL']),
                            value=['USD'],
                            labelStyle = {'cursor': 'pointer', 'margin-left':'10px'}
                        ),
                        dcc.Graph(id="fx")
                    ],
                        style={'marginRight': 20, 'marginLeft': 20}),
                ])
            ])
            
            @app.callback(
                Output("rates", "figure"),
                Output("eurorates", "figure"),             
                Output("fx", "figure"),   
                Input('my-date-picker-range', 'start_date'),
                Input('my-date-picker-range', 'end_date'),
                Input('rates_currency', 'value'),
                Input('checklist-rates-maturity', 'value'),
                Input('eurorates_currency', 'value'),
                Input('checklist-eurorates-maturity', 'value'),
                Input('fx_currency', 'value')
            )

            def update_output(start_date, end_date, rates_currency, rates_year, eurorates_currency, eurorates_year, fx_currency):
                return self.plot(start_date, end_date, rates_currency, rates_year, eurorates_currency, eurorates_year, fx_currency)                

            # Run app and display result inline in the notebook
            #app.run_server(mode='inline')
            
            #Run app and display result in another tab
            app.run_server(host = '127.0.0.1',debug = True)