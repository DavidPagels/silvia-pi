#!/usr/bin/python

# Raspberry Pi SPI Port and Device
spi_port = 0
spi_dev = 0

# Pin # for relay connected to heating element
he_pin = 7

# Main loop sample rate in seconds
sample_time = 0.1

# PID Proportional, Integral, and Derivative values
Ku = 22
Ts = 168

p = 0.6 * Ku
i = 1.2 * Ku / Ts
d = 0.075 * Ku * Ts

# Web/REST Server Options
port = 8080

# Uses emulated hardware if True
testing = False
