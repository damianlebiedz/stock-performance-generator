
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
    return symbol