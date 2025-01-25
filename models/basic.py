from build123d import *
from ocp_vscode import *

with BuildPart() as main:
    Box(10, 20, 30)
    Cylinder(10, 20, mode=Mode.SUBTRACT)

main.part.color = "#FF2244EE"
main.part.name = "main"

show(main.part)