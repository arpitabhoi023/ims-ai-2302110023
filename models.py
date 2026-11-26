
import cadquery as cq
from cadquery import func as cf
from dataclasses import dataclass


@dataclass
class CellSpec:
    r_cell: float
    h_cell: float


def make_cell(spec):
    return cf.cylinder(d=2 * spec.r_cell, h=spec.h_cell)


def tray(spec, n=3, clearance=0.3, wall=4.0,
         thickness=6.0, depth=3.0):

    pocket_r = spec.r_cell + clearance
    pitch = 2 * pocket_r + wall

    length = n * pitch + wall
    width = 2 * pocket_r + 2 * wall

    plate = cf.box(length, width, thickness)

    pocket = cf.cylinder(
        d=2 * pocket_r,
        h=depth + 1
    ).moved(z=thickness - depth)

    # Create battery pockets
    for i in range(n):
        x = (i - (n - 1) / 2) * pitch
        plate = plate - pocket.moved(x=x)

    # Add two mirrored mounting holes
    for x in (-length / 2 + wall / 2,
              length / 2 - wall / 2):

        hole = cf.cylinder(
            d=3.0,
            h=thickness + 2
        )

        plate = plate - hole.moved(x=x, z=-1)

    return plate


# Three battery cell formats
cells = {
    "18650": CellSpec(9.0, 65.0),
    "21700": CellSpec(10.5, 70.0),
    "4680": CellSpec(23.0, 80.0)
}


# Generate and export all three trays
for name, spec in cells.items():

    model = tray(spec, n=3)

    filename = f"tray_{name}.stl"

    cq.exporters.export(
        model,
        filename
    )

    print(name, "tray created:", filename)
    print("Valid model:", model.isValid())
