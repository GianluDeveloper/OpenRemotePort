package main

import (
	"crypto/sha512"
	"encoding/hex"
	"fmt"
	"net/http"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

var initialPassword = "hellop#firstsec"
var secretKey string = "z2Xm3m4Dr:/Rm2Gv5WdpCpDLdYVrqCgpcftYqMiqSXLu3esqzwfgpwxKqyDm765UnJttuw2CtxV2bunpTwmqvLeFTfrzdkA3Q6pNNGPwvrTDCBHFN4jPyWAj7X7wPrX7feiKxRni2PZc6go3Ksd7HETh6HbGRZgiZKtSdQohfwK9qNYWGF5975ePgGLTgykGGpFik3AmhxKRWN7NxzUVdotWkdzdkVCzLkGcVzi8C9BqDt9vekshWZoCvVNo8zFnph7ZvCN6n9ZrHpyhfaNNddPAPxCsDzWxRVbK7tHkrbvdPUxmM5D87LcmQBwDfJybvspvy23ZbCcufKER6xSXizMBxG3m6gZjj4nopRrRHVSieB4YEf2pCAeXH3GghMEJ3bEtFuGCeacQ8y3PgDZaoyZD92Lq6t6raRjdSxzYrHq4h7VGTRrBNzorsXD3VffkWusQCVigwgr6difcSxdUK7qVd4rX5VdJv"
var maxTime int32 = 60
var minTime int32 = 10
var maxDuration int = 3600 * 24 // max 1 day. for infinite use 0

func removeRule(rule []string, duration int) {
	var newRule []string

	newRule = append(newRule, "delete")
	newRule = append(newRule, rule...)

	time.Sleep(time.Duration(duration) * time.Second)
	exec.Command("ufw", newRule...).Output()
	fmt.Printf("Removed rule\n")
	// send some notification
}

func getsha512(inputString string) (sha string) {
	bv := []byte(inputString)
	hasher := sha512.New()
	hasher.Write(bv)
	sha = hex.EncodeToString(hasher.Sum(nil))
	return
}

// myIP echo ip
func myIP(w http.ResponseWriter, r *http.Request) {
	theIP := r.Header.Get("X-Real-IP")
	_, wantJSON := r.URL.Query()["json"]
	if wantJSON {
		fmt.Fprintf(w, "{\"ip\":\"%s\"}", theIP)

	} else {
		fmt.Fprintf(w, "%s", theIP)
	}
}

// OpenExec service
func OpenExec(w http.ResponseWriter, r *http.Request) {
	command, okc := r.URL.Query()["command"]
	sign, oks := r.URL.Query()["sign"]
	Now, okn := r.URL.Query()["time"]
	duration, okd := r.URL.Query()["duration"]
	passedPassword, okp := r.URL.Query()["password"]

	if !okc || !oks || !okn || !okd || !okp {
		fmt.Fprintf(w, "request error.")
		return
	}
	if passedPassword[0] != initialPassword {
		fmt.Fprintf(w, "invalid first security password.") // to prevent possibile hashing dos
		return
	}

	now := int32(time.Now().Unix())
	remoteNow64, _ := strconv.Atoi(Now[0])
	remoteNow := int32(remoteNow64)
	if remoteNow < (now-minTime) || remoteNow > (now+maxTime) {
		fmt.Fprintf(w, "timestamp error %d %d.", remoteNow64, now)
		return
	}

	concatValues := secretKey + ":" + command[0] + ":" + Now[0] + ":" + duration[0] + ":" + passedPassword[0]
	myHash := getsha512(concatValues)

	if myHash != sign[0] {

		fmt.Fprintf(w, "not authorized to do that.")
		return
	}
	Duration, err := strconv.Atoi(duration[0])
	if err != nil || Duration > maxDuration {
		fmt.Fprintf(w, "duration error. maybe longer than %d seconds?", maxDuration)
		return
	}

	cmds := strings.Split(command[0], " ")
	out, err := exec.Command("ufw", cmds...).Output()

	if err != nil {
		fmt.Fprintf(w, "error: \n%s", err)
		return
	}
	fmt.Fprintf(w, "%s", out[:])

	if Duration > 0 {
		go removeRule(cmds, Duration)
	}

	// c, _ := redis.Dial("tcp", ":6379")
	// defer c.Close()
	// n, _ := redis.Int(c.Do("INCR", "k1"))
	// fmt.Fprintf(w, "%s -> %s %s %s now is %d Hello %s, %d!", concatValues, myHash, command, sign, now, getsha512("ciao"), n)
}

func main() {
	http.HandleFunc("/", OpenExec)
	http.HandleFunc("/ip", myIP)
	http.ListenAndServe(":8082", nil)
}
