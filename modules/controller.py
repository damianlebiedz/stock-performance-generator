# CONTROLLER

# Asset with which we compare the portfolio performance
comparison_ticker = "^SPX"

currency_of_portfolio = "PLN"

def format_symbol_for_yf(symbol):
    if symbol.endswith('.UK'):
        return symbol[:-3] + '.L'
    elif symbol.endswith('.US'):
        return symbol[:-3]
    elif symbol.endswith('.FR'):
        return symbol[:-3] + '.PA'
    return symbol
