from flask import Flask, make_response
import pytz
from datetime import datetime, timedelta
from flask_cors import CORS
from helper import request

app = Flask(__name__)
CORS(app, max_age=31536000, supports_credentials=True)


def time_calculate(hour, min):
    # input_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=hour, minute=min))
    input_time = datetime.now().astimezone(pytz.timezone('Asia/Seoul')).replace(hour=hour, minute=min,
                                                                                         second=0, microsecond=0)
    kst_now = datetime.now().astimezone(pytz.timezone('Asia/Seoul'))
    # input_time = input_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))

    if input_time.hour < kst_now.hour:
        input_time = input_time.replace(day=input_time.day + 1)
    elif input_time.hour == kst_now.hour:
        if input_time.minute < kst_now.minute:
            input_time = input_time.replace(day=input_time.day + 1)

    time_one = input_time - timedelta(minutes=465)
    time_two = input_time - timedelta(minutes=375)
    time_three = input_time - timedelta(minutes=285)

    return kst_now, time_one, time_two, time_three


def time_transform(input_time):
    try:
        ampm = "오후" if input_time.hour > 12 else "오전"
        sleep_hour = input_time.hour - 12 if input_time.hour > 12 else input_time.hour
        if sleep_hour == 0:
            sleep_hour = 12

        result = f"{ampm} {sleep_hour}시"

        if input_time.minute != 0:
            result += f" {input_time.minute}분"

        return result

    except AttributeError:

        sleep_hour = input_time.seconds // 3600
        sleep_min = input_time.seconds % 3600 // 60

        if sleep_hour != 0:
            result = f"{sleep_hour}시간"
            if sleep_min != 0:
                result += f" {sleep_min}분"
        else:
            result = f"{sleep_min}분"

        return result


@app.route("/answer.go_to_bed_time", methods=['POST', 'GET'])
def go_to_bet_time():
    data = request.get_json(silent=True, force=True)['action'].get('parameters')
    wakeup_time_duration = data.get('wakeup_time_duration').get('value')
    wakeup_time_hour = data.get('wakeup_time_hour').get('value')
    wakeup_time_min = data.get('wakeup_time_min', dict()).get('value', '0')

    wakeup_time_hour = int(wakeup_time_hour)
    wakeup_time_min = int(wakeup_time_min)

    if wakeup_time_duration == "오전":
        if wakeup_time_hour > 12:
            return make_response({"resultCode": "exception_common",
                                  "output": "exception_common"})
    else:
        if wakeup_time_hour < 12:
            wakeup_time_hour += 12

    kst_now, time_one, time_two, time_three = time_calculate(wakeup_time_hour, wakeup_time_min)

    output_times = dict()

    print(f"wakeup_time_hour = {wakeup_time_hour}")
    print(f"wakeup_time_min = {wakeup_time_min}")
    print(kst_now)
    print(time_one)
    print(time_two)
    print(time_three)

    if kst_now < time_one:
        output_times['best_sleep_time1'] = time_transform(time_one)
        output_times['best_sleep_time2'] = time_transform(time_two)
        output_times['best_sleep_time3'] = time_transform(time_three)
        output_times['remain_time'] = time_transform(time_one - kst_now)
    elif time_one < kst_now < time_two:
        output_times['best_sleep_time2'] = time_transform(time_two)
        output_times['best_sleep_time3'] = time_transform(time_three)
        output_times['remain_time'] = time_transform(time_two - kst_now)
    elif time_two < kst_now < time_three:
        output_times['best_sleep_time3'] = time_transform(time_three)
        output_times['remain_time'] = time_transform(time_three - kst_now)
    elif time_three < kst_now:
        output_times['default_lack_of_sleep'] = "True"

    # output 형태느 다음과 같다.
    output = {
        "resultCode": "OK",
        "output": output_times
    }

    return make_response(output)


@app.route("/time1", methods=['POST'])
def time_one():
    data = request.get_json(silent=True, force=True)['action'].get('parameters')

    output_times = dict()
    print(data)

    output_times['best_sleep_time1'] = data['best_sleep_time1'].get('value')
    output_times['remaine_time'] = data['remain_time'].get('value')

    output = {
        "resultCode": "OK",
        "output": output_times
    }

    return make_response(output)


@app.route("/time2", methods=['POST'])
def time_two():
    data = request.get_json(silent=True, force=True)['action'].get('parameters')

    output_times = dict()
    print(data)

    output_times['best_sleep_time2'] = data['best_sleep_time2'].get('value')
    output_times['remain_time'] = data['remain_time'].get('value')

    output = {
        "resultCode": "OK",
        "output": output_times
    }

    return make_response(output)


@app.route("/time3", methods=['POST'])
def time_three():
    data = request.get_json(silent=True, force=True)['action'].get('parameters')

    output_times = dict()
    print(data)

    output_times['best_sleep_time3'] = data['best_sleep_time3'].get('value')
    output_times['remain_time'] = data['remain_time'].get('value')

    output = {
        "resultCode": "OK",
        "output": output_times
    }

    return make_response(output)


@app.route("/later_time1", methods=['POST'])
def later_time_one():
    data = request.get_json(silent=True, force=True)['action'].get('parameters')

    output_times = dict()
    print(data)

    output_times['best_sleep_time2'] = data['best_sleep_time2'].get('value')
    output_times['best_sleep_time3'] = data['best_sleep_time3'].get('value')

    output = {
        "resultCode": "OK",
        "output": output_times
    }

    return make_response(output)


@app.route("/later_time2", methods=['POST'])
def later_time_two():
    data = request.get_json(silent=True, force=True)['action'].get('parameters')

    output_times = dict()
    print(data)

    output_times['best_sleep_time3'] = data['best_sleep_time3'].get('value')

    output = {
        "resultCode": "OK",
        "output": output_times
    }

    return make_response(output)


@app.route("/default_lack_of_sleep", methods=['POST', 'GET'])
def default_lack_of_sleep():
    output = {
        "resultCode": "OK",
        "output": dict()
    }

    return make_response(output)


@app.route("/")
def default():
    return "배포"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)

