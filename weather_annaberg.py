"""
Goal:
Weather app for Annaberg, Lower Austria, with push notifications and a website

Was muss das Programm können (auf Deutsch, weil das nur meine eigene Übersicht ist und nicht drin bleibt):

1. Aktuelles Wetter anzeigen
2. Vorhersage für heute, morgen und übermorgen treffen können
3. Die Vorhersagen in frühe Morgenstunden, morgens - vormittags, mittags, nachmittags, abends - nachts unterteilen, weil sonst die Aussagen nutzlos sind für den Liftbetrieb
4. Bei Gewitter und Sturm(böen) die Zeit dazu ausspucken (wegen Liftbetrieb)
5. Liftbetrieb ist von 8 - 17 Uhr, im Winter von 8 - 16 Uhr. Das muss bei Vorhersagen dazu bedacht werden.

Wenn das läuft:

6. 5 verschiedene Modelle von Open Meteo vergleichen, Mittelwert ziehen 
7. auf 2 verschiedene Anbieter erweitern, je verschiedene Modelle berechnen, daraus dann absoluten Mittelwert ziehen

---------------------

To do:

1. Funktionierende Funktionen schreiben. Dann darauf aufbauen.

enthalten sein müssen:
Temperaturen (min, max, gefühlt)
Gewitterwahrscheinlichkeit
Regen/Schneewahrscheinlichkeit
Wind (Geschwindigkeit, Richtung, Böen)

Das Ergebnis soll sein:

16.08.2026:

Wetter: überwiegend sonnig
Regen/Schnee: unwahrscheinlich, am wahrscheinlichsten noch zwischen 15 - 16 Uhr
Gewitter: wahrscheinlich, zwischen 15 - 16 Uhr
Wind: überwiegend schwach aus Nordosten, zwischen 15 - 16 Uhr kräfige Böen möglich
Liftbetrieb: vorraussichtlich eingeschränkt

Dh:

1. 
"""

import requests #for the api datas
import weather_functions as wf
from datetime import date, timedelta #we need dates like "Today the 15.08.2026"

#we need the different dates to make exact forecasts
today_us = date.today()
today = today_us.strftime("%d.%m.%Y")
tomorrow_us = today_us + timedelta(days=1)
tomorrow = tomorrow_us.strftime("%d.%m.%Y")
da_tomorrow_us = today_us + timedelta(days=2)
day_after_tomorrow = da_tomorrow_us.strftime("%d.%m.%Y")
today_api = today_us.isoformat()

url = "https://api.open-meteo.com/v1/forecast"
#url2 = "https://dataset.api.hub.geosphere.at/v1/datasets" 

parameter = {
    "latitude": 47.8717277,
    "longitude": 15.3760583,
    "current": ",".join([  #data for today
        "temperature_2m",
        "apparent_temperature",
        "precipitation_probability",
        "weather_code",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
    ]),

    "hourly": ",".join([ #hourly forecast
        "temperature_2m",
        "apparent_temperature",
        "precipitation_probability",
        "weather_code",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
    ]),

    "minutely_15": "weather_code",

    "daily": ",".join([ #forecast for tomorrow
        "temperature_2m_min",
        "temperature_2m_max",
        "apparent_temperature_min",
        "apparent_temperature_max",
        "precipitation_probability_max",
        "weather_code",
        "wind_speed_10m_max",
        "wind_direction_10m_dominant",
        "wind_gusts_10m_max",
    ]),

    "wind_speed_unit": "kmh", 
    "timezone": "Europe/Vienna",
    "forecast_days": 3 #until incl. the day after tomorrow
}

result = requests.get(url, params=parameter) 

if not result.ok: #debugging
    print(result.json()) #what happens when we let us show "result"
    result.raise_for_status() #successful would be 200

data = result.json() #the json file with all the data

times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]
minutely_times = data["minutely_15"]["time"]
weather_codes = data["hourly"]["weather_code"]
w_codes_minutely = data["minutely_15"]["weather_code"]

#TEMPERATURE-PART------------------------------------------------------------

wf_morning, wf_late_morning, wf_noon, wf_afternoon, wf_evening = wf.temperature_function(times, temps, today_api)

morning = wf.average_values(wf_morning)
late_morning = wf.average_values(wf_late_morning)
noon = wf.average_values(wf_noon)
afternoon = wf.average_values(wf_afternoon)
evening = wf.average_values(wf_evening)

print(f"Temperaturen heute: Morgens: {morning} Grad, vormittags: "
      f"{late_morning} Grad, mittags: {noon} Grad, nachmittags: "
      f"{afternoon} Grad, abends: {evening} Grad")

#THUNDERSTORM PROBABILITY----------------------------------------------------

periods_raw = wf.thunderstorm_times(wf.thunderstorm_forecast(minutely_times,
                                               w_codes_minutely,
                                               today_api))

periods_formatted = []

for start, end in periods_raw:
    periods_formatted.append(f"von {start} bis {end} Uhr")

if periods_formatted:
    print("Gewittergefahr "+" und ".join(periods_formatted) + ".")
else:
    print("Heute besteht keine Gewittergefahr.")

#TEST-PART-------------------------------------------------------------------

"""


times= data["hourly"]["time"]
wind_speeds = data["hourly"]["wind_speed_10m"]
tomorrow_api = tomorrow_us.isoformat() #das Datumsformat, mit dem die Datennamen 
                                       #der einzelnen Stunden anfangen

print(times)

for time, wind_speed in zip(times, wind_speeds):
    if time.startswith(tomorrow_api):
        print(time, wind_speed)

"""
#TEST-PART-ENDE--------------------------------------------------------------------------

#---- Function for wind direction ---------------------------------------------------
#we want to have a word like southeast as a direction instead of just "225"

"""def direction_function(direction):
    if direction >= 337.5 or direction < 22.5:
        return "Norden"
    elif direction < 67.5:
        return "Nordosten"
    elif direction < 112.5:
        return "Osten"
    elif direction < 157.5:
        return "Südosten"
    elif direction < 202.5:
        return "Süden"
    elif direction < 247.5:
        return "Südwesten"
    elif direction < 292.5:
        return "Westen"
    elif direction < 337.5:
        return "Nordwesten"

current_direction = data["current"]["wind_direction_10m"]
today_direction = data["daily"]["wind_direction_10m_dominant"][0]
tomorrow_direction = data["daily"]["wind_direction_10m_dominant"][1]
dat_direction = data["daily"]["wind_direction_10m_dominant"][2]

current_winddirection = direction_function(current_direction)
today_winddirection = direction_function(today_direction)
tomorrow_winddirection = direction_function(tomorrow_direction)
dat_winddirection = direction_function(dat_direction)

#---- Function for wind speed -------------------------------------------------------

def speed_function(speed):
    if speed < 1:
        return "kein Wind."
    elif speed < 6:
        return f"ein leiser Zug mit {speed} km/h aus"
    elif speed < 12:
        return f"eine leichte Brise mit {speed} km/h aus"
    elif speed < 20:
        return f"ein schwacher Wind mit {speed} km/h aus"
    elif speed < 29:
        return f"ein mäßiger Wind mit {speed} km/h aus"
    elif speed < 39:
        return f"ein frischer Wind mit {speed} km/h aus"
    elif speed < 50:
        return f"ein starker Wind mit {speed} km/h aus"
    elif speed < 62:
        return f"ein steifer Wind mit {speed} km/h aus"
    elif speed < 75:
        return f"ein stürmischer Wind mit {speed} km/h aus"
    elif speed < 89:
        return f"Sturm mit {speed} km/h aus"
    elif speed < 103:
        return f"schwerer Sturm mit {speed} km/h aus"
    elif speed < 118:
        return f"ein orkanartiger Sturm mit {speed} km/h aus"
    else:
        return f"ein Orkan mit {speed} km/h aus"

current_speed = data["current"]["wind_speed_10m"]
current_windspeed = speed_function(current_speed)


#---- THE FORECAST -----------------------------------------------------------------
print("Aktuelles Wetter:")
print(f"Gerade weht {current_windspeed} {current_winddirection}.")
print("")
print(f"Wetter heute am {today}:")

print("")
print(f"Wetter morgen am {tomorrow}:")

print("")
print(f"Voraussichtliches Wetter übermorgen am {day_after_tomorrow}:")

print("")



"""
