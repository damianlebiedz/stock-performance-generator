import plotly.graph_objects as go
from modules.controller import comparison_ticker
from modules.controller import currency_of_portfolio


def summary_plot(summary):
    start_date = summary.iloc[0]['Date'].strftime('%Y-%m-%d')
    end_date = summary.iloc[-1]['Date'].strftime('%Y-%m-%d')
    try:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=summary['Date'],
            y=summary[f'Total change [%] in {currency_of_portfolio}'],
            mode='lines',
            name=f'Total change [%] in {currency_of_portfolio} of portfolio',
            line=dict(color='green')
        ))

        fig.add_trace(go.Scatter(
            x=summary['Date'],
            y=summary[f'Total change [%] of {comparison_ticker}'],
            mode='lines',
            name=f'Total change [%] of {comparison_ticker}',
            line=dict(color='grey')
        ))

        fig.update_layout(
            title=f'Portfolio performance from {start_date} to {end_date}',
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
        print(f"Error in summary_plot: {e}")
