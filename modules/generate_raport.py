import pandas as pd
import plotly.io as pio
import os
from datetime import datetime
from modules.plot_generator import stock_plot, summary_plot


def save_combined_report(summary, all_stocks):
    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"output/portfolio_report_{timestamp}"

    stock_fig = stock_plot(all_stocks)
    summary_fig = summary_plot(summary)

    stock_html = pio.to_html(stock_fig, include_plotlyjs='cdn', full_html=False)
    summary_html = pio.to_html(summary_fig, include_plotlyjs='cdn', full_html=False)

    html = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>Portfolio Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .plot-container {{ margin-bottom: 50px; }}
            </style>
        </head>
        <body>
            <h1>Portfolio Report</h1>

            <div class="plot-container">
                {summary_html}
            </div>

            <div class="plot-container">
                {stock_html}
            </div>
        </body>
    </html>
    """

    with open(filename+".html", "w", encoding="utf-8") as f:
        f.write(html)

    with pd.ExcelWriter(filename+".xlsx") as writer:
        summary.to_excel(writer, sheet_name='Summary', index=False)
        for idx, stock in enumerate(all_stocks):
            ticker = stock['Ticker']
            for info in stock['Informations']:
                timeframe = info['Timeframe']
                timeframe.to_excel(writer, sheet_name=f'{ticker}', index=False)

    print(f"Report saved as: {filename}")
