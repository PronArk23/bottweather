import telebot
# weather
from bs4 import BeautifulSoup
import requests
# for system
import time

# weather parse
def Weather():
	URL = 'https://yandex.ru/pogoda/yaroslavl?lat=57.640057&lon=39.838684'
	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 YaBrowser/20.7.2.124 Yowser/2.5 Safari/537.36'
	}

	response = requests.get(URL, headers = HEADERS)
	soup = BeautifulSoup(response.content, 'html.parser')

	temperature = soup.find('div', class_ = 'temp fact__temp fact__temp_size_s').find('span', class_ = 'temp__value').get_text()
	temperatureAs = soup.find('div', class_ = 'term term_orient_h fact__feels-like').find('span', class_ = 'temp__value').get_text()
	temperatureYesterday = soup.find('div', class_ = 'term term_orient_h fact__yesterday').find('span', class_ = 'temp__value').get_text()
	# clouds = soup.find('div', class_ = 'cloud tooltip').get_text(strip = True)
	waitRain = soup.find('p', class_ = 'maps-widget-fact__title').get_text(strip = True)
	humidity = soup.find('div', class_ = 'term term_orient_v fact__humidity').get_text(strip = True)
	pressure = soup.find('div', class_ = 'term term_orient_v fact__pressure').get_text(strip = True)
	# sunrise = soup.find('div', class_ = 'sunrise_set tooltip').get_text(strip = True)
	speedOfWind = soup.find('div', class_ = 'term term_orient_v fact__wind-speed').get_text(strip = True)


	resoultTemp = 'Текущая температура: ' + temperature + '°\n'
	resoultTempAs = 'Ощущается как: ' + temperatureAs + '°\n'		
	resoultTempYesterday = 'Вчера в это время: ' + temperatureYesterday + '°\n'
	resoultWaitRain = waitRain
	# resoultClouds = clouds + '\n'
	resoultHumidity = 'Влажность: ' + humidity + '\n'
	# resoultPressure = 'Давление: ' + pressure + '\n'
	# resoultSunrise = sunrise + '\n'
	resoultWind = 'Скорость ветра: ' + speedOfWind + '\n'

	resoults = resoultTemp + resoultTempAs + resoultTempYesterday + resoultWind + resoultHumidity + resoultWaitRain

	return(resoults)

# telebot


bot = telebot.TeleBot()

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
	if message.text == 'Привет':
		bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
	elif message.text == 'Погода':
		bot.send_message(message.from_user.id, 'Секунду, ищу информацию')
		time.sleep(1)
		bot.send_message(message.from_user.id, Weather())

	elif message.text == '/help':
		bot.send_message(message.from_user.id, 'Напиши привет')
	else:
		bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help.')



# none stop
bot.polling(none_stop=True, interval=0)