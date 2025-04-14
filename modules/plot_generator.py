import matplotlib.pyplot as plt


def stock_plot(all_stocks):
    try:
        for stock in all_stocks:
            ticker = stock['Ticker']
            for info in stock['Informations']:
                timeframe = info['Timeframe']
                plt.figure(figsize=(10, 6))
                plt.plot(timeframe['Date'], timeframe['Total profit'], label=f'{ticker} Total profit', linewidth=2)
                plt.title(f'Total profit over Time for {ticker}')
                plt.xlabel('Date')
                plt.ylabel('Total profit')
                plt.legend()
                plt.grid()
                plt.show()

    except Exception as e:
        print(f"Error in stock_plot: {e}")


def summary_plot(summary):
    try:
        plt.plot(summary['Date'], summary['Total profit'], label='Total Profit', linewidth=3, linestyle='--', color='black')
        plt.title('Portfolio total profit over time')
        plt.xlabel('Date')
        plt.ylabel('Total profit')
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print(f"Error in summary_plot: {e}")