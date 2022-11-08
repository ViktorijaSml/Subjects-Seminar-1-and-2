import asyncio
from bleak import BleakClient
import random

mylist = ["Square", "Circle", "Hexagon"]
flag = False


ADDRESS = "FC:DE:51:CB:FE:4D"
CHARACTERISTIC_UUID = "00000005-0000-1000-8000-00805f9b34fb"

ENABLE = "0F01"
ENABLE = bytearray.fromhex(ENABLE)

DISABLE = "0F00"
DISABLE = bytearray.fromhex(DISABLE)

def touch_it(shape,info):
    if shape == "Square":
        if info[3]== 0 or info[4]== 0:
            print("Touch!")
            return True
    elif shape == "Circle":
        if info[0]== 0 or info[2]== 0:
            print("Touch!")
            return True
    elif shape == "Hexagon":
        if info[1]== 0 or info[5]== 0:
            print("Touch!")
            return True
    else:
        print("Wrong input for touch_it")
    return False    


def notification_handler(sender, data):
    global flag
    global shape

    if touch_it(shape[0], data)== True:
        print("Good job!")
        flag = True

        
async def main():
    global flag
    async with BleakClient(ADDRESS) as client:
        print("Connected!")
        global mylist
        global shape
        svcs = await client.get_services()
        touch = svcs.get_service(18).characteristics[1]
        controller = (svcs.get_service(34).characteristics)[0]

        await client.write_gatt_char(controller, ENABLE)
        shape = random.sample(mylist, k=1)
        print("Touch " + shape[0] + "!")

        await asyncio.sleep(4.0) #stabiliziraj se

        print("Go!")
        while flag == False:
            await client.start_notify(touch, notification_handler)
        
        
        await client.stop_notify(touch)
        await client.write_gatt_char(controller, DISABLE)

    flag = False        
    print("Disconnected!")

asyncio.run(main())
