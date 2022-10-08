import struct


class FilePC:
    path = ""
    lat = 0.0
    lon = 0.0
    scale = 0.0
    year = ''
    month = ''
    day = ''
    hour = ''
    minute = ''
    second = ''
    micro_sec = 0
    sample_rate = 0
    sample_num = 0
    sample_type = 0
    sample_size = 0
    trace_num = ''
    trace_source = ''
    samples = []

    def __init__(self, path):
        self.path = path

    def __str__(self):
        info = str(self.day) + '.' + str(self.month) + '.' + str(self.year) + \
               ' - ' + str(self.hour) + ':' + str(self.day) + '\n' + 'Частота: ' + str(self.sample_rate)
        return info

    def read(self):
        try:
            f = open(self.path, "rb")
        except:
            return False

        file_type = f.read(2)
        if file_type != b'PC':
            return False

        f.read(4)
        self.lat = struct.unpack('f', f.read(4))[0]
        self.lon = struct.unpack('f', f.read(4))[0]
        self.scale = struct.unpack('d', f.read(8))[0]
        self.year = struct.unpack('b', f.read(1))[0]
        self.month = struct.unpack('b', f.read(1))[0]
        self.day = struct.unpack('b', f.read(1))[0]
        self.hour = struct.unpack('b', f.read(1))[0]
        self.minute = struct.unpack('b', f.read(1))[0]
        self.second = struct.unpack('b', f.read(1))[0]
        self.micro_sec = struct.unpack('i', f.read(4))[0]
        self.sample_rate = struct.unpack('h', f.read(2))[0]
        self.sample_num = struct.unpack('i', f.read(4))[0]

        data_type = struct.unpack('h', f.read(2))[0]
        if data_type == 2:
            self.sample_type = "h"
            self.sample_size = 2
        elif data_type == 4:
            self.sample_type = "i"
            self.sample_size = 4
        elif data_type == 4100:
            self.sample_type = "f"
            self.sample_size = 4
        else:
            self.sample_type = "d"
            self.sample_size = 8
        self.trace_num = struct.unpack('c', f.read(1))[0]
        self.trace_source = struct.unpack('c', f.read(1))[0]

        self.samples = []
        for i in range(self.sample_num):
            next_sample = f.read(self.sample_size)
            self.samples.append(struct.unpack(self.sample_type, next_sample)[0])

        f.close()
        return True

    def print_info(self):
        print("Path: " + self.path)
        print("Lat: " + str(self.lat))
        print("Lon: " + str(self.lon))
        print("Scale: " + str(self.scale))
        print("Year: " + str(self.year))
        print("Month: " + str(self.month))
        print("Day: " + str(self.day))
        print("Hour: " + str(self.hour))
        print("Minute: " + str(self.minute))
        print("Second: " + str(self.second))
        print("Microsecond: " + str(self.micro_sec))
        print("Sample rate: " + str(self.sample_rate))
        print("Sample number: " + str(self.sample_num))
        print("Sample type: " + str(self.sample_type))
        print("Trace number: " + str(self.trace_num))
        print("Trace source: " + str(self.trace_source))