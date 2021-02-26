# Open remote port on server

This software aims to provide a way to keep only http/https and smtp services available from outside, while at the same time allow legit clients to request port opening on the server.

It uses ufw in my case, but can be easily adapted to any remote command (not only for firewalling).

# Design

It works getting request parameters (for additional security, allow only get requests on your reverse proxy), checking if all are provided, then checks that the password on the client corresponds to the one on the server (to prevent any hash flooding).

Verify that the time of the request is not too old or too new (keep your and the server clock in sync!).

It also make sure that the full request SHA512 of the client is the same as the server, adding to the hash a shared secret.

If all the checks are successful, it'll run the command. It'll return to the client an error message if it fails, or stdout output if everything went well.

# Golang Server

Build the server with

`./compile.sh`

The Go source is in **PortOpener.go** and the binary output will be in **./build/PortOpener**

# Python Scripts

**Client.py** is the client to do the request.

**CronKeeper.py** is the cronjob script to make sure the firewall keeps allowing the client between IP changes.
