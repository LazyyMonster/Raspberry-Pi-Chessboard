import smbus
import time
import math
import board
from adafruit_ht16k33 import matrix
import adafruit_tca9548a


#constants
LIGHT_STRENGTH = 0.1


class Hardware:
#preparing i2c devices
    i2c = board.I2C()
    I2C_address = 0x70
    I2C_bus_number = 1
    bus = smbus.SMBus(I2C_bus_number)
#   columns values of reed switches states (each of 8 bits represent squares
    mbrd = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    initBrd = [60, 60, 60, 60, 60, 60, 60, 60]

    chcol = ["A", "B", "C", "D", "E", "F", "G", "H"]
    DEVICE = [0x21, 0x22, 0x23, 0x24]
    GPIOn = [0x12, 0x13]
    IODIRA = 0x00
    IODIRB = 0x01
    GPIOA = 0x12
    GPIOB = 0x13
    GPPUA = 0x0C
    GPPUB = 0x0D

    tca = adafruit_tca9548a.TCA9548A(i2c)
    matrix = matrix.Matrix8x8(tca[1], address = 0x71)

    translate = [[[8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7]],
        [[7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]],
        [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7]],
        [[5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7]],
        [[4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7]],
        [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7]],
        [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7]],
        [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]],
        [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]]]


    moveFrom = [-1, -1]
    moveTo = [-1, -1]


    def __init__(self):
        self.init_i2c_devices()


    def init_i2c_devices(self):
        #print ("initiation of i2c devices")
        try:
            for i in range(0, 4):
                i2c_channel = 2**(i+2)
                self.bus.write_byte(self.I2C_address, i2c_channel)
                self.bus.write_byte_data(self.DEVICE[i], self.IODIRA, 0xFF)
                self.bus.write_byte_data(self.DEVICE[i], self.GPPUA, 0xFF)
                self.bus.write_byte_data(self.DEVICE[i], self.IODIRB, 0xFF)
                self.bus.write_byte_data(self.DEVICE[i], self.GPPUB, 0xFF)
        except:
            print ("error in init_i2c_devices")


    def checkStartingPosition(self):
        #startRows = [1 = first bit, 2 = second bit, 7 = 7th bit, 8 = 8th bit]
        print ("Set pieces!")
        try:
            while True:
                for k in range(0, 4):
                    for i in range(2):
                        i2c_channel = 2**(k+2)

                        self.bus.write_byte(self.I2C_address, i2c_channel)

                        colValue = self.bus.read_byte_data(self.DEVICE[k], self.GPIOn[i])
                        column = (k * 2) + i

                        bits = bin(colValue)[2:].zfill(8)
                        self.matrix[column, 0] = int(bits[-1]) * LIGHT_STRENGTH
                        self.matrix[column, 1] = int(bits[-2]) * LIGHT_STRENGTH
                        self.matrix[column, 6] = int(bits[-7]) * LIGHT_STRENGTH
                        self.matrix[column, 7] = int(bits[-8]) * LIGHT_STRENGTH
                        self.mbrd[column] = colValue
                        if self.mbrd == self.initBrd:
                            print ("Pieces are ready!")
                            return True
        except:
            print ("error in checkStartingPosition")


    #routine for ligtning the passed leds coords for a given time
    def led(self, *leds, sleepTime = 0.1):
        self.matrix.fill(0)

        for led in leds:
            column, row = led
	    #set ligth strength
            self.matrix[column, row - 1] = LIGHT_STRENGTH

        time.sleep(sleepTime)
        self.matrix.fill(0)


    #routine for ligtning the passed leds coords forever
    def ledForever(self, *leds):
       # self.matrix.fill(0)

        for led in leds:
            column, row = led
            self.matrix[column, row - 1] = LIGHT_STRENGTH


    def highlightMove(self, moveFrom, moveTo, ledTime = 0.1):
        while True:
            try:
                self.matrix.fill(0)
                self.ledForever(moveFrom)
                self.ledForever(moveTo)
                break
            except Exception as e:
                print ("error in highlightMove")
                print (f"exception message: {e}")


    def highlightValidMoves(self, validMoves):
        self.matrix.fill(0)
        if not validMoves:
            return

        for validMove in validMoves:
            column = validMove[0]
            row = validMove[1]

            self.matrix[column, 7 - row] = LIGHT_STRENGTH


    def searchForMove(self):
        try:
            for k in range(0, 4):
                for i in range(2):
                    i2c_channel = 2**(k+2)
                    column = (k * 2) + i

                    self.bus.write_byte(self.I2C_address, i2c_channel)

                    prevColVal = self.mbrd[column]
                    colVal = self.bus.read_byte_data(self.DEVICE[k], self.GPIOn[i])

                    if colVal != prevColVal:
                        self.mbrd[column] = colVal
                        rowInBin = colVal ^ prevColVal
                        row = math.frexp(rowInBin)[1]

                        if colVal > prevColVal:
                            self.moveFrom = [column, row]
                            return self.moveFrom, None

                        else:
                            self.moveTo = [column, row]
                            return self.moveFrom, self.moveTo
        except:
            print ("error in searchForMove")


    def resetLed(self):
        self.matrix.fill(0)
