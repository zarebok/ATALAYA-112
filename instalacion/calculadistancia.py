# coding=utf-8
import WazeRouteCalculator
import logging

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Av. de la Transición Española, s/n, 28100 Alcobendas, Madrid'
to_address = 'Av. de España, 52, 28100 Alcobendas, Madrid'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_route_info()
