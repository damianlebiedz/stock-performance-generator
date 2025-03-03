import matplotlib.pyplot as plt

def plot_daily_performance(daily_performance):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_performance.index, daily_performance.values, label="Portfolio Performance", color="blue")

    plt.title("Daily Portfolio Performance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Profit/Loss (in PLN)")
    plt.grid(True)
    plt.legend()

    plt.savefig('daily_performance_chart.png')
    plt.show()