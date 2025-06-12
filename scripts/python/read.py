import toml

def read_toml(file) -> dict:
    return toml.load(file)

def read_stations(stations_file):

    net = []
    sta = []
    lat = []
    lon = []
    ele = []
    bur = []
    sen = []

    # station file has following format:
    # 'Net.Sta', 'Lat', 'Lon', 'Elev', 'Bur', Sensor
    with open(stations_file, 'r') as f:

        for line in f.readlines():
            line = line.strip()
            if line[0] == '#':
                continue
            line = line.split(',')
            _net, _sta = line[0].split('.')
            net.append(_net.strip())
            sta.append(_sta.strip())
            lat.append(float(line[1]))
            lon.append(float(line[2]))
            ele.append(float(line[3]))
            bur.append(float(line[4]))
            sen.append(line[5])

    return net, sta, lat, lon, ele, bur, sen
