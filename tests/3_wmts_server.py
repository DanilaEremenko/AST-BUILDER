from http.server import BaseHTTPRequestHandler, HTTPServer
import signal
import sys
import json
import pandas as pd
import io
import numpy as np
import math

df = pd.DataFrame()
img_not_found = open('404_page_not_found.jpg', 'rb').read()


class WmtsUseful():

    @staticmethod
    def get_altitude_from_zoom(zoom):
        return 591657550.5 / (2 ** (zoom - 1))

    @staticmethod
    def get_zoom_from_altitude(altitude):
        return int(math.log(591657550.5 / altitude, 2) + 1)

    @staticmethod
    def get_most_near_tile_i(df, r):
        def get_d(x1, y1, x2, y2):
            return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return int(
            df.loc[
                get_d(x1=df['longitude'], y1=df['latitude'], x2=r['longitude'], y2=r['latitude'])
                ==
                min(get_d(x1=df['longitude'], y1=df['latitude'], x2=r['longitude'], y2=r['latitude']))
                ] \
                ['id']
        )

    #######################################################################################################
    # converting functions
    # according with:
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
    #######################################################################################################
    @staticmethod
    def num2deg(xtile, ytile, zoom):
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)

    @staticmethod
    def deg2num(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)


class HttpProcessor(BaseHTTPRequestHandler):
    def _send_wmts_response(self, errorCode, data, content_type):
        self.send_response(200)
        self.send_header('content-type', content_type)
        self.end_headers()
        self.wfile.write(data)

    def _parse_client_prms(self):
        path_splited = self.path.split('/')

        if path_splited[1] != 'tile':
            self._send_wmts_response(
                errorCode=200,
                data='page not exist'.encode(),
                content_type='text/plain'
            )
            return None
        else:
            request_prm = {}
            request_prm['z'] = int(path_splited[2])
            request_prm['x'] = int(path_splited[3])
            request_prm['y'] = int(path_splited[4].split('.')[0])

            request_prm['altitude'] = WmtsUseful.get_altitude_from_zoom(request_prm['z'])
            request_prm['latitude'], request_prm['longitude'] = WmtsUseful.num2deg(xtile=request_prm['x'],
                                                                                   ytile=request_prm['y'],
                                                                                   zoom=request_prm['z'])
            return request_prm

    def do_GET(self):

        request_prm = self._parse_client_prms()

        print('------------------- REQUEST ------------------------')
        print(request_prm)

        row = df[(df['x'] == request_prm['x'])
                 & (df['y'] == request_prm['y'])
                 & (df['z'] == request_prm['z'])] \
            .head(1)

        if row.empty:

            print('NOT FOUND\n', row)

            self._send_wmts_response(
                errorCode=200,
                data=img_not_found,
                content_type='image/png'
            )

        else:

            print('FOUND, PASSED ', row.iloc[0]['img_name'])

            self._send_wmts_response(
                errorCode=200,
                data=row.iloc[0]['data'],
                content_type='image/png'
            )


def signal_handler(sig, frame):
    print('Exiting server')
    sys.exit(0)


def get_df(tile_dir, img_size):
    import exif_parser as ep
    import os
    from PIL import Image

    tile_dir_abs = os.path.abspath(tile_dir)

    img_names = os.listdir(tile_dir_abs)
    img_names.sort()
    img_names = img_names  # TODO delete

    res_dict = {'id': [], 'img_name': [],
                'latitude': [], 'longitude': [], 'altitude': [],
                'x': [], 'y': [], 'z': [],
                'data': []}

    for id, img_name in enumerate(img_names):
        img_gps = ep.get_gps_info(Image.open('%s/%s' % (tile_dir_abs, img_name)))
        res_dict['latitude'].append(img_gps['Latitude'])
        res_dict['longitude'].append(img_gps['Longitude'])
        res_dict['altitude'].append(img_gps['Altitude'])

        res_dict['z'].append(WmtsUseful.get_zoom_from_altitude(img_gps['Altitude']))

        x, y = WmtsUseful.deg2num(
            lat_deg=img_gps['Latitude'],
            lon_deg=img_gps['Longitude'],
            zoom=res_dict['z'][-1]
        )
        res_dict['x'].append(x)
        res_dict['y'].append(y)

        img = Image.open('%s/%s' % (tile_dir_abs, img_name))
        img.thumbnail(img_size)

        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()

        res_dict['data'].append(imgByteArr)

    res_dict['img_name'] = img_names
    res_dict['id'] = list(range(len(res_dict['img_name'])))

    return pd.DataFrame(res_dict)


def main():
    # parsing arguments
    with open('config.json') as fp:
        config_dict = json.load(fp)

    global df
    print('rendering images...')
    df = get_df(config_dict['TILE_DIR'], config_dict['IMG_SIZE'])
    print('df.size = %d' % len(df))
    print('sizeof(df) = %.2f MB' % (sys.getsizeof(df) / 1024 / 1024))

    signal.signal(signal.SIGINT, signal_handler)
    print('SIGINT handler created')

    serv = HTTPServer(('', config_dict['PORT']), HttpProcessor)
    print('Requests expected on %d port\nWMTS server running...' % config_dict['PORT'])

    serv.serve_forever()


if __name__ == '__main__':
    main()
