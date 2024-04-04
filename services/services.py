# Функция возвращающая количество заправленных литров
def total_liters(spent_money, price_per_liter) -> float:
    return round(float(spent_money)/float(price_per_liter), 2)

# Функция возвращающая расход топлива
def fuel_consumption_f(total_litr, mileage) -> float:
    return round((float(total_litr)/float(mileage))*100, 2)

# Функция, которая рассчитывает среднюю скорость
def average_speed(time_min, distance_km) -> float:
    return round(float(distance_km)/(float(time_min)/60), 2)