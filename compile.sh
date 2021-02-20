#!/bin/bash

if [ ! -d "./build" ]; then
    mkdir "./build"
fi

go build -ldflags "-s -w" -o "./build/PortOpener" "PortOpener.go"
