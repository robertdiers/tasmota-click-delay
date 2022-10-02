#!/usr/bin/env python
import TasmotaCirculation

if __name__ == "__main__":
    print ("force stopping circulation")
    circulation_client = TasmotaCirculation.connect()
    TasmotaCirculation.off(circulation_client)
