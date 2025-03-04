import matplotlib.pyplot as plt

def plot_portfolio(grouped_data):
    plt.figure(figsize=(10, 10))
    plt.pie(grouped_data.values, labels=grouped_data.index, autopct='%1.1f%%')
    plt.title('Portfolio')
    plt.axis('equal')
    plt.savefig('output/portfolio.png')
    plt.show()

def plot_daily_performance(daily_performance):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_performance.index, daily_performance.values, label="Portfolio Performance", color="blue")

    plt.title("Daily Portfolio Performance")
    plt.xlabel("Date")
    plt.ylabel("Daily Profit/Loss (in PLN)")
    plt.grid(True)
    plt.legend()

    plt.savefig('output/daily_performance.png')
    plt.show()