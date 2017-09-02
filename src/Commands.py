# -*- coding: utf-8 -*-

import os, sys

CMD_EXIT = 1
CMD_SEND_MESSAGE = 3
CMD_PUT_FILE = 4
CMD_PUT_ADF = 5


class Commands:
    """This class was intended as a base for a fancy gui app for AX."""
    def __init__(self, ax):
        """ax is an valid/initialized instance of the AX class"""
        self.ax = ax

    def close(self):
        """Close the associated serial port"""
        self.ax.close()

    def send_exit(self):
        """Lets the amiga-side (axam) terminate"""
        self.ax.write_command(CMD_EXIT)

    # TODO: this function should either check for length of message or plit it in several parts.
    def send_message(self, message):
        """Sends a message to the amiga"""
        self.ax.write_command(CMD_SEND_MESSAGE)
        self.ax.write_str(message)

    def send_file(self, filename, dst):
        """Sends a file where dst is the fully qualified name (e.g. 'ram:Commands.py')"""
        src = open(sys.argv[1], 'rb')
        self.ax.write_command(CMD_PUT_FILE)
        self.ax.write_str(dst)
        to_read = 1024
        cur = 0
        size = os.path.getsize(filename)
        self.ax.write_size(size)

        while cur < size:
            if size - cur < to_read:
                to_read = size - cur

            data = src.read(to_read)
            self.ax.write_data(data)
            result = self.ax.read_result()
            if result != 0:
                return result
            cur += to_read

        return 0

    def send_adf(self, filename, drive):
        """Sends an adf file directly to a amiga disk drive. The drive ist selected by id
           where 0 is the internal drive, 1 the first external drive and so on.
           (This is a rather lengthy operation)
        """
        src = open(filename, 'rb')
        self.ax.write_command(CMD_PUT_ADF)
        to_read = 11 * 512
        cur = 0
        track = 0
        size = os.path.getsize(filename)
        self.ax.write_command(drive)

        while cur < size:
            if size - cur < to_read:
                to_read = size - cur

            data = src.read(to_read)
            self.ax.write_data(data)
            result = self.ax.read_result()
            if result != 0:
                return result
            track += 1

            cur += to_read

        return 0
