#!/usr/bin/python3
# Basic 2D IK example of AL5 + Python (library)

import math
import serial


def ard_constrain(value, min, max):
    if value < min:
        value = min
    if value > max:
        value = max
    return value


def ard_map(value, min1, max1, min2, max2):
    value = ((value - min1) * (max2 - min2) / (max1 - min1) + min2)
    return value


class AL5D:
    def __init__(self):
        # open serial port
        self.sp = serial.Serial('/dev/ttyUSB0', 9600)
        # set constant values
        self.A = 146.1  # mm  # shoulder_to_elbow
        self.B = 187.3  # mm  # elbow_to_wrist
        # Radians to degrees constant
        self.rad_to_deg = 57.295779  # Radians to degrees constant
        # CST RC values
        self.CST_ANGLE_MIN = 0
        self.CST_ANGLE_MAX = 180
        self.CST_RC_MIN = 500
        self.CST_RC_MAX = 2500

        self.current_angles = [0, 90, 90, 90, 0, 0]

    def go_home(self):
        self.current_angles = [0, 160, 40, 100, 0]

    def get_pulse_from_angle(self, angle):
        angle = ard_constrain(angle, self.CST_ANGLE_MIN, self.CST_ANGLE_MAX)
        pulse = ard_map(angle, self.CST_ANGLE_MIN, self.CST_ANGLE_MAX, self.CST_RC_MIN, self.CST_RC_MAX)
        return int(pulse)

    def write_angles_to_servos(self, angle_array, time_to_complete):
        """writes input angles from array to the servo corresponding to their index"""
        # Get values from angles to pulses (µs)
        pulse_____base = self.get_pulse_from_angle(angle_array[0] + 36)
        pulse_shoulder = self.get_pulse_from_angle(angle_array[1] - 10)
        pulse____elbow = self.get_pulse_from_angle(180 - angle_array[2])
        pulse____wrist = self.get_pulse_from_angle(angle_array[3])
        pulse_____grab = self.get_pulse_from_angle(angle_array[4])

        # Get values from speeds
        speed_____base = pulse_____base / time_to_complete
        speed_shoulder = pulse_shoulder / time_to_complete
        speed____elbow = pulse____elbow / time_to_complete
        speed____wrist = pulse____wrist / time_to_complete
        speed_____grab = pulse_____grab / time_to_complete

        # Write values to SSC-32U
        write = []
        write.append("#0 P" + str(pulse_____base) + " S" + str(speed_____base) + "\r")
        write.append("#1 P" + str(pulse_shoulder) + " S" + str(speed_shoulder) + "\r")
        write.append("#2 P" + str(pulse____elbow) + " S" + str(speed____elbow) + "\r")
        write.append("#3 P" + str(pulse____wrist) + " S" + str(speed____wrist) + "\r")
        write.append("#4 P" + str(pulse_____grab) + " S" + str(speed_____grab) + "\r")
        # write[5] = "#5 P" + str(pulseWR) + " S" + str(speedWR) + "\r"

        for i in write:
            print(i)
        for i in write:
            self.sp.write(i.encode())

    def angles_from_cylindrical(self, radius, theta, height):
        """returns array of angles based on radius (in mm), theta (in degrees), height (in mm)"""
        # base
        angle_base = theta
        #
        print("base")
        print(angle_base)
        length_hypotenuse = math.sqrt(radius * radius + height * height)
        print("hypotenuse")
        print(length_hypotenuse)
        angle_hypotenuse_radius = 57.295779 * math.atan(height / radius)
        print("angle hr")
        print(angle_hypotenuse_radius)
        angle_a_hypotenuse = 57.295779 * math.acos((self.A * self.A - self.B * self.B + length_hypotenuse *
                                                    length_hypotenuse) / ((self.A * 2) * length_hypotenuse))
        print("angle ah")
        print(angle_a_hypotenuse)
        angle_elbow = 57.295779 * math.acos((self.A * self.A + self.B * self.B - length_hypotenuse *
                                             length_hypotenuse) / ((self.A * 2) * self.B))
        print("elbow")
        print(angle_elbow)
        angle_shoulder = angle_a_hypotenuse + angle_hypotenuse_radius
        print("shoulder")
        print(angle_shoulder)
        angle_wrist = math.fabs(90 - angle_hypotenuse_radius)  # (wa - Elbow - Shoulder) - 90
        print("wrist")
        print(angle_wrist)
        return [angle_base, angle_elbow, angle_shoulder, angle_wrist, 0]

    def angles_from_cartesian(self, x, y, z):
        """returns array of angles based on x, y, z (in mm from 0, 0, 0 at shoulder)"""
        radius = math.sqrt(x * x + z * z)
        # set theta
        theta = 0
        if x > 0:
            theta += math.atan(z / x) * self.rad_to_deg  # theta += arcsin(opposite / adjacent)
        else:
            theta = 90 - math.atan(x / z) * self.rad_to_deg
        # now use cylindrical function
        return self.angles_from_cylindrical(radius, theta, y)

    def __del__(self):
        print("< Returning Home... >")
        self.go_home()
        # Set all motors to idle/unpowered (pulse = 0)
        print("< Idling motors... >")
        for i in range(0, 6):
            print(("#" + str(i) + " P" + str(0) + "\r").encode())
            self.sp.write(("#" + str(i) + " P" + str(0) + "\r").encode())
        print("< Done >")
        del self.sp


arm = AL5D()
arm.write_angles_to_servos(arm.current_angles, 10)


# while input("continue?") == "y":
#     x = input("x: ")
#     y = input("y: ")
#     z = input("z: ")
#     arm.current_angles = arm.angles_from_cartesian(int(x), int(y), int(z))
#     arm.write_angles_to_servos(arm.current_angles, 10)

servo = input("enter servo number: ")
while servo.isnumeric():
    arm.current_angles[int(servo)] = int(input("enter angle in degrees: "))
    arm.write_angles_to_servos(arm.current_angles, 10)
    servo = input("enter servo number: ")
