#!/usr/bin/env python3
"""Solve the 8x8 pentomino board with the four corners removed."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable


BOARD_SIZE = 8
LETTERS = "ABCDEFGH"
REMOVED_CELLS = {(0, 0), (7, 0), (0, 7), (7, 7)}

PENTOMINOES = {
    "F": [(1, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
    "I": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    "L": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],
    "P": [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)],
    "N": [(2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
    "T": [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)],
    "U": [(0, 0), (2,  0), (0, 1), (1, 1), (2, 1)],
    "V": [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    "W": [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
    "X": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "Y": [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)],
    "Z": [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
}


@dataclass(frozen=True)
class Placement:
    piece: str
    cells: tuple[tuple[int, int], ...]


def normalize(cells: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    cells = tuple(cells)
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def orientations(cells: list[tuple[int, int]]) -> set[tuple[tuple[int, int], ...]]:
    result = set()
    for x_sign in (1, -1):
        for y_sign in (1, -1):
            transformed = [(x * x_sign, y * y_sign) for x, y in cells]
            result.add(normalize(transformed))
            result.add(normalize((y, x) for x, y in transformed))
    return result


def shape_signature(cells: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    return min(orientations(cells))


def cell_name(cell: tuple[int, int]) -> str:
    x, y = cell
    return f"{LETTERS[x]}{y + 1}"


def build_placements() -> list[Placement]:
    board_cells = {
        (x, y)
        for y in range(BOARD_SIZE)
        for x in range(BOARD_SIZE)
        if (x, y) not in REMOVED_CELLS
    }
    placements = []

    for piece, cells in PENTOMINOES.items():
        for shape in orientations(cells):
            width = max(x for x, _ in shape) + 1
            height = max(y for _, y in shape) + 1
            for y_offset in range(BOARD_SIZE - height + 1):
                for x_offset in range(BOARD_SIZE - width + 1):
                    placed = tuple(
                        sorted((x + x_offset, y + y_offset) for x, y in shape)
                    )
                    if all(cell in board_cells for cell in placed):
                        placements.append(Placement(piece, placed))

    return placements


def solve(limit: int | None = None):
    placements = build_placements()
    columns = [f"piece:{piece}" for piece in PENTOMINOES]
    columns.extend(f"cell:{cell_name(cell)}" for cell in sorted(valid_cells()))

    rows = []
    for placement in placements:
        row_columns = {f"piece:{placement.piece}"}
        row_columns.update(f"cell:{cell_name(cell)}" for cell in placement.cells)
        rows.append((placement, row_columns))

    column_to_rows = {column: set() for column in columns}
    for row_index, (_, row_columns) in enumerate(rows):
        for column in row_columns:
            column_to_rows[column].add(row_index)

    active_columns = set(columns)
    active_rows = set(range(len(rows)))
    partial: list[int] = []
    found = 0

    def search():
        nonlocal found
        if limit is not None and found >= limit:
            return
        if not active_columns:
            found += 1
            yield [rows[row_index][0] for row_index in partial]
            return

        column = min(
            active_columns,
            key=lambda c: len(column_to_rows[c] & active_rows),
        )
        candidates = list(column_to_rows[column] & active_rows)
        if not candidates:
            return

        for row_index in candidates:
            placement, row_columns = rows[row_index]
            removed_columns = set()
            removed_rows = set()

            partial.append(row_index)
            for covered_column in row_columns:
                if covered_column in active_columns:
                    active_columns.remove(covered_column)
                    removed_columns.add(covered_column)
                for conflicting_row in column_to_rows[covered_column] & active_rows:
                    active_rows.remove(conflicting_row)
                    removed_rows.add(conflicting_row)

            yield from search()

            active_rows.update(removed_rows)
            active_columns.update(removed_columns)
            partial.pop()

    yield from search()


def valid_cells() -> set[tuple[int, int]]:
    return {
        (x, y)
        for y in range(BOARD_SIZE)
        for x in range(BOARD_SIZE)
        if (x, y) not in REMOVED_CELLS
    }


def render(solution: list[Placement]) -> str:
    grid = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for x, y in REMOVED_CELLS:
        grid[y][x] = "#"
    for placement in solution:
        for x, y in placement.cells:
            grid[y][x] = placement.piece

    lines = ["   A B C D E F G H"]
    for y, row in enumerate(grid, start=1):
        lines.append(f"{y}  {' '.join(row)}")
    return "\n".join(lines)


def placement_coordinates(solution: list[Placement]) -> str:
    parts = []
    for placement in sorted(solution, key=lambda p: p.piece):
        cells = " ".join(cell_name(cell) for cell in placement.cells)
        parts.append(f"{placement.piece}: {cells}")
    return "\n".join(parts)


def solution_summary(solution: list[Placement]) -> str:
    pieces = sorted(placement.piece for placement in solution)
    repeated = sorted(piece for piece in set(pieces) if pieces.count(piece) > 1)
    shape_signatures = {
        piece: shape_signature(cells) for piece, cells in PENTOMINOES.items()
    }
    duplicate_shapes = sorted(
        (
            piece
            for piece, signature in shape_signatures.items()
            if list(shape_signatures.values()).count(signature) > 1
        )
    )

    if pieces == sorted(PENTOMINOES) and not repeated and not duplicate_shapes:
        return "Pieces utilisees: 12 formes differentes (F I L N P T U V W X Y Z), une fois chacune."
    if duplicate_shapes:
        return f"Attention: forme(s) de pentamino en double: {' '.join(duplicate_shapes)}"
    if repeated:
        return f"Attention: piece(s) en double: {' '.join(repeated)}"
    return f"Attention: pieces trouvees: {' '.join(pieces)}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solve an 8x8 pentomino board with A1, A8, H1 and H8 empty."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="maximum number of solutions to print; use 0 to count all solutions",
    )
    parser.add_argument(
        "--coords",
        action="store_true",
        help="also print each pentomino placement as board coordinates",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    limit = None if args.limit == 0 else args.limit
    count = 0

    for count, solution in enumerate(solve(limit), start=1):
        if args.limit != 0:
            print(f"Solution {count}")
            print(solution_summary(solution))
            print(render(solution))
            if args.coords:
                print()
                print(placement_coordinates(solution))
            print()

    if args.limit == 0:
        print(f"{count} solution(s)")
    elif count == 0:
        print("Aucune solution trouvee.")


if __name__ == "__main__":
    main()
