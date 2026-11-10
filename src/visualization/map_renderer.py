"""Minimal Pygame renderer for ODDS maps and contestant positions."""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping
import re
import sys
from typing import Any

import pygame

from src.core.map import Position, Terrain, WorldMap


TERRAIN_COLORS = {
    Terrain.GRASS: (119, 164, 105),
    Terrain.WATER: (83, 145, 190),
    Terrain.FOREST: (54, 112, 76),
    Terrain.ROCK: (145, 142, 132),
}
MARKER_COLORS = (
    (225, 81, 75),
    (245, 191, 67),
    (84, 133, 224),
    (188, 101, 202),
    (42, 171, 158),
    (238, 133, 61),
    (218, 103, 151),
    (99, 108, 119),
)
ANSI_TOKEN = re.compile(r"(\x1b\[[0-9;]*m)")
ANSI_COLORS = {
    30: (30, 30, 30),
    31: (205, 70, 65),
    32: (65, 155, 85),
    33: (205, 165, 55),
    34: (75, 115, 205),
    35: (175, 90, 180),
    36: (55, 155, 165),
    37: (220, 220, 215),
    90: (115, 120, 118),
    91: (245, 95, 85),
    92: (95, 195, 110),
    93: (245, 205, 85),
    94: (110, 150, 245),
    95: (215, 125, 220),
    96: (90, 205, 215),
    97: (245, 245, 240),
}


class _ConsoleTee:
    """Forward console output while also sending complete lines to the viewer."""

    def __init__(self, original: Any, on_line: Any):
        self.original = original
        self.on_line = on_line
        self.pending = ""

    def write(self, text: str) -> int:
        written = self.original.write(text)
        self.pending += text
        while "\n" in self.pending:
            line, self.pending = self.pending.split("\n", 1)
            if line.strip():
                self.on_line(line)
        return written

    def flush(self) -> None:
        self.original.flush()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.original, name)


def map_dimensions(world: WorldMap) -> tuple[int, int]:
    """Return map width and height, deriving them from tiles when needed."""
    tiles = getattr(world, "tiles", {})
    if tiles:
        width = max(x for x, _ in tiles) + 1
        height = max(y for _, y in tiles) + 1
    else:
        width = int(getattr(world, "width", 0))
        height = int(getattr(world, "height", 0))
    if width < 1 or height < 1:
        raise ValueError("Cannot render an empty map")
    return width, height


def world_to_screen(
    position: Position,
    tile_size: int,
    map_width: int,
    map_height: int,
    marker_radius: int = 0,
) -> tuple[int, int]:
    """Convert tile-space coordinates to pixels and keep them on the map."""
    max_x = map_width * tile_size
    max_y = map_height * tile_size
    inset = min(marker_radius, tile_size // 2)
    x = min(max(position.x * tile_size, inset), max_x - inset)
    y = min(max(position.y * tile_size, inset), max_y - inset)
    return round(x), round(y)


def _contestant_name(contestant: Any) -> str:
    return str(getattr(contestant, "name", contestant))


class MapRenderer:
    """Draw a WorldMap and its entity-to-Position mapping without mutating it."""

    def __init__(
        self,
        world: WorldMap,
        tile_size: int = 48,
        tick_duration: float = 0.5,
    ):
        if tile_size < 8:
            raise ValueError("tile_size must be at least 8 pixels")
        if tick_duration < 0:
            raise ValueError("tick_duration cannot be negative")
        pygame.init()
        self.world = world
        self.tile_size = tile_size
        self.tick_duration = tick_duration
        self.log_lines: deque[str] = deque(maxlen=500)
        self.width, self.height = map_dimensions(world)
        self.map_rect = pygame.Rect(0, 0, self.width * tile_size, self.height * tile_size)
        self.log_width = 380
        self._contestant_colors: dict[Any, tuple[int, int, int]] = {}
        for contestant in getattr(world, "positions", {}):
            self._color_for_contestant(contestant)
        self.legend_height = 30 + 18 * len(self._active_contestants())
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("ODDS Map Viewer")
        self.is_open = True
        self._clock = pygame.time.Clock()
        self._original_stdout = sys.stdout
        self._stdout_tee = _ConsoleTee(self._original_stdout, self.log_lines.append)
        sys.stdout = self._stdout_tee

    def _active_contestants(self) -> list[tuple[Any, Position]]:
        positions = getattr(self.world, "positions", {})
        return [
            (contestant, position)
            for contestant, position in positions.items()
            if isinstance(position, Position)
            and getattr(contestant, "alive", True)
        ]

    def _color_for_contestant(self, contestant: Any) -> tuple[int, int, int]:
        """Assign each contestant a color once and retain it for this viewer."""
        if contestant not in self._contestant_colors:
            index = len(self._contestant_colors)
            self._contestant_colors[contestant] = MARKER_COLORS[index % len(MARKER_COLORS)]
        return self._contestant_colors[contestant]

    @property
    def window_size(self) -> tuple[int, int]:
        return (
            self.map_rect.width + self.log_width,
            max(self.map_rect.height + self.legend_height, 560),
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((247, 247, 244))
        tiles: Mapping[tuple[int, int], Any] = getattr(self.world, "tiles", {})

        for y in range(self.height):
            for x in range(self.width):
                tile = tiles.get((x, y))
                terrain = getattr(tile, "terrain", Terrain.GRASS)
                color = TERRAIN_COLORS.get(terrain, (180, 180, 180))
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (230, 233, 226), rect, width=1)

        active = self._active_contestants()
        font = pygame.font.Font(None, 16)
        legend_font = pygame.font.Font(None, 15)
        legend_items = (
            (Terrain.GRASS, "Grass"),
            (Terrain.WATER, "Water"),
            (Terrain.FOREST, "Forest"),
            (Terrain.ROCK, "Rock"),
        )
        legend_x = 10
        for terrain, label in legend_items:
            pygame.draw.rect(surface, TERRAIN_COLORS[terrain], (legend_x, self.map_rect.height + 7, 10, 10))
            text = legend_font.render(label, True, (55, 58, 58))
            surface.blit(text, (legend_x + 14, self.map_rect.height + 5))
            legend_x += 14 + text.get_width() + 9

        radius = max(4, min(9, self.tile_size // 3))
        for index, (contestant, position) in enumerate(active):
            color = self._color_for_contestant(contestant)
            center = world_to_screen(position, self.tile_size, self.width, self.height, radius)
            pygame.draw.circle(surface, (255, 255, 255), center, radius + 2)
            pygame.draw.circle(surface, color, center, radius)

            label = font.render(_contestant_name(contestant), True, (42, 47, 50))
            row_y = self.map_rect.height + 27 + index * 18
            pygame.draw.circle(surface, color, (16, row_y + 6), 5)
            surface.blit(label, (27, row_y))

        panel_x = self.map_rect.width
        pygame.draw.rect(surface, (238, 240, 237), (panel_x, 0, self.log_width, surface.get_height()))
        pygame.draw.line(surface, (205, 210, 205), (panel_x, 0), (panel_x, surface.get_height()), 1)
        title_font = pygame.font.Font(None, 28)
        log_font = pygame.font.Font(None, 20)
        surface.blit(title_font.render("Simulation log", True, (35, 42, 40)), (panel_x + 18, 16))
        pygame.draw.line(surface, (205, 210, 205), (panel_x + 16, 48), (panel_x + self.log_width - 16, 48), 1)

        text_width = self.log_width - 36
        styled_lines: list[list[tuple[str, tuple[int, int, int], bool]]] = [[]]
        current_width = 0
        default_color = (55, 61, 58)
        for raw_line in self.log_lines:
            color = default_color
            bold = False
            for chunk in ANSI_TOKEN.split(raw_line):
                if chunk.startswith("\x1b["):
                    codes = [int(code) if code else 0 for code in chunk[2:-1].split(";")]
                    if 0 in codes:
                        color, bold = default_color, False
                    if 1 in codes:
                        bold = True
                    for code in codes:
                        if code in ANSI_COLORS:
                            color = ANSI_COLORS[code]
                    continue

                words = re.findall(r"\S+\s*|\s+", chunk)
                for word in words:
                    word_width = log_font.size(word)[0]
                    if current_width and current_width + word_width > text_width:
                        styled_lines.append([])
                        current_width = 0
                        word = word.lstrip()
                        word_width = log_font.size(word)[0]
                    if word:
                        styled_lines[-1].append((word, color, bold))
                        current_width += word_width
            styled_lines.append([])
            current_width = 0

        line_y = 60
        max_rows = max(0, (surface.get_height() - 70) // 22)
        visible_lines = styled_lines[-max_rows:] if max_rows else []
        for styled_line in visible_lines:
            line_x = panel_x + 18
            for text, color, bold in styled_line:
                log_font.set_bold(bold)
                rendered = log_font.render(text, True, color)
                surface.blit(rendered, (line_x, line_y))
                line_x += rendered.get_width()
            log_font.set_bold(False)
            line_y += 22

    def update_renderer(self) -> bool:
        """Redraw the latest world state and display it for ``tick_duration``.

        Call once after each simulation tick. The wait keeps the window
        responsive; set ``renderer.tick_duration`` to change the display time.
        Returns False after the user closes the window.
        """
        if not self.is_open:
            return False

        self.draw(self.screen)
        pygame.display.flip()
        deadline = pygame.time.get_ticks() + round(self.tick_duration * 1000)
        first_pass = True
        while self.is_open and (first_pass or pygame.time.get_ticks() < deadline):
            first_pass = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_open = False
            if self.is_open:
                self._clock.tick(60)
        if not self.is_open:
            self.close()
        return self.is_open

    def close(self) -> None:
        """Close the renderer window and release Pygame resources."""
        self.is_open = False
        pygame.display.quit()
        if sys.stdout is self._stdout_tee:
            sys.stdout = self._original_stdout


def run_renderer(world: WorldMap, tile_size: int = 48) -> None:
    """Open a static map view; closing the window exits the renderer."""
    renderer = MapRenderer(world, tile_size)
    while renderer.update_renderer():
        pass
    pygame.quit()


def sample_world() -> WorldMap:
    """Build a small standalone demo using the existing simulation types."""
    from src.contestants.contestant import Contestant

    world = WorldMap(height=12, width=18)
    terrain_rows = (
        (Terrain.FOREST, 2, 3),
        (Terrain.WATER, 8, 2),
        (Terrain.ROCK, 13, 4),
    )
    for terrain, start_x, start_y in terrain_rows:
        for y in range(start_y, min(start_y + 3, world.height)):
            for x in range(start_x, min(start_x + 3, world.width)):
                tile = world.tiles[(x, y)]
                world.set_tile(Position(x, y), type(tile)(tile.x, tile.y, terrain))

    demos = (
        ("Alex", 1.8, 1.6),
        ("Blair", 5.5, 4.2),
        ("Casey", 10.2, 6.8),
        ("Drew", 16.5, 10.3),
    )
    for name, x, y in demos:
        contestant = Contestant(name, "", 5, 5, 5)
        world.update_position(contestant, Position(x, y))
    return world


if __name__ == "__main__":
    run_renderer(sample_world())
