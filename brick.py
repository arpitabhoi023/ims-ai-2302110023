
import math
from cadquery import Workplane as cq

def clutch_brick(length, width, height,
                 stud_d, stud_h, spacing):

    body = cq.box(length, width, height)

    # Create 2 rows and 4 columns of studs
    for row in range(2):
        for col in range(4):
            x = (col - 1.5) * spacing
            y = (row - 0.5) * spacing

            stud = cq.Workplane("XY").circle(
                stud_d / 2
            ).extrude(stud_h).translate(
                (x, y, height)
            )

            body = body.union(stud)

    expected = (length * width * height +
                8 * math.pi * (stud_d / 2)**2 * stud_h)

    assert abs(body.val().Volume() - expected) < 0.5

    body.export("brick.stl")

brick = clutch_brick(15.6, 7.8, 9.6, 4.8, 1.7, 8.0)
