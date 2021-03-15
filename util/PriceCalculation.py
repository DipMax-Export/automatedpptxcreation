from util.CurrencyConv import CurrencyConv


def PriceCalculation(price, tgt_currency, margin):
    Curr_BDT_EUR = 103
    fee = 15  # Abwicklungsgebühr Penta
    fee_GB = 3.5
    fee_curr_ex = 0.005
    exc_rate_US = CurrencyConv("USD")
    exc_rate_GBP = CurrencyConv("GBP")

    if tgt_currency == "BDT":
        exc_rate = Curr_BDT_EUR
    else:
        exc_rate = CurrencyConv(tgt_currency)
    if "£" in price:
        price = ''.join(filter(str.isdigit, price))
        price = ((int(price)) / 1.20) / exc_rate_GBP #Nettoberechnung
        price = price + price * fee_curr_ex + fee_GB
    else:
        price = ''.join(filter(str.isdigit, price))

    price_eur = int(price) * (1 + (int(margin) / 100))
    price_usd = int(price_eur * exc_rate_US + (price_eur * exc_rate_US) * fee_curr_ex)
    price_curr = int(price_eur * exc_rate + (price_eur * exc_rate) * fee_curr_ex)

    # Formatting
    price_eur = '{:20,.2f}'.format(price_eur) + " EUR"
    price_usd = '{:20,.2f}'.format(price_usd) + " USD"
    price_curr = '{:20,.0f}'.format(price_curr) + " " + tgt_currency

    return price_eur.lstrip(), price_usd.lstrip(), price_curr.lstrip()
