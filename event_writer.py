import pandas as pd


class EventWriter:

    def __init__(self):
        self.coin_market_cap_items = []
        self.row_id = 0

    def append_events_list(self, names, prices, urls, daily_variation, weekly_variation, market_cap,
                           volume_usd, volume_currencies, circulating_supply):
        self.coin_market_cap_items.append(
            (self.row_id, names, prices, urls, daily_variation, weekly_variation, market_cap,
             volume_usd, volume_currencies, circulating_supply))
        self.row_id += 1

    def save_events_to_csv(self, csv_path):
        dataframe = pd.DataFrame(self.coin_market_cap_items, columns= range(10))
        column_names = ['row_id', 'name', 'price', 'url', '24h_%', '7d%', 'Market_Cap', 'Volume(24h)', 'Volume(2)',
                        'Circulating_Supply']
        dataframe.columns = column_names
        dataframe.to_csv(csv_path)

    def save_events_to_json(self, json_path):
        dataframe = pd.DataFrame(self.coin_market_cap_items, columns= range(10))
        column_names = ['row_id', 'name', 'price', 'url', '24h_%', '7d%', 'Market_Cap', 'Volume(24h)', 'Volume(2)',
                        'Circulating_Supply']
        dataframe.columns = column_names

        dataframe.to_json(json_path)
