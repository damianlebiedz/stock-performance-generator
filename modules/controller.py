# CONTROLLER

# If you are using a history of transactions from XStation5 platform from XTB broker, set True
# Otherwise you should format your history of transactions as indicated in data/README.md file, then set False
XStation5 = False

# Asset with which we compare the portfolio performance
comparison_ticker = "^SPX"

def format_symbol_for_yf(symbol):
    if symbol.endswith('.UK'):
        return symbol[:-3] + '.L'
    elif symbol.endswith('.US'):
        return symbol[:-3]
    elif symbol.endswith('.FR'):
        return symbol[:-3] + '.PA'
    return symbol

def format_currency_for_yf(symbol):
    if symbol.endswith('.UK'):
        return 'GBP'
    elif symbol.endswith('.US'):
        return 'USD'
    elif symbol.endswith('.FR' or '.DE'):
        return 'EUR'
    return 'USD'