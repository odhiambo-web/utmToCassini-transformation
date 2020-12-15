from copy import deepcopy
from math import sqrt, cos, sin, radians, atan, degrees
from statistics import mean

class Converter:
    def __init__(self, data, settings, config, cartesian = None):
        self.settings = settings
        self.data = data
        self.config = config
        self.cartesian = cartesian
        self.results = []
    
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
        c = self.settings[self.config['zone']][self.config['model']]
        results = []
        xo = mean([p['x'] for p in self.cartesian])
        yo = mean([p['y'] for p in self.cartesian])
        zo = mean([p['z'] for p in self.cartesian])
        for p in deepcopy(self.cartesian):
            ux = p['x'] - xo
            uy = p['y'] - yo
            uz = p['z'] - zo
            x = xo + c['tx'] + ((1+c['s']) * (ux+(c['rz']*uy)-(c['ry']*uz)))
            y = yo + c['ty'] + ((1+c['s']) * (uy-(c['rz']*ux)+(c['rx']*uz)))
            z = zo + c['tz'] + ((1+c['s']) * (uz+(c['ry']*ux)-(c['rx']*uy)))
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


class Geographic:
    def __init__(self, clarke, settings):
        self.clarke = clarke
        self.settings = settings
        self.results = []

    def geographic(self):
        s = deepcopy(self.settings)
        eSq = (2*s['clarkeToCartesian']['f']) - (s['clarkeToCartesian']['f']**2)
        results = []
        for p in deepcopy(self.clarke):
            lng = degrees(atan(p['y']/p['x']))
            D = sqrt((p['x']**2) + (p['y']**2))
            phi0 = degrees(atan(p['z']/(D*(1-eSq))))
            Nc = s['clarkeToCartesian']['a'] / sqrt((1-(eSq*(sin(radians(phi0))**2))))
            phi1 = degrees(atan((p['z'] + (eSq*Nc*sin(radians(phi0))))/D))
            Nc1 = s['clarkeToCartesian']['a'] / sqrt((1-(eSq*(sin(radians(phi1))**2))))
            phi2 = degrees(atan((p['z'] + (eSq*Nc1*sin(radians(phi1))))/D))
            Nc2 = s['clarkeToCartesian']['a'] / sqrt((1-(eSq*(sin(radians(phi2))**2))))
            phi3 = degrees(atan((p['z'] + (eSq*Nc2*sin(radians(phi2))))/D))
            if abs(phi2 - phi1) < 0.0001:
                phi = phi3
            else:
                phi = phi3
            h = (D/cos(radians(phi)))-Nc1
            results.append({'index':p['index'], 'x': phi, 'y': lng, 'z': h, 'point_id': p['point_id']})
        self.results = results
        return self.results

class Cassini: 
    def __init__(self, utm, config, settings):
        self.utm = utm
        self.config = config
        self.settings = settings
        self.results = []
    
    def cassini(self):
        s = deepcopy(self.settings[self.config['sheet']])
        results = []
        for p in deepcopy(self.utm):
            y = ((s['b']*p['x'])-(s['b']*s['tx'])-(s['a']*p['y'])+(s['a']*s['ty']))/(-(s['b']**2)-(s['a']**2))
            x = ((s['a']*p['x'])-(s['a']*s['tx'])+(s['b']*p['y'])-(s['b']*s['ty']))/((s['a']**2)+(s['b']**2))
            results.append({'index':p['index'], 'x': x, 'y': y, 'point_id': p['point_id']})
        self.results = results
        return self.results
