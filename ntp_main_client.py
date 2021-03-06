import struct
import datetime
import socket
import time


def get_fraction(number, precision):
    return int((number - int(number)) * 2 ** precision)


class NTPPacket:
    """Source: https://habr.com/ru/post/448060/"""

    _FORMAT = "!B B b b 11I"  # format for struct.pack(), struct.unpack()

    def __init__(self, version_number=2, mode=3, transmit=0):
        # Necessary of enter leap second (2 bits)
        self.leap_indicator = 0
        # Version of protocol (3 bits)
        self.version_number = version_number
        # Mode of sender (3 bits)
        self.mode = mode
        # The level of "layering" reading time (1 byte)
        self.stratum = 0
        # Interval between requests (1 byte)
        self.pool = 0
        # Precision (log2) (1 byte)
        self.precision = 0
        # Interval for the clock reach NTP server (4 bytes)
        self.root_delay = 0
        # Scatter the clock NTP-server (4 bytes)
        self.root_dispersion = 0
        # Indicator of clocks (4 bytes)
        self.ref_id = 0
        # Last update time on server (8 bytes)
        self.reference = 0
        # Time of sending packet from local machine (8 bytes)
        self.originate = 0
        # Time of receipt on server (8 bytes)
        self.receive = 0
        # Time of sending answer from server (8 bytes)
        self.transmit = transmit

    def pack(self):
        """Transforms NTPPacket to byte-object for send by UDP"""
        return struct.pack(NTPPacket._FORMAT,
                           (self.leap_indicator << 6) + (self.version_number << 3) + self.mode,
                           self.stratum,
                           self.pool,
                           self.precision,
                           int(self.root_delay) + get_fraction(self.root_delay, 16),
                           int(self.root_dispersion) + get_fraction(self.root_dispersion, 16),
                           self.ref_id,
                           int(self.reference),
                           get_fraction(self.reference, 32),
                           int(self.originate),
                           get_fraction(self.originate, 32),
                           int(self.receive),
                           get_fraction(self.receive, 32),
                           int(self.transmit),
                           get_fraction(self.transmit, 32))

    def unpack(self, data: bytes):
        """Transforms byte-object to NTPPacket for use"""
        unpacked_data = struct.unpack(NTPPacket._FORMAT, data)

        self.leap_indicator = unpacked_data[0] >> 6  # 2 bits
        self.version_number = unpacked_data[0] >> 3 & 0b111  # 3 bits
        self.mode = unpacked_data[0] & 0b111  # 3 bits

        self.stratum = unpacked_data[1]  # 1 byte
        self.pool = unpacked_data[2]  # 1 byte
        self.precision = unpacked_data[3]  # 1 byte

        # 2 bytes | 2 bytes
        self.root_delay = (unpacked_data[4] >> 16) + \
                          (unpacked_data[4] & 0xFFFF) / 2 ** 16
        # 2 bytes | 2 bytes
        self.root_dispersion = (unpacked_data[5] >> 16) + \
                               (unpacked_data[5] & 0xFFFF) / 2 ** 16

        # 4 bytes
        self.ref_id = str((unpacked_data[6] >> 24) & 0xFF) + " " + \
                      str((unpacked_data[6] >> 16) & 0xFF) + " " + \
                      str((unpacked_data[6] >> 8) & 0xFF) + " " + \
                      str(unpacked_data[6] & 0xFF)

        self.reference = unpacked_data[7] + unpacked_data[8] / 2 ** 32  # 8 bytes
        self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32  # 8 bytes
        self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32  # 8 bytes
        self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32  # 8 bytes

        return self

    def current_time(self, arrive):
        """arrive - time to receiving a response packet on a local machine"""
        time_different = ((arrive - self.originate) - (self.transmit - self.receive)) / 2
        current_time = datetime.datetime.fromtimestamp(time.time() + time_different).strftime("%c")
        return time_different, current_time

    def __str__(self):
        return "Leap indicator: {0.leap_indicator}\n" \
               "Version number: {0.version_number}\n" \
               "Mode: {0.mode}\n" \
               "Stratum: {0.stratum}\n" \
               "Pool: {0.pool}\n" \
               "Precision: {0.precision}\n" \
               "Root delay: {0.root_delay}\n" \
               "Root dispersion: {0.root_dispersion}\n" \
               "Ref id: {0.ref_id}\n" \
               "Reference: {0.reference}\n" \
               "Originate: {0.originate}\n" \
               "Receive: {0.receive}\n" \
               "Transmit: {0.transmit}" \
            .format(self)


def main():
    """Takes current time from NTP-server"""
    # Time difference between 1970 and 1900, seconds
    format_diff = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600

    # Waiting time for recv (seconds)
    waiting_time = 5

    server = "pool.ntp.org"
    port = 123

    packet = NTPPacket(version_number=4, mode=3, transmit=time.time() + format_diff)
    answer = NTPPacket()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(waiting_time)
        s.sendto(packet.pack(), (server, port))
        data = s.recv(48)
        arrive_time = time.time() + format_diff
        answer.unpack(data)

    result = "Time difference: {}\nServer time: {}\n".format(*answer.current_time(arrive_time))
    print(result)


if __name__ == '__main__':
    main()