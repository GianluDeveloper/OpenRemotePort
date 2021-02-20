# Open server remote port

This software aims to provide a way to keep only http/https and smtp services available from outside, while at the same time allow legit clients to request port opening on the server.

It uses ufw in my case, but can be easily adapted to any remote command (so not only for firewalling).

# Design

Works getting request parameters (for additional security, allow only get requests on you reverse proxy), checking if all are provided, then checks that the password on the client corresponds to the one on the server (to prevent any hash flooding).

Verify that the time of the request is not too old or too new (keep your and the server clock in sync!).

And finally make sure that the full request SHA512 of the client is the same as the server, adding to the hash a shared secret.

If all the checks are successful, then execute the command, and gives the error message if it fails, or the successful output if everything went well.
