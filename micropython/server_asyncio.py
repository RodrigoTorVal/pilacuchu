try:
	import uasyncio as asyncio
except:
	import asyncio

import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid="GALERIA"
password="tirotidritigo"

station=network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected()==False:
	pass
print('Connection successful')
print(station.ifconfig())

@asyncio.coroutine
def serve(reader, writer):
	print(reader, writer)
	print("================")
	print((yield from reader.read()))
	yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello.\r\n")
	print("After response write")
	yield from writer.aclose()
	print("Finished processing request")

@asyncio.coroutine
def teste():
	while True:
		print("holaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXhola")
		await asyncio.sleep(0)
loop = asyncio.get_event_loop()
loop.call_soon(asyncio.start_server(serve,station.ifconfig()[0],80))
loop.create_task(teste())
loop.run_forever()
loop.close()

#192.168.1.35
"""
import asyncio

async def snmp():
    while True:
        print("Doing the snmp thing")
        await asyncio.sleep(1)

async def proxy():
    while True:
        print("Doing the proxy thing")
        await asyncio.sleep(2)

loop = asyncio.get_event_loop()
loop.create_task(snmp())
loop.create_task(proxy())
loop.run_forever()
"""
