import numpy as np
from math import *
import matplotlib.pyplot as plt

class CrankControlMechanism:
    def __init__(self, L1, L2, L3, L4, Rpx, t1, t2, t3, t4, a):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        self.Rpx = Rpx
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.a = a
        self.t = self.t3 - 180 + self.a - 90
        self.t = abs(self.t)
        self.C = self.Rpx

        # Initialize arrays for plotting
        self.n = np.array([])
        self.m = np.array([])

    @staticmethod
    def format_float(num):
        return np.format_float_positional(num, trim='-')

    def calculate_forces(self, T_input, x):
        # Compute angle t2 based on user input
        self.t2 = x
        self.update_matrices(T_input)
        Forces = np.dot(self.A_inverse, self.constant_matrix)
        Fshank = abs(Forces[8, 0])
        torque_shank = Fshank * 0.17
        return Fshank, torque_shank

    def update_matrices(self, T_input):
        # Update matrix based on current angles
        R12x = (self.L2 / 2) * cos(radians(self.t2) + pi)
        R12y = (self.L2 / 2) * sin(radians(self.t2) + pi)

        R32x = (self.L2 / 2) * cos(radians(self.t2))
        R32y = (self.L2 / 2) * sin(radians(self.t2))

        R23x = (self.L3 / 2) * cos(radians(self.t3))
        R23y = (self.L3 / 2) * sin(radians(self.t3))

        R43x = (self.L3 / 2) * cos(radians(self.t3) + pi)
        R43y = (self.L3 / 2) * sin(radians(self.t3) + pi)

        R34x = (self.L4 / 2) * cos(radians(self.t4))
        R34y = (self.L4 / 2) * sin(radians(self.t4))

        R14x = (self.L4 / 2) * cos(radians(self.t4) + pi)
        R14y = (self.L4 / 2) * sin(radians(self.t4) + pi)

        self.A = np.array([[1, 0, 1, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 1, 0, 0, 0, 0, 0],
                           [-R12y, R12x, -R32y, R32x, 0, 0, 0, 0, 0],
                           [0, 0, -1, 0, 1, 0, 0, 0, cos(radians(self.t))],
                           [0, 0, 0, -1, 0, 1, 0, 0, sin(radians(self.t))],
                           [0, 0, R23y, -R23x, -R43y, R43x, 0, 0, self.C],
                           [0, 0, 0, 0, -1, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, -1, 0, 1, 0],
                           [0, 0, 0, 0, R34y, -R34x, -R14y, R14x, 0]])

        self.A_inverse = np.linalg.inv(self.A)
        self.constant_matrix = np.array([[0],
                                        [0],
                                        [T_input],
                                        [0],
                                        [0],
                                        [0],
                                        [0],
                                        [0],
                                        [0]])

    def plot_results(self):
        plt.plot(self.n, self.m, 'r--')
        plt.xlabel('Crank Angle (degrees)')
        plt.ylabel('Output Shank Torque (Nm)')
        plt.title('Output Shank Torque vs Crank Angle')
        plt.grid(True)
        plt.show()

    def run(self):
        # Collect user inputs
        T_input = float(input('Enter any Torque measured at Crank (Nm): '))
        T_input = -T_input

        x = 0
        while x < 20 or x > 70:
            x = int(input('Enter the crank angle between 20 and 70 deg: '))

        # Calculate forces and update results
        Fshank, torque_shank = self.calculate_forces(T_input, x)
        self.n = np.append(self.n, x)
        self.m = np.append(self.m, torque_shank)
        print(f'At {x} deg the Output Shank Torque is: {torque_shank} Nm with Input crank Torque: {T_input} Nm')

        # Plot results
        self.plot_results()

if __name__ == "__main__":
    # Initialize parameters
    L1 = 17.4544 / 1000
    L2 = 35.5 / 1000
    L3 = 41.5415 / 1000
    L4 = 46.1494 / 1000
    Rpx = 0.15  # m
    t1 = 40  # theta1
    t2 = 20  # theta2
    t3 = 127  # theta3
    t4 = 101  # theta4
    a = 103  # alpha

    # Create mechanism instance and run
    mechanism = CrankControlMechanism(L1, L2, L3, L4, Rpx, t1, t2, t3, t4, a)
    mechanism.run()
