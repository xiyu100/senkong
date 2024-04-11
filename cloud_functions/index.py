import logging
import os.path
import threading
import skyland
from skyland import send_pushbullet_notification

# 华为云本地文件在./code下面
# 注：cred过几个小时就会失效，不要使用它，得用鹰角通行证账号获得它
# file_save_name = f'{os.path.dirname(__file__)}/creds.txt'
file_save_token = f'{os.path.dirname(__file__)}/INPUT_HYPERGRYPH_TOKEN.txt'
file_save_pushbullet_token = f'{os.path.dirname(__file__)}/INPUT_PUSHBULLET_TOKEN.txt'


def read(path):
    v = []
    with open(path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            i = i.strip()
            i and i not in v and v.append(i)
    return v


def handler(event, context):
    tokens = read(file_save_token)
    pushbullet_tokens = read(file_save_pushbullet_token)

    if tokens and pushbullet_tokens and len(tokens) == len(pushbullet_tokens):
        for i in range(1, len(tokens)):
            threading.Thread(target=start, args=(tokens[i], pushbullet_tokens[i])).start()
        start(tokens[0], pushbullet_tokens[0])
    else:
        logging.error("Token文件内容无效或数量不匹配")
    return {
        "statusCode": 200,
    }


def start(token, pushbullet_token):
    try:
        cred = skyland.login_by_token(token)
        skyland.do_sign(cred, pushbullet_token)
    except Exception as ex:
        error_message = f'签到完全失败了！：{str(ex)}'
        logging.error(error_message, exc_info=ex)

        # 将错误消息发送给Pushbullet
        send_pushbullet_notification(pushbullet_token, "签到失败", error_message)
