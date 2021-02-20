import requests
import time
import hashlib
import urllib.parse


def mainFunc():
    # your ip address or other ip
    ip = requests.get("https://gianlu.dev/ip").text.strip()

    server_ip = "any"
    port = "22"
    proto = "tcp"
    initial_password = "hellop#firstsec"
    custom_path = "goUeffe"

    duration = 1

    secret_key = "z2Xm3m4Dr:/Rm2Gv5WdpCpDLdYVrqCgpcftYqMiqSXLu3esqzwfgpwxKqyDm765UnJttuw2CtxV2bunpTwmqvLeFTfrzdkA3Q6pNNGPwvrTDCBHFN4jPyWAj7X7wPrX7feiKxRni2PZc6go3Ksd7HETh6HbGRZgiZKtSdQohfwK9qNYWGF5975ePgGLTgykGGpFik3AmhxKRWN7NxzUVdotWkdzdkVCzLkGcVzi8C9BqDt9vekshWZoCvVNo8zFnph7ZvCN6n9ZrHpyhfaNNddPAPxCsDzWxRVbK7tHkrbvdPUxmM5D87LcmQBwDfJybvspvy23ZbCcufKER6xSXizMBxG3m6gZjj4nopRrRHVSieB4YEf2pCAeXH3GghMEJ3bEtFuGCeacQ8y3PgDZaoyZD92Lq6t6raRjdSxzYrHq4h7VGTRrBNzorsXD3VffkWusQCVigwgr6difcSxdUK7qVd4rX5VdJv"

    now = int(time.time())
    command = f"allow from {ip} to {server_ip} port {port} proto {proto}"

    concat_value = secret_key + ":" + command + ":" + \
        str(now) + ":" + str(duration) + ":" + initial_password

    concat_value = concat_value.encode("utf8")

    sign = hashlib.sha512(concat_value).hexdigest()

    command_quoted = urllib.parse.quote_plus(command)
    initial_password_quoted = urllib.parse.quote_plus(initial_password)

    url = f"https://gianlu.dev/{custom_path}?command={command_quoted}&password={initial_password_quoted}&sign={sign}&time={now}&duration={duration}"

    r = requests.get(url)
    print(r.text)


if __name__ == "__main__":
    mainFunc()
