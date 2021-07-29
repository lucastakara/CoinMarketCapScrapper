
import requests
from bs4 import BeautifulSoup

from config import Paths
from event_writer import EventWriter


class CoinMarketCapScrapper:

    def __init__(self):
        self.event_writer = EventWriter()
        self.data = []
        self.save_results = True

    def get_html_page(self, URL):
        script = '''
            headers = {
                ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                ['cookie'] = 'bm_sv=8348027EADF53A62B0A88A2489F9E63A~/Z/M+RBmRemmCIlsBEfDmqtib6poRJXX7QobxdWDCOwYAJijRtzG2DcRFwGEVGBTo2oGg8NXwdvhBSyFPS6u3aO+vPZNILLcIB37Pr6pfDvInSDjZprAYED/dfjU3CWj977GaHNsIKR1PFTUcIJmIoK/scopOeqmPdS4KvJM27o=; Domain=.gearbest.com; Path=/; Max-Age=6422; HttpOnly'
            }
            splash:set_custom_headers(headers)
            splash.private_mode_enabled = false
            splash.images_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            return splash:html()
        '''

        html_content = requests.post(url='http://localhost:8050/run',
                                     json={
                                         'lua_source': script,
                                         'url': URL
                                     })

        return html_content

    def proccess_text(self, html):
        raw_text = BeautifulSoup(html.text, 'lxml')
        processed_text = raw_text.find('table', class_='h7vnx2-2 bFpGkc cmc-table')
        return processed_text

    def get_coin_symbol(self):
        symbol = self.row.find('p', class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").text
        return symbol

    def get_volume_currencies(self):
        volume2 = self.row.find_all('p', class_="sc-1eb5slv-0 etpvrL")
        if len(volume2) > 0:
            volume2 = volume2[1].text
            return volume2

    def get_weekly_variation(self):
        self.row_variations_positive = self.row.find_all('span', class_='sc-15yy2pl-0 kAXKAX')
        self.row_variations_negative = self.row.find_all('span', class_='sc-15yy2pl-0 hzgCfk')

        if self.row_variations_positive is not None and len(self.row_variations_positive) > 1:
            daily_variation_column_positive = self.row_variations_positive[1]
            day_variation_value_positive = daily_variation_column_positive.text
            value = "+" + day_variation_value_positive
            return value

        if self.row_variations_negative is not None and len(self.row_variations_negative) > 1:
            daily_variation_column_negative = self.row_variations_negative[1]
            day_variation_value_negative = daily_variation_column_negative.text
            value = "-" + day_variation_value_negative
            return value

    def get_daily_variation(self):
        self.row_variations_positive = self.row.find_all('span', class_='sc-15yy2pl-0 kAXKAX')
        self.row_variations_negative = self.row.find_all('span', class_='sc-15yy2pl-0 hzgCfk')

        if self.row_variations_positive is not None and len(self.row_variations_positive) > 0:
            daily_variation_column_positive = self.row_variations_positive[0]
            day_variation_value_positive = daily_variation_column_positive.text
            value = "+" + day_variation_value_positive
            return value

        if self.row_variations_negative is not None and len(self.row_variations_negative) > 0:
            daily_variation_column_negative = self.row_variations_negative[0]
            day_variation_value_negative = daily_variation_column_negative.text
            value = "-" + day_variation_value_negative
            return value

    def get_coin_url(self):
        coin_url = self.row.find('div', class_='sc-16r8icm-0 escjiH')
        coin_url = coin_url.find('a', class_='cmc-link', href=True)
        coin_url = coin_url['href']
        coin_url = 'https://coinmarketcap.com' + coin_url
        return coin_url

    def get_coin_price(self):
        price = self.row.find('div', class_='sc-131di3y-0 cLgOOr').text
        return price

    def get_market_captalization(self):
        market_cap = self.row.find('span', class_='sc-1ow4cwt-1 ieFnWP').text
        return market_cap

    def get_volume_usd(self):
        volume = self.row.find('p', class_='sc-1eb5slv-0 kDEzev font_weight_500___2Lmmi').text
        return volume

    def get_circulating_supplies(self):
        circulating_supply = self.row.find('p', class_="sc-1eb5slv-0 hNpJqV").text
        return circulating_supply


    def run(self):
        html = scrapper.get_html_page(URL='https://coinmarketcap.com/')
        processed_text = scrapper.proccess_text(html)
        for self.row in processed_text.find_all('tr'):
            try:
                symbol = self.get_coin_symbol()
                coin_price = scrapper.get_coin_price()
                url = scrapper.get_coin_url()
                daily_variation = scrapper.get_daily_variation()
                weekly_variation = scrapper.get_weekly_variation()
                market_cap = scrapper.get_market_captalization()
                volume_usd = scrapper.get_volume_usd()
                volume_currencies = scrapper.get_volume_currencies()
                circulating_supplies = scrapper.get_circulating_supplies()
                if self.save_results:
                    self.event_writer.append_events_list(symbol, coin_price, url, daily_variation,
                                                         weekly_variation, market_cap, volume_usd, volume_currencies,
                                                         circulating_supplies)
            except AttributeError:
                continue

            finally:
                self.event_writer.save_events_to_csv(Paths.CSV_PATH)
                self.event_writer.save_events_to_json(Paths.JSON_PATH)


if __name__ == '__main__':
    scrapper = CoinMarketCapScrapper()
    scrapper.run()
