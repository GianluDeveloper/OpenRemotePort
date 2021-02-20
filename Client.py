import requests
import time
import hashlib
import urllib.parse

# your ip address or other ip
ip = requests.get("https://gianlu.dev/ip").text.strip()

serverIp = "any"
port = "22"
proto = "tcp"
initialPassword = "hellop#firstsec"
customPath = "goUeffe"

duration = 1


secretKey = "z2Xm3m4Dr:/Rm2Gv5WdpCpDLdYVrqCgpcftYqMiqSXLu3esqzwfgpwxKqyDm765UnJttuw2CtxV2bunpTwmqvLeFTfrzdkA3Q6pNNGPwvrTDCBHFN4jPyWAj7X7wPrX7feiKxRni2PZc6go3Ksd7HETh6HbGRZgiZKtSdQohfwK9qNYWGF5975ePgGLTgykGGpFik3AmhxKRWN7NxzUVdotWkdzdkVCzLkGcVzi8C9BqDt9vekshWZoCvVNo8zFnph7ZvCN6n9ZrHpyhfaNNddPAPxCsDzWxRVbK7tHkrbvdPUxmM5D87LcmQBwDfJybvspvy23ZbCcufKER6xSXizMBxG3m6gZjj4nopRrRHVSieB4YEf2pCAeXH3GghMEJ3bEtFuGCeacQ8y3PgDZaoyZD92Lq6t6raRjdSxzYrHq4h7VGTRrBNzorsXD3VffkWusQCVigwgr6difcSxdUK7qVd4rX5VdJv"


now = int(time.time())
command = f"allow from {ip} to {serverIp} port {port} proto {proto}"

concatValue = secretKey + ":" + command + ":" + \
    str(now) + ":" + str(duration) + ":" + initialPassword

concatValue = concatValue.encode("utf8")


sign = hashlib.sha512(concatValue).hexdigest()

commandQuoted = urllib.parse.quote_plus(command)
initialPasswordQuoted = urllib.parse.quote_plus(initialPassword)

url = f"https://gianlu.dev/{customPath}?command={commandQuoted}&password={initialPasswordQuoted}&sign={sign}&time={now}&duration={duration}"

r = requests.get(url)
print(r.text)
