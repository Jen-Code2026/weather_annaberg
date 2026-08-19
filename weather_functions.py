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

def thunderstorm_hour(times, thunderstorms, target_date):
    thunderstorms_hour = []

    for time, thunderstorm in zip(times, thunderstorms):
        if time.startswith("target_date"):
            hour_raw = time[11:13]
            hour = hour_raw + ":00"

            if thunderstorm in (95, 96, 99):
                thunderstorms_hour.append(hour)
                
    return thunderstorms_hour