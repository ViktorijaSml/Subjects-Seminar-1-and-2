import asyncio

from bleak import BleakClient
from pynput.keyboard import Key, Controller

#------
#------
#------
#------
#------
#------
#------
#------
#------
#------

ADDRESS = "FC:DE:51:CB:FE:4D"
CHARACTERISTIC_UUID = "00000007-0000-1000-8000-00805f9b34fb"

dice = [5, 1, 4, 3, 0, 2]
keyboard = Controller()

def move(value):
    global dice
    global keyboard
    direction = dice.index(value)
    match direction:
        case 0:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            dice = [dice[5], dice[4], dice[2], dice[3], dice[0], dice[1]]
        case 1:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            dice = [dice[4], dice[5], dice[2], dice[3], dice[1], dice[0]]
        case 2:
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            dice = [dice[0], dice[1], dice[5], dice[4], dice[2], dice[3]]
        case 3:
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            dice = [dice[0], dice[1], dice[4], dice[5], dice[3], dice[2]]

def notification_handler(sender, data):
    move(data[-1])

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected!")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(300.0)
        await client.stop_notify(CHARACTERISTIC_UUID)
    print("Disconnected!")

asyncio.run(main())
