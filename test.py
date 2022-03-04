def get_file(x):
    switcher = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        'comment': 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }
    return switcher.get(x, "nothing")


print(get_file('comment'))
