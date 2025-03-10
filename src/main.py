from time import sleep

from captchaVerification import *


def reserve(config, start_time, end_time, ground_index):
    url = "https://reservation.sustech.edu.cn/api/blade-app/qywx/saveOrder?userid=" + config["student_id"] \
          + "&token=" + config["token"]
    captchaVerification = str(Verification())[2:-1]  # The original value seems like b'xxxxxxxx', so I use [2:-1]
    data = {
        "customerName": config["student_name"],
        "customerId": "1433554008613634050",
        "customerTel": config["student_tel"],
        "userNum": 1,
        "customerEmail": "",
        "gymId": "1297443858304540673",
        "gymName": "润杨羽毛球馆",
        "groundId": config["ground_url"][str(ground_index)],
        "groundName": config["ground_name"][str(ground_index)],
        "groundType": "0",
        "messagePushType": "0",
        "isIllegal": "0",
        "orderDate": config["order_time"],
        "startTime": start_time,
        "endTime": end_time,
        "tmpOrderDate": config["order_time"],
        "tmpStartTime": start_time,
        "tmpEndTime": end_time,
        "captchaVerification": captchaVerification
    }
    headers = config["headers"]
    try:
        re = requests.post(url, json=data, headers=headers)
        re_data = json.loads(re.text)
        if re_data["success"]:
            print("You have reserved Ground " + str(ground_index) + " from " + start_time + " to " + end_time)
            return True
        else:
            print(f"Failed to reserve Ground {ground_index} from {start_time} to {end_time} --> {re.text}")
            return False
    except requests.RequestException as e:
        print(f"{e}")
        return False


if __name__ == "__main__":
    config = get_config()
    for start_time, end_time in zip(config["start_time"], config["end_time"]):
        for ground_id in list(config["ground_url"].keys()):
            if ground_id == "3" or ground_id == "4" or ground_id == "8" or ground_id == "10":
                continue
            print(f"Reserve Ground {ground_id} from {start_time} to {end_time}")
            result = False
            try:
                result = reserve(config, start_time, end_time, ground_id)
            except Exception as e:
                pass
            if result:
                break
