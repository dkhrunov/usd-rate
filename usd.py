import requests
import time
from datetime import datetime
 
USD_API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/neKPCYhNiYQYGyBNsgelTEqGep5uE1x5ADHkH-gtKBt'
 
def get_latest_usd_price():
    response = requests.get(USD_API_URL)
    response_json = response.json()
    # Конвертирует курс в число с плавающей запятой
    return float(response_json['Valute']['USD']['Value'])
 
 
def post_ifttt_webhook(event, value):
    data = {'value1': value}
    # Вставка желаемого события
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Отправка запроса HTTP POST в URL вебхука
    requests.post(ifttt_event_url, json=data)

def format_usd_history(usd_history):
    rows = []
    for usd_price in usd_history:
        # Форматирует дату в строку: '24.02.2018 15:09'
        #date = usd_price['date'].strftime('%d.%m.%Y %H:%M')
        price = usd_price['price']
        # тег <b> делает текст полужирным
        # 24.02.2018 15:09: $<b>10123.4</b>
        #row = '{}: $<b>{}</b>'.format(date, price)
        row = '{0:.2f}'.format(price)
        rows.append(row)
 
    # Используйте тег <br> для создания новой строки
    return '<br>'.join(rows)

USD_PRICE_THRESHOLD = 60  # Настройте так, как вам угодно
 
def main():
    usd_history = []
    while True:
        price = get_latest_usd_price()
        #date = datetime.now()
        #usd_history.append({'date': date, 'price': price})
        usd_history.append({'price': price})
 
        # Отправка срочного уведомления
        if price <= USD_PRICE_THRESHOLD:
            post_ifttt_webhook('usd_price_update', price)
 
        # Отправка уведомления Telegram
        # После получения 5 объектов в usd_history – отправляем обновление
        if len(usd_history) == 1:
            post_ifttt_webhook('usd_price_update', 
                               format_usd_history(usd_history))
            # Сброс истории
            usd_history = []
 
        # Сон на 5 минут
        # (Для тестовых целей вы можете указать меньшее число)
        time.sleep(10)
 
if __name__ == '__main__':
    main()