#!/usr/bin/env python
import TasmotaCirculation
import TasmotaHeatingSystem

if __name__ == "__main__":
    try:
        print ("force stopping circulation")
        circulation_client = TasmotaCirculation.connect()
        TasmotaCirculation.off(circulation_client)
    except Exception as ex1:
        print ("ERROR force stopping circulation: ", ex1)
    try:
        print ("force stopping heatingsystem")
        heatingsystem_client = TasmotaHeatingSystem.connect()
        TasmotaHeatingSystem.off(heatingsystem_client)
    except Exception as ex2:
        print ("ERROR force stopping heatingsystem: ", ex2)
