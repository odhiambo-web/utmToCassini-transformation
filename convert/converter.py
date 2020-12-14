from copy import deepcopy
from math import sqrt, cos, sin, radians
from statistics import mean

class Converter:
    def __init__(self, data, settings, config, cartesian = None):
        self.settings = settings
        self.data = data
        self.config = config
        self.cartesian = cartesian
        self.results = {}
    
    def convert(self):
        results = []
        for p in deepcopy(self.data):
            results.append(self.convertToCartesian(p))
        self.cartesian = results
        return self.cartesian

    def transform(self):
        self.convert()
        if self.config['model'] == '3p':
            self.results = self.convertUsing3p()
        elif self.config['model'] == '7p':
            self.results = self.convertUsing7p()
        else:
            self.results = self.convertUsing10p()
        return self.results

    def convertUsing3p(self):
        c = self.settings[self.config['zone']][self.config['model']]
        results = []
        for p in deepcopy(self.cartesian):
            x = p['x'] + c['tx']
            y = p['y'] + c['ty']
            z = p['z'] + c['tz']
            results.append({'index':p['index'], 'x': x, 'y': y, 'z': z, 'point_id': p['point_id']})
        self.results = results
        return self.results

    def convertUsing7p(self):
        c = self.settings[self.config['zone']][self.config['model']]
        results = []
        for p in deepcopy(self.cartesian):
            x = c['tx'] + ((1+c['s']) * (p['x']+(c['rz']*p['y'])-(c['ry']*p['z'])))
            y = c['ty'] + ((1+c['s']) * (p['y']-(c['rz']*p['x'])+(c['rx']*p['z'])))
            z = c['tz'] + ((1+c['s']) * (p['z']+(c['ry']*p['x'])-(c['rx']*p['y'])))
            results.append({'index':p['index'], 'x': x, 'y': y, 'z': z, 'point_id': p['point_id']})
        self.results = results
        return self.results

    def convertUsing10p(self):
        # c = self.settings[self.config['zone']][self.config['model']]
        # results = []
        # xo = mean([p['x'] for p in self.cartesian])
        # yo = mean([p['y'] for p in self.cartesian])
        # zo = mean([p['z'] for p in self.cartesian])
        # for p in deepcopy(self.cartesian):
        #     ux = p['x'] - xo
        #     uy = p['y'] - yo
        #     uz = p['z'] - zo
        #     x = p['x'] + c['tx'] + ((1+c['s']) * (ux+(c['rz']*uy)-(c['ry']*uz)))
        #     y = p['y'] + c['ty'] + ((1+c['s']) * (uy-(c['rz']*ux)+(c['rx']*uz)))
        #     z = p['z'] + c['tz'] + ((1+c['s']) * (uz+(c['ry']*ux)-(c['rx']*uy)))
        #     results.append({'index':p['index'], 'x': x, 'y': y, 'z': z, 'point_id': p['point_id']})
        # self.results = results
        # return self.results       
        c = self.settings[self.config['zone']]['7p']
        results = []
        for p in deepcopy(self.cartesian):
            x = c['tx'] + ((1+c['s']) * (p['x']+(c['rz']*p['y'])-(c['ry']*p['z'])))
            y = c['ty'] + ((1+c['s']) * (p['y']-(c['rz']*p['x'])+(c['rx']*p['z'])))
            z = c['tz'] + ((1+c['s']) * (p['z']+(c['ry']*p['x'])-(c['rx']*p['y'])))
            results.append({'index':p['index'], 'x': x, 'y': y, 'z': z, 'point_id': p['point_id']})
        self.results = results
        return self.results 

    def convertToCartesian(self, point):
        s = deepcopy(self.settings)
        eSq = (2*s['wgsToCartesian']['f']) - (s['wgsToCartesian']['f']**2)
        Nw = s['wgsToCartesian']['a'] / sqrt((1-(eSq*(sin(radians(float(point['lat'])))**2))))
        x = (Nw+float(point['height'])) * cos(radians(float(point['lat']))) * cos(radians(float(point['long'])))
        y = (Nw+float(point['height'])) * cos(radians(float(point['lat']))) * sin(radians(float(point['long'])))
        z = ((1-eSq)*Nw + float(point['height'])) * sin(radians(float(point['lat'])))
        return {'index':point['index'], 'x': x, 'y': y, 'z': z, 'point_id': point['point_id']}
