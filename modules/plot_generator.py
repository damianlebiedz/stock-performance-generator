import plotly.express as px

def stock_plot(all_stocks):
    try:
        for stock in all_stocks:
            ticker = stock['Ticker']
            for info in stock['Informations']:
                timeframe = info['Timeframe']
                fig = px.line(
                    timeframe,
                    x='Date',
                    y='Total profit',
                    title=f'Total profit over Time for {ticker}',
                    labels={'Date': 'Date', 'Total profit': 'Total profit'}
                )
                fig.update_traces(name=f'{ticker} Total profit', line=dict(width=2, color='black'))
                fig.update_layout(template='plotly_white')
                fig.show()

    except Exception as e:
        print(f"Error in stock_plot: {e}")


def summary_plot(summary):
    try:
        fig = px.line(
            summary,
            x='Date',
            y='Total profit',
            title='Portfolio total profit over time',
            labels={'Date': 'Date', 'Total profit': 'Total profit'}
        )
        fig.update_traces(name='Total Profit', line=dict(width=2, color='black'))
        fig.update_layout(template='plotly_white')
        fig.show()

    except Exception as e:
        print(f"Error in summary_plot: {e}")