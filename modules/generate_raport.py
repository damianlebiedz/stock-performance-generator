import plotly.io as pio
import os
from datetime import datetime
from modules.plot_generator import summary_plot


def save_combined_report(summary):
    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"output/portfolio_report_{timestamp}"

    summary_fig = summary_plot(summary)

    summary_html = pio.to_html(summary_fig, include_plotlyjs='cdn', full_html=False)

    html = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .plot-container {{ margin-bottom: 50px; }}
            </style>
        </head>
        <body>
            <div class="plot-container">
                {summary_html}
            </div>
        </body>
    </html>
    """

    with open(filename+".html", "w", encoding="utf-8") as f:
        f.write(html)

    summary.to_excel(filename+".xlsx")

    print(f"Report saved as: {filename}")
