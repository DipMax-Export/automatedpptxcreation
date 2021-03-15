from forex_python.converter import CurrencyRates


# Currency berechnungen
def CurrencyConv(input_curr):
    c = CurrencyRates()
    exchange_rate = c.get_rate("EUR", input_curr)  # convert curr

    return exchange_rate
