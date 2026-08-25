#functions to import into the main source file

"""
Daytimes:

morning: 0 - 6 uhr
late morning: 6 - 11 uhr
noon: 11 - 14 uhr
afternoon: 14 - 19 uhr
evening: 19 - 0 uhr

* Output weather codes, for example, like this:

* If 1-2 are the same, e.g. rain, and 3-5 are also the same, e.g. no rain: starts rainy, rain stops around midday.

* If 1, 3, and 5 are the same: rain occurs repeatedly throughout the day.

Possible combinations:

* 1-5 the same: all day
* 1-4 the same: all day, then towards the evening ...
* 2-5 the same: starts with x, then y for the rest of the day
* 1-3 and 4-5 the same: x until midday, y from the afternoon onwards
* 1-2 the same and 3-5 the same: starts with x, y from midday onwards
* 1-3 + 5 the same: x throughout the day, interrupted by y in the afternoon (morning, midday). This also applies to all combinations of this type, e.g. 1 + 3-5 the same, 1 + 2 + 4 + 5 the same.
* 1-3 the same, while 4 and 5 are each different: x until early afternoon, then changeable weather
* Nothing is the same, or no more than 2 values are the same: changeable weather, with the highest precipitation probability around e.g. the afternoon
* The same weather occurs 3 times non-consecutively: x occurs repeatedly throughout the day, interrupted by y. If the other two points also differ: + y around midday and z in the evening
* 2-4 the same, with 1 and 5 different: starts with x, then y throughout the day, changing to z towards the evening
* 2-4 the same, with 1 and 5 the same: starts with x, y throughout the day, then x again towards the evening
* 3-5 the same, with 1 and 2 different: starts changeable, then y from midday onwards

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

#RAIN & SNOW

def rainfall_forecast(minutely_times, w_codes_minutely, today_api):
    rainfall_periods = []

    for minutely_time, code in zip(minutely_times, w_codes_minutely):
        if minutely_time.startswith(today_api):
            if code in(51,53,55):
                rainfall_type = "Nieselregen, am wahrscheinlichsten"
            elif code in(56,57,66):
                rainfall_type = "Eisregen, am wahrscheinlichsten"
            elif code == 67:
                rainfall_type = "starker Eisregen, am wahrscheinlichsten"
            elif code in(61, 63, 80, 81):
                rainfall_type = "Regen, am wahrscheinlichsten"
            elif code in(65, 82):
                rainfall_type = "starker Regen, am wahrscheinlichsten"
            elif code in(71,73,77,85):
                rainfall_type = "Schneefall, am wahrscheinlichsten"
            elif code in(75,86):
                rainfall_type = "starker Schneefall, am wahrscheinlichsten"
            else:
                continue

            minutely_raw = minutely_time[11:16]
            hour, minute = map(int, minutely_raw.split(":"))
            total_minutes = hour * 60 + minute

            rainfall_periods.append([minutely_raw, total_minutes, rainfall_type])
    return rainfall_periods

def rainfall_times(rainfall_forecast):
    if not rainfall_forecast:
        return []

    start = rainfall_forecast[0][0]
    end = rainfall_forecast[0][0]
    previous_minutes = rainfall_forecast[0][1]
    previous_rainfall_type = rainfall_forecast[0][2]
    from_to_periods = []

    for time, total_minute, rainfall_type in rainfall_forecast[1:]:
        difference = total_minute - previous_minutes

        if difference > 15 or rainfall_type != previous_rainfall_type:
            from_to_periods.append([start, end, previous_rainfall_type])
            start = time
        
        end_minutes = total_minute + 15
        end_hour = end_minutes // 60
        end_minute = end_minutes % 60
        end = f"{end_hour:02d}:{end_minute:02d}"
                
        previous_minutes = total_minute
        previous_rainfall_type = rainfall_type
        
    from_to_periods.append([start, end, previous_rainfall_type])
        
    return from_to_periods