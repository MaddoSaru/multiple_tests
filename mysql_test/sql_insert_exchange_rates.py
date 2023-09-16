from utils.functions.general_functions import add_currencies

add_currencies(
    table_name = 'cryptocompare_currencies_exchange_rates', 
    endpoint = 'histoday',
    method = 'fill'
)
