import plotly.graph_objects as go


def stock_plot(all_stocks):
    try:
        fig = go.Figure()
        buttons = []

        for idx, stock in enumerate(all_stocks):
            ticker = stock['Ticker']
            for info in stock['Informations']:
                timeframe = info['Timeframe']

                if 'Total change [%]' not in timeframe.columns or 'Total change [%] in PLN' not in timeframe.columns:
                    print(f"Warning: missing columns in data for {ticker}")
                    continue

                visible = [False] * (2 * len(all_stocks))
                visible[2 * idx] = True
                visible[2 * idx + 1] = True

                fig.add_trace(go.Scatter(
                    x=timeframe['Date'],
                    y=timeframe['Total change [%]'],
                    mode='lines',
                    name=f'{ticker} Total change [%]',
                    line=dict(color='black'),
                    visible=True if idx == 0 else False
                ))

                fig.add_trace(go.Scatter(
                    x=timeframe['Date'],
                    y=timeframe['Total change [%] in PLN'],
                    mode='lines',
                    name=f'{ticker} Total change [%] in PLN',
                    line=dict(color='green'),
                    visible=True if idx == 0 else False
                ))

                buttons.append(dict(
                    label=ticker,
                    method='update',
                    args=[{'visible': [i == 2 * idx or i == 2 * idx + 1 for i in range(2 * len(all_stocks))]},
                          {'title': f"{ticker}"}]
                ))

        fig.update_layout(
            title=f"{all_stocks[0]['Ticker']}",
            xaxis_title='Date',
            yaxis_title='%',
            updatemenus=[{
                'buttons': buttons,
                'direction': 'down',
                'showactive': True,
                'x': 0.1,
                'xanchor': 'left',
                'y': 1.1,
                'yanchor': 'top'
            }],
            legend=dict(x=0, y=-0.2, orientation='h'),
            margin=dict(t=80),
            dragmode = False,
            hovermode = "closest",
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True)
        )

        return fig

    except Exception as e:
        print(f"Error in stock_plot_plotly: {e}")


def summary_plot(summary):
    try:
        if 'Total change [%]' not in summary.columns or 'Total change [%] in PLN' not in summary.columns:
            print("Warning: missing columns in summary data")
            return

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=summary['Date'],
            y=summary['Total change [%]'],
            mode='lines',
            name='Portfolio Total change [%]',
            line=dict(color='black')
        ))

        fig.add_trace(go.Scatter(
            x=summary['Date'],
            y=summary['Total change [%] in PLN'],
            mode='lines',
            name='Portfolio Total change [%] in PLN',
            line=dict(color='green')
        ))

        fig.update_layout(
            title='Portfolio',
            xaxis_title='Date',
            yaxis_title='%',
            legend=dict(x=0, y=-0.2, orientation='h'),
            margin=dict(t=80),
            dragmode = False,
            hovermode = "closest",
            xaxis = dict(fixedrange=True),
            yaxis = dict(fixedrange=True)
        )

        return fig

    except Exception as e:
        print(f"Error in summary_plot_plotly: {e}")
