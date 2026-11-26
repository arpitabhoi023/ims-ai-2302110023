
from cadquery import func as cf

plate = cf.box(80, 50, 10)
hole = cf.cylinder(d=20, h=10)

part = plate - hole

print(part.isValid())
print(round(part.Volume(), 1))

part.exportStl("plate.stl")
