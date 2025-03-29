import matplotlib.pyplot as plt

def plot_daily_performance(daily_performance):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_performance['Date'], daily_performance['Profit'], label="Daily Portfolio Performance", color="blue")

    plt.title("Daily Portfolio Performance")
    plt.xlabel("Date")
    plt.ylabel("Profit")
    plt.grid(True)
    plt.legend()

    plt.savefig('output/daily_portfolio_performance.png')
    plt.show()