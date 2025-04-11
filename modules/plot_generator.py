import matplotlib.pyplot as plt


def stock_plot(all_stocks):
    try:
        for stock in all_stocks:
            ticker = stock['Ticker']
            for info in stock['Informations']:
                timeframe = info['Timeframe']
                plt.figure(figsize=(10, 6))
                plt.plot(timeframe['Date'], timeframe['Profit'], label=f'{ticker} Profit', linewidth=2)
                plt.title(f'Profit Over Time for {ticker}')
                plt.xlabel('Date')
                plt.ylabel('Profit')
                plt.legend()
                plt.grid()
                plt.show()

    except Exception as e:
        print(f"Error in plot_profits: {e}")

def summary_plot(summary):
    try:
        plt.plot(summary['Date'], summary['Profit'], label='Total Profit', linewidth=3, linestyle='--', color='black')
        plt.title('Combined Profit Over Time')
        plt.xlabel('Date')
        plt.ylabel('Profit')
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print(f"Error in plot_profits: {e}")