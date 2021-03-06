from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:

    def __init__(self,
                 width: int,
                 height: int,
                 entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = numpy.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = numpy.full((width, height), fill_value=False, order='F')
        self.explored = numpy.full((width, height), fill_value=False, order='F')

        self.tiles[30:33, 22] = tile_types.wall

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = numpy.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
