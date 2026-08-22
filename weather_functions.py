#functions to import into the main source file

"""
Idee:

zeit:

start des tages: 0 - 6 uhr
vormittags: 6 - 11 uhr
mittags: 11 - 14 uhr
nachmittags: 14 - 19 uhr
abends: 19 - 0 uhr

wettercodes zb. so ausgeben:
wenn 1 - 2 gleich und zb regen, und 3 - 5 auch gleich und kein regen: startet regnerisch, gegen mittag hört der regen auf
wenn 1, 3 und 5 gleich: immer wieder kommt es zu regen 

mögliche Kombinationen:

1 - 5 gleich: ganzer Tag
1 - 4 gleich: ganzen Tag, gegen Abend ...
2 - 5 gleich: startet x, dann den Rest des Tages yp
1 - 3 und 4 - 5 gleich: bis Mittag x, ab Nachmittag y
1 - 2 gleich 3 - 5 gleich: startet x, ab Mittag y
1 - 3 + 5 gleich: den ganzen Tag, nachmittags (vormittags, mittags) unterbrochen von (das geht für alle Kombis in der Art: 1 + 3 - 5 gleich, 1 + 2 + 4 + 5 gleich)
1 - 3 gleich, 4 und 5 jeweils anders: bis zum frühen Nachmittag x, danach wechselhaft
nichts gleich oder nur max. 2 Werte gleich: Wetter wechselhaft, höchste Niederschlagswahrscheinlichkeit gegen zb. Nachmittag
3 x dasselbe Wetter, unzusammenhängend: im Tagesverlauf immer wieder x, unterbrochen von y (unterscheiden sich die beiden anderen punkte auch: + gegen Mittag und z am Abend)
2 - 4 gleich, 1 und 5 unterschiedlich: startet x, dann über den Tag y, zum Abend hin z
2 - 4 gleich, 1 + 5: startet mit x, über den Tag y, gegen Abend wieder x
3 - 5 gleich, 1 und 2 verschieden: startet wechselhaft, ab Mittag dann


"""

#--- Temperature Functions

def temperature_function(times, temps, target_date):
    wf_morning = []
    wf_late_morning = []
    wf_noon = []
    wf_afternoon = []
    wf_evening = []

    for time, temp in zip(times, temps):
        if time.startswith(target_date):
            hour_raw = time[11:13]
            hour = int(hour_raw)

            if hour in range(0, 6):
                wf_morning.append(temp)
            elif hour in range(6, 11):
                wf_late_morning.append(temp)
            elif hour in range(11, 14):
                wf_noon.append(temp)
            elif hour in range(14, 19):
                wf_afternoon.append(temp)
            else:
                wf_evening.append(temp)

    return wf_morning, wf_late_morning, wf_noon, wf_afternoon, wf_evening


#---- Average values 

def average_values(werte):
    average_raw = sum(werte) / len(werte)
    average = round(average_raw, 1)
    return average

#---- Probability for a thunderstorm

def thunderstorm_forecast(minutely_times, w_codes_minutely, today_api):
    thunderstorm_periods = []

    for minutely_time, code in zip(minutely_times, w_codes_minutely):
        if minutely_time.startswith(today_api):
            if code in (95, 96, 99):
                minutes_raw = minutely_time[11:16]
                hour, minute = map(int, minutes_raw.split(":")) 
                total_minutes = (hour * 60) + minute

                thunderstorm_periods.append([minutes_raw, total_minutes])
    return thunderstorm_periods

def thunderstorm_times(thunderstorm_forecast):
    if not thunderstorm_forecast:
        return []
    
    start = thunderstorm_forecast[0][0]
    end = thunderstorm_forecast[0][0]
    previous_minutes = thunderstorm_forecast[0][1]
    from_to_periods = []

    for time, total_minute in thunderstorm_forecast[1:]:
        difference = total_minute - previous_minutes

        if difference > 15:
            from_to_periods.append([start, end])
            start = time

        end_minutes = total_minute + 15
        end_hour = end_minutes // 60
        end_minute = end_minutes % 60
        end = f"{end_hour:02d}:{end_minute:02d}"
        
        previous_minutes = total_minute

    from_to_periods.append([start, end])

    return from_to_periods