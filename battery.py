def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.
    '''
    global cur_temp  # in degrees Celsius
    cur_temp = 20
    global cur_charge  # in percentage points
    cur_charge = 50
    global cur_time  # in minutes
    global damage_counter
    damage_counter = 0

    global good_battery_health
    good_battery_health = True

    global battery_state
    battery_state = "idle"
    cur_time = 0
    good_battery_health = True

    global activities
    activities = {"idle": simulate_idle,
                  "use": simulate_usage, "charge": simulate_charge}


def simulate_activity(activity, duration):
    if activity in activities.keys():
        activities[activity](duration)


def simulate_idle(duration):
    global cur_charge, cur_temp, cur_time
    update_time(duration)
    cur_charge -= duration * 0.5
    if (cur_temp - duration) >= 0:
        cur_temp -= duration
    else:
        cur_temp = 0


def simulate_usage(duration):
    global cur_charge, cur_temp, cur_time
    update_time(duration)
    if (cur_charge - (duration * 2)) <= 0:
        duration -= cur_charge/2
        cur_temp += cur_charge/2
        cur_charge = 0
        simulate_dead(duration)
    else:
        cur_charge -= 2*duration
        cur_temp += duration


def simulate_charge(duration):
    global cur_temp, cur_charge, cur_time, good_battery_health

    # Ensures battery in bad health cant exceed 80% charge and time it doesnt charge is spent idle
    if not good_battery_health:
        if cur_charge + duration > 80:
            cur_temp += ((cur_charge + duration) - 80) * 0.25
        cur_charge = max(cur_charge + duration, 80)

    fast_charge = duration_fast_charge_possible()
    final_charge = (fast_charge * 3) + (duration - fast_charge)

    if final_charge >= 90 and damage_counter >= 2:
        good_battery_health = False
        cur_charge += fast_charge * 3
        cur_temp += fast_charge * 0.5

    if fast_charge > 0:
        duration -= fast_charge
        # Fast charging increases the temperature by 0.5°C per minute
        cur_temp += fast_charge * 0.5
        # Fast charging increases the charge by 3% per minute
        cur_charge += fast_charge * 3

    if duration > 0:
        # Slow charging increases the temperature by 0.25°C per minute
        cur_temp += duration * 0.25
        # Slow increases charge by 1% per minute
        cur_charge += duration
    if cur_charge > 80


def simulate_dead(duration):
    global cur_temp
    cur_temp = max(0, (cur_temp - duration))


# if temp 0-40 battery charge is below 80 % , and battery health is good.
def duration_fast_charge_possible():
    if (cur_temp < 40) and (cur_temp > 0) and (cur_charge < 80) and (good_battery_health):
        time_charge = (80 - cur_charge) / 3
        time_temp = (40 - cur_temp) / 0.5

        return min(time_temp, time_charge)
    else:
        return 0


def get_cur_temp() -> float:
    return cur_temp


def get_cur_charge() -> float:
    return cur_charge


def get_cur_battery_health() -> bool:
    return good_battery_health


def update_time(duration):
    global cur_time, damage_counter
    cur_time += duration
    if (cur_time/60) >= 6:
        cur_time = 0
        damage_counter = 0


def charge_time_needed(minutes):
    needed_charge = minutes*2
    fast_charge = duration_fast_charge_possible()
    slow_charge = needed_charge - (cur_charge + fast_charge*3)
    return fast_charge + slow_charge


def check_health():


if __name__ == '__main__':
    initialize()

    print(duration_fast_charge_possible())  # 10
    print(charge_time_needed(50))  # 30

    simulate_activity("charge", 30)
    print(get_cur_charge())  # 100
    print(get_cur_temp())  # 30

    simulate_activity("use", 50)
    print(get_cur_charge())  # 0
    print(get_cur_temp())  # 80

    simulate_activity("use", 10)
    print(get_cur_charge())  # 0
    print(get_cur_temp())  # 70

    simulate_activity("charge", 100)
    print(get_cur_charge())  # 100
    print(get_cur_temp())  # 95

    simulate_activity("idle", 100)
    print(get_cur_charge())  # 50
    print(get_cur_temp())  # 0
    print(get_cur_battery_health())  # True
    print(duration_fast_charge_possible())  # 10

    simulate_activity("charge", 80)
    print(get_cur_charge())  # 90
    print(get_cur_temp())  # 22.5
    print(get_cur_battery_health())  # False

    simulate_activity("use", 40)
    print(get_cur_charge())  # 10
    print(get_cur_temp())  # 62.5

    simulate_activity("charge", 80)
    print(get_cur_charge())  # 80
    print(get_cur_temp())  # 82.5

    initialize()
    # add your tests here
