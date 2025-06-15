from typing import List

from pydantic import BaseModel


class HelixRectangleParams(BaseModel):
    x0: float
    y0: float
    width: float
    height: float
    corner_radius: float
    layer_index_list: List[int]
    track_width: float
    connect_width: float
    drill_size: float
    via_size: float
    net_number: int
    segment_number: int = 100
