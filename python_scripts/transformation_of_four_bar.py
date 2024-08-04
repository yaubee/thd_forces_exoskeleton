import numpy as np
from math import *

np.set_printoptions(suppress=True)

class FourBarMechanism:
    def __init__(self, L1, L2, L3, L4, L5, t1, t2, a, b, t4):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        self.L5 = L5
        self.t1 = t1
        self.t2 = t2
        self.a = a
        self.b = b
        self.t4 = t4

        self.trig_t1 = -self.t1
        self.trig_t2 = -self.t2

        # Compute initial angles
        self.compute_shank_angles()
        self.compute_link_points()

    def shank_angle(self):
        k1 = self.L1 / self.L2
        k2 = self.L1 / self.L3
        k3 = ((self.L4**2) - (self.L1**2) - (self.L2**2) - (self.L3**2)) / (2 * self.L2 * self.L3)
        E = -2 * sin(radians(self.t2))
        D = k2 * cos(radians(self.t2)) + cos(radians(self.t2)) + k3 - k1
        F = k2 * cos(radians(self.t2)) - cos(radians(self.t2)) + k3 + k1
        angle = 2 * degrees(atan((-E + sqrt(E**2 - 4 * D * F)) / (2 * D)))

        if angle < 0:
            angle += 360

        return angle

    def compute_shank_angles(self):
        t = self.shank_angle()
        self.tc_coupler = -(t + abs(self.t1))
        self.tc_coupler_hor = t + self.t1
        self.tshank_hor = self.tc_coupler_hor - self.b
        self.tc_coupler_ver = t + self.t1 - 90
        self.tshank_ver = self.tc_coupler_ver - self.b

        if t < 0:
            self.tshank_ver += 360

    @staticmethod
    def translate_point(start, vx, vy):
        translation_vector = np.array([[vx], [vy]])
        end_point = np.add(start, translation_vector)
        return end_point

    @staticmethod
    def trig_pyth(start, length, angle, inverse=0):
        rotation_angle = -inverse * pi / 2
        translation = np.array([[length * cos(radians(angle))],
                                [length * sin(radians(angle))]])
        rotation_matrix = np.array([[cos(rotation_angle), -sin(rotation_angle)],
                                    [sin(rotation_angle), cos(rotation_angle)]])
        rotated_translation = rotation_matrix.dot(translation)
        end_point = np.add(start, rotated_translation)
        return end_point

    @staticmethod
    def line_equation(start, end):
        start = np.append(start, [[1]], axis=0)
        end = np.append(end, [[1]], axis=0)
        return np.cross(start, end, axis=0)

    @staticmethod
    def intersect_lines(s1, e1, s2, e2):
        eq1 = FourBarMechanism.line_equation(s1, e1)
        eq2 = FourBarMechanism.line_equation(s2, e2)
        prod = np.cross(eq1, eq2, axis=0)
        if prod[2, 0] != 0:
            intersection = np.array([[prod[0, 0] / prod[2, 0]],
                                     [prod[1, 0] / prod[2, 0]]])
            return intersection

    def compute_link_points(self):
        self.p1 = np.array([[0], [0]])
        self.p2 = self.trig_pyth(self.p1, self.L1, self.trig_t1, 0)
        self.p4 = self.trig_pyth(self.p1, self.L2, self.trig_t1 + self.trig_t2, 0)
        self.p3 = self.trig_pyth(self.p4, self.L3, self.tc_coupler, 0)
        self.p5 = (self.p3 + self.p4) / 2
        self.p6 = self.trig_pyth(self.p5, self.L5, -self.tshank_ver, 1)

        self.icr = self.intersect_lines(self.p1, self.p4, self.p2, self.p3)

    def print_results(self):
        print('Input angle:', self.t2)
        print('Shank output angle to horizontal:', self.tshank_hor)
        print('p1:', self.p1)
        print('p2:', self.p2)
        print('p4:', self.p4)
        print('p3:', self.p3)
        print('p5:', self.p5)
        print('p6:', self.p6)
        print('ICR:', self.icr)

if __name__ == "__main__":
    # 4-bar linkage parameters:
    L1 = 17.45
    L2 = 35.75
    L3 = 41.89
    L4 = 46.15
    L5 = 30.00
    t1 = 40.23
    t2 = 20
    a = 103.15
    b = 180. - a
    t4 = 100.83

    mechanism = FourBarMechanism(L1, L2, L3, L4, L5, t1, t2, a, b, t4)
    mechanism.print_results()
