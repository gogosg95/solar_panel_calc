import math
import matplotlib.pyplot as plt
from tabulate import tabulate

# създаване на таблица за битов товаров график мощност за един час от 0:00 в (kW), = b_i_час
b_i_1 = 3.0
b_i_2 = 2.93
b_i_3 = 2.96
b_i_4 = 2.96
b_i_5 = 3.0
b_i_6 = 3.04
b_i_7 = 4.5
b_i_8 = 4.56
b_i_9 = 4.5
b_i_10 = 3.83
b_i_11 = 3.08
b_i_12 = 3.0
b_i_13 = 3.08
b_i_14 = 3.0
b_i_15 = 3.08
b_i_16 = 3.15
b_i_17 = 3.23
b_i_18 = 3.9
b_i_19 = 4.86
b_i_20 = 4.35
b_i_21 = 4.5
b_i_22 = 4.28
b_i_23 = 3.08
b_i_24 = 3.0

# Таблица - Average hourly profiles - Direct normal irradiation [kWh/m2] - типова крива за слънчевата радиация в хубав пролетно-летен (октомври) ден по нашите географски ширини
c_i_1 = 0
c_i_2 = 0
c_i_3 = 0
c_i_4 = 0
c_i_5 = 0
c_i_6 = 0
c_i_7 = 0.121
c_i_8 = 0.290
c_i_9 = 0.363
c_i_10 = 0.414
c_i_11 = 0.435
c_i_12 = 0.449
c_i_13 = 0.443
c_i_14 = 0.403
c_i_15 = 0.336
c_i_16 = 0.213
c_i_17 = 0
c_i_18 = 0
c_i_19 = 0
c_i_20 = 0
c_i_21 = 0
c_i_22 = 0
c_i_23 = 0
c_i_24 = 0

# list night load - товари през нощта
list_night_load = [b_i_17, b_i_18, b_i_19, b_i_20, b_i_21, b_i_22, b_i_23, b_i_24, b_i_1, b_i_2, b_i_3, b_i_4, b_i_5,
                   b_i_6]


# list day load - товари през деня
list_day_load = [b_i_7, b_i_8, b_i_9, b_i_10, b_i_11, b_i_12, b_i_13, b_i_14, b_i_15,
                 b_i_16]

# list Average hourly profiles
list_average_hourly_profiles = [c_i_1, c_i_2, c_i_3, c_i_4, c_i_5, c_i_6, c_i_7, c_i_8, c_i_9, c_i_10, c_i_11, c_i_12,
                                c_i_13, c_i_14, c_i_15, c_i_16, c_i_17, c_i_18, c_i_19, c_i_20, c_i_21, c_i_22,
                                c_i_23, c_i_24]

# Нужна тотална мощност която батерията трябва да покрие през нощта (Capacity) в часовата рамка: 19:00-05:00 (p_night, kWh)
p_night = sum(list_night_load) / 0.7
print(f"тотална мощност която батерията  трябва да покрие (Capacity): {p_night:.2f}, kWh")

# пиков товар през нощта p_night_max който батерията трябва да покрие (Max Output)
p_night_max = max(list_night_load)
print(f"пиков товар който батерията трябва да покрие през ноща (Max Output): {p_night_max:.2f}, kW")

# цялостен товар които панелите трябва да покрият през деня + батерия (кпр 0,7). (p_day, kWh)
p_day = sum(list_day_load) + p_night
print(f"цялостен товар които панелите трябва по покрият през деня + батерия: {p_day:.2f}, kWh")

# цялостен товар през денят
p_day_total = sum(list_day_load)
print(f"цялостен товар  през деня : {p_day_total:.2f}, kWh")

# пиков товар през денят p_day_max който панелите трябва да покрият kW
p_day_max = max(list_day_load)
print(f"пиков товар през денят който панелите трябва да покрият: {p_day_max:.2f},kW")

# нужна площ според пиков товар през денят (l_max,m2)
c_day_max = max(list_average_hourly_profiles)
l_max = p_day_max / c_day_max

# тотална мощност акумулиране през денят p_day_total
multiplied_average_hourly_profiles = [element * l_max for element in list_average_hourly_profiles]
p_day_total = sum(multiplied_average_hourly_profiles)

# увеличаване на площа за покриване на нуждите на батерията
while p_day_total < p_day:
    l_max += 0.1 * l_max
    multiplied_average_hourly_profiles = [element * l_max for element in list_average_hourly_profiles]
    p_day_total = sum(multiplied_average_hourly_profiles)

print(f"нужна площ: {l_max:.2f},m2")

# взимам размер на един панела  1.6 m2. Нужен брой на PV панели n:
n = math.ceil(l_max / 1.6)
print(f"нужен брой панели: {n}")

# Взимам P_pan мощност на един панел 500W
p_pan = 500

# нужна мощност на инвертора i_needed
i_needed = n * p_pan / 1000
print(f"нужна мощност на инвертора: {math.ceil(i_needed)},kW")

# p = инсталирана фотоволтаична мощност
print(f"инсталирана фотоволтаична мощност: {i_needed:.2f},kW")

# графика генерирана мощност за всеки час
# list hours
hours_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
plt.plot(hours_day, multiplied_average_hourly_profiles)
plt.xlabel("x - часови диапазон")
plt.ylabel("y - генерирана мощност, kW")
plt.title("Генерирана мощност")
plt.show()

table_1 = [hours_day,  multiplied_average_hourly_profiles]
print(f"таблица генерирана мощност:\n{tabulate(table_1)}")

# графика за товар през нощта
# list нощтни часове
list_night_hours = ["17", "18", "19", "20", "21", "22", "23", "24", "1", "2", "3", "4", "5", "6"]
plt.plot(list_night_hours, list_night_load)
plt.xlabel("x - часови диапазон")
plt.ylabel("y - товар през нощта, kW")
plt.title("Товар през нощта")
plt.show()

table_2 = [list_night_hours, list_night_load]
print(f"таблица товар през нощта:\n{tabulate(table_2)}")

# графика на зареждане на батерията
list_power_generation = [c_i_7, c_i_8, c_i_9, c_i_10, c_i_11, c_i_12, c_i_13,
                         c_i_14, c_i_15, c_i_16]
hourly_generated_power = [element * l_max for element in list_power_generation]
battery_power = []
zip_object = zip(hourly_generated_power, list_day_load)
for hourly_generated_power_i, list_day_load_2 in zip_object:
    battery_power.append(hourly_generated_power_i-list_day_load_2)

hours_day_batt = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
plt.plot(hours_day_batt, battery_power)
plt.xlabel("x - часови диапазон")
plt.ylabel("y - батерия генерирана мощност, kW")
plt.title("Генериране на мощност - батерия")
plt.show()

table_3 = [hours_day_batt, battery_power]
print(f"таблица зареждане на батерията:\n{tabulate(table_3)}")

# графика на разреждане на батерията
accumulated_batt_power = sum(battery_power)
power_depletion = []

if accumulated_batt_power > 0:
    accumulated_batt_power = accumulated_batt_power - b_i_17
    power_depletion.append(accumulated_batt_power)
    if accumulated_batt_power > 0:
        accumulated_batt_power = accumulated_batt_power - b_i_18
        power_depletion.append(accumulated_batt_power)
        if accumulated_batt_power > 0:
            accumulated_batt_power = accumulated_batt_power - b_i_19
            power_depletion.append(accumulated_batt_power)
            if accumulated_batt_power > 0:
                accumulated_batt_power = accumulated_batt_power - b_i_20
                power_depletion.append(accumulated_batt_power)
                if accumulated_batt_power > 0:
                    accumulated_batt_power = accumulated_batt_power - b_i_21
                    power_depletion.append(accumulated_batt_power)
                    if accumulated_batt_power > 0:
                        accumulated_batt_power = accumulated_batt_power - b_i_22
                        power_depletion.append(accumulated_batt_power)
                        if accumulated_batt_power > 0:
                            accumulated_batt_power = accumulated_batt_power - b_i_23
                            power_depletion.append(accumulated_batt_power)
                            if accumulated_batt_power > 0:
                                accumulated_batt_power = accumulated_batt_power - b_i_24
                                power_depletion.append(accumulated_batt_power)
                                if accumulated_batt_power > 0:
                                    accumulated_batt_power = accumulated_batt_power - b_i_1
                                    power_depletion.append(accumulated_batt_power)
                                    if accumulated_batt_power > 0:
                                        accumulated_batt_power = accumulated_batt_power - b_i_2
                                        power_depletion.append(accumulated_batt_power)
                                        if accumulated_batt_power > 0:
                                            accumulated_batt_power = accumulated_batt_power - b_i_3
                                            power_depletion.append(accumulated_batt_power)
                                            if accumulated_batt_power > 0:
                                                accumulated_batt_power = accumulated_batt_power - b_i_4
                                                power_depletion.append(accumulated_batt_power)
                                                if accumulated_batt_power > 0:
                                                    accumulated_batt_power = accumulated_batt_power - b_i_5
                                                    power_depletion.append(accumulated_batt_power)
                                                    if accumulated_batt_power > 0:
                                                        accumulated_batt_power = accumulated_batt_power - b_i_6
                                                        power_depletion.append(accumulated_batt_power)

plt.plot(list_night_hours, power_depletion)
plt.xlabel("x - часови диапазон")
plt.ylabel("y - разреждане на батерията, kWh")
plt.title("разреждане  през нощта")
plt.show()

table_4 = [list_night_hours, power_depletion]
print(f"таблица разреждане на батерията:\n{tabulate(table_4)}")

# акумулирана мощност в батерията
batt_power_generated = sum(battery_power)
print(f"акумулирана мощност от батерията: {batt_power_generated:.2f},kW")