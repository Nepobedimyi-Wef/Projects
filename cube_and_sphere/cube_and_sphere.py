class Calc1:
    def __init__(self, cube_side, sphere_radius):
        self.cube_side = cube_side
        self.sphere_radius = sphere_radius

    def cube_area(self):
        print(f"{self.cube_side ** 2 * 6}")

    def v_sphere(self):
        print(f"{4/3 * 3.14 * self.sphere_radius ** 3}")

class Calc2:
    def __init__(self, cube_side, sphere_radius):
        self.cube_side = cube_side
        self.sphere_radius = sphere_radius

    def cube_area(self):
        print(f"{self.cube_side ** 2 * 6}")

    def v_sphere(self):
        print(f"{4/3 * 3.14 * self.sphere_radius ** 3}")

cube_side = int(input('Введите сторону куба: '))
sphere_radius = int(input('Введите радиус сферы: '))

Cube = Calc1(cube_side, sphere_radius)
Sphere = Calc2(cube_side, sphere_radius)

for calc in (Cube, Sphere):
    calc.cube_area()
    calc.v_sphere()
