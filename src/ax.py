import serial, struct, sys

class AX:
    def __init__(self, device='/dev/ttyUSB0'):
        self.device = device
        self.ser = serial.Serial(port=device, baudrate=9600, timeout=3, rtscts=1, dsrdtr=1)

    def close(self):
        self.ser.close()

    def write_data(self, data):
        self.ser.write(data)

    def read_data(self, size):
        return self.ser.read(size=size)

    def write_command(self, cmd):
        data = bytearray()
        p = struct.pack('b', cmd)
        data.append(p)
        self.write_data(data)

    def write_size(self, size):
        data = bytearray()
        data.extend(struct.pack("!i", size))
        self.write_data(data)

    def read_size(self):
        size = int(struct.unpack('!i', self.read_data(4))[0])
        return size

    def read_result(self):
        result = int(struct.unpack('b', self.read_data(1))[0])
        return result

    def write_str(self, str):
        data = bytearray()
        data.extend([ord(c) for c in str])
        self.write_size(len(data))
        self.write_data(data)

    def read_str(self):
        size = self.read_size()
        s = str(self.read_data(size))

        return s

