import asyncio
from bleak import BleakClient
import random

mylist = ["Red", "Green", "Blue", "Yellow", "Purple", "White"]
flag = False

ADDRESS = "FC:DE:51:CB:FE:4D"
CHARACTERISTIC_UUID = "00000005-0000-1000-8000-00805f9b34fb"

ENABLE = "0F01"
ENABLE = bytearray.fromhex(ENABLE)

DISABLE = "0F00"
DISABLE = bytearray.fromhex(DISABLE)

COLORS = "03 100000 001000 000010 101000 100010 101010"
COLORS = bytearray.fromhex(COLORS)

def find_it(color,info):
    if color == "Red":
        if info[0]== 0 :
            print("Found it!")
            return True
    elif color == "Green":
        if info[1]== 0 :
            print("Found it!")
            return True
    elif color == "Blue":
        if info[2]== 0 :
            print("Found it!")
            return True
    elif color == "Yellow":
        if info[3]== 0 :
            print("Found it!")
            return True
    elif color == "Purple":
        if info[4]== 0 :
            print("Found it!")
            return True
    elif color == "White":
        if info[5]== 0 :
            print("Found it!")
            return True    
    else:
        print("Wrong input for find_it")
    return False    


def notification_handler(sender, data):
    global flag
    global color
    
    if find_it(color[0], data)== True:
        print("Good job!")
        flag = True
   
        
async def main():
    global flag
    async with BleakClient(ADDRESS) as client:
        print("Connected!")
        global mylist
        global color
        
        svcs = await client.get_services()
        touch = svcs.get_service(18).characteristics[1]
        controller = (svcs.get_service(34).characteristics)[0]

        await client.write_gatt_char(controller, ENABLE)
        await client.write_gatt_char(controller, COLORS)
   
        color = random.sample(mylist, k=1)
        print("Find " + color[0] + "!")
        await asyncio.sleep(4.0) #stabiliziraj se

        print("Go!")
        while flag == False:
            await client.start_notify(touch, notification_handler)

        await client.stop_notify(touch)
        await client.write_gatt_char(controller, DISABLE)

    flag = False        
    print("Disconnected!")

asyncio.run(main())
