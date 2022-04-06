#!/usr/bin/python

# Raspberry Pi SPI Port and Device
spi_port = 0
spi_dev = 0

# Pin # for relay connected to heating element
he_pin = 7

# Main loop sample rate in seconds
sample_time = 0.1

# PID Proportional, Integral, and Derivative values
p = 3.4
i = 0.3
d = 40.0

# Web/REST Server Options
port = 8080

# Uses emulated hardware if True
testing = False
