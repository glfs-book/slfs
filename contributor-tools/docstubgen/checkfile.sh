#!/bin/bash

# Helper script for checking files in docstubgen.
# (C) Seal Sealy 2025

# ELF is binaries and shared libraries
# scripts is all kinds of misc .sh stuff and more
# ar archive is for static libs

file $1 | grep -E "ELF|script|ar archive" > /dev/null 2>&1
if [ $? -ne 0 ]; then
	exit 1
fi
exit 0
