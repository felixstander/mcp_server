from math import atan2, cos, radians, sin, sqrt
from typing import Tuple

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("resource_improvement")

@mcp.tool()
def adjacent_area(area_gps:List[Tuple[str,str]]):
    # [('南山区','29.124,112.231'),('福田区','30.144,113.232'),('罗湖区','30.144,122.421')]

    nearest_areas = []

    for i, (area_name, gps) in enumerate(area_gps):
        lat1, lon1 = map(float, gps.split(','))
        min_distance = float('inf')
        nearest_area = None

        for j, (other_area_name, other_gps) in enumerate(area_gps):
            if i != j:
                lat2, lon2 = map(float, other_gps.split(','))
                distance = _haversine(lon1, lat1, lon2, lat2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_area = other_area_name

        nearest_areas.append((area_name, nearest_area))


    def _haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points 
        on the earth (specified in decimal degrees)
        """
        # 将十进制度数转换为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Haversine公式
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a)) 
        r = 6371  # 地球半径，单位为公里
        return c * r

    return nearest_areas
if __name__ == "__main__":
    mcp.run(transport='stdio')
