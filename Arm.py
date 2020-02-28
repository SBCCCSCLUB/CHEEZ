#!/usr/bin/python3
# Basic 2D IK example of AL5 + Python (library)

import math
import serial
import time


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
        self.CST_RC_MIN = 700
        self.CST_RC_MAX = 2500
        # post process physical limit angles
        self.minAngles = [0, 0, 21, 0, 0, 0]  # TODO populate minimum allowable angles
        self.maxAngles = [180, 180, 180, 180, 180, 180]  # TODO populate maximum allowable angles

        self.current_angles = [0, 90, 90, 90, 0, 0]
        self.go_home(1)

    def go_home(self, time_to=  10):
        self.current_angles = [0, 170, 25, 120, 0]
        self.write_angles_to_servos(self.current_angles, time_to)
        time.sleep(time_to)

    def get_pulse_from_angle(self, angle):
        angle = ard_constrain(angle, self.CST_ANGLE_MIN, self.CST_ANGLE_MAX)
        pulse = ard_map(angle, self.CST_ANGLE_MIN, self.CST_ANGLE_MAX, self.CST_RC_MIN, self.CST_RC_MAX)
        return int(pulse)

    def check_angles_in_physical_range(self, angle_array):
        for servo_index in range(len(angle_array)):
            if angle_array[servo_index] < self.minAngles[servo_index]:
                angle_array[servo_index] = self.minAngles[servo_index]
                print("!Warn: Angle on servo " + str(servo_index) + "below physical capability. Setting to " +
                      str(angle_array[servo_index]))
            elif angle_array[servo_index] > self.maxAngles[servo_index]:
                angle_array[servo_index] = self.maxAngles[servo_index]
                print("!Warn: Angle on servo " + str(servo_index) + "above physical capability. Setting to " +
                      str(angle_array[servo_index]))

    def write_angles_to_servos(self, angle_array, time_to_complete):
        """writes input angles from array to the servo corresponding to their index"""
        print("input angle array: " + str(angle_array))
        self.check_angles_in_physical_range(angle_array)

        # Get values from angles to pulses (µs)
        pulse_____base = self.get_pulse_from_angle(angle_array[0] + 36)
        pulse_shoulder = self.get_pulse_from_angle(angle_array[1] - 10)
        pulse____elbow = self.get_pulse_from_angle(180 - angle_array[2])
        pulse____wrist = self.get_pulse_from_angle(250 - angle_array[3])  # 180 - [angle from bottom of B] + 70
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
        print("< Calculating Motor Angles from Cylindrical... >")
        # TODO prevent use of coordinates out of range
        # do math
        # Base is just theta
        angle_base = theta
        print("Servo Angle:        Base: " + str(angle_base))
        # calculate length of hypotenuse (shoulder to wrist)
        length_hypotenuse = math.sqrt(radius * radius + height * height)
        print("     Length:  Hypotenuse: " + str(length_hypotenuse))
        #
        angle_hypotenuse_radius = 57.295779 * math.atan(height / radius)
        print("      Angle: between the Horizon and the Hypotenuse: " + str(angle_hypotenuse_radius))
        #
        angle_a_hypotenuse_ratio = (self.A * self.A - self.B * self.B + length_hypotenuse * length_hypotenuse) \
                                   / ((self.A * 2) * length_hypotenuse)
        if angle_a_hypotenuse_ratio >= 1:
            angle_a_hypotenuse_ratio = 1
            print("!Warn: ah ratio greater than 1")
        elif angle_a_hypotenuse_ratio <= -1:
            angle_a_hypotenuse_ratio = -1
            print("!Warn: ah ratio less than -1")
        angle_a_hypotenuse = 57.295779 * math.acos(angle_a_hypotenuse_ratio)
        print("      Angle: between A and Hypotenuse: " + str(angle_a_hypotenuse))
        #
        angle_elbow_ratio = (self.A * self.A + self.B * self.B - length_hypotenuse * length_hypotenuse)\
                            / ((self.A * 2) * self.B)
        if angle_elbow_ratio >= 1:
            angle_elbow_ratio = 1
            print("!Warn: elbow ratio greater than 1")
        elif angle_elbow_ratio <= -1:
            angle_elbow_ratio = -1
            print("!Warn: elbow ratio less than -1")
        angle_elbow = 57.295779 * math.acos(angle_elbow_ratio)
        print("Servo Angle:       Elbow: " + str(angle_elbow))
        #
        angle_shoulder = angle_a_hypotenuse + angle_hypotenuse_radius
        print("Servo Angle:    Shoulder: " + str(angle_shoulder))
        #
        angle_wrist = math.fabs(270 - angle_a_hypotenuse - angle_hypotenuse_radius - angle_elbow)
        print("Servo Angle:       Wrist: " + str(angle_wrist))
        #
        print("< Done >")
        return [angle_base, angle_shoulder, angle_elbow, angle_wrist, 0]

    def angles_from_cartesian(self, x_mm, y_mm, z_mm):
        """returns array of angles based on x_mm, y_mm, z_mm (in mm from 0, 0, 0 at shoulder)"""
        print("< Calculating Cylindrical Coordinates from Cartesian... >")
        # TODO prevent use of coordinates out of range
        # calculate radius
        radius = math.sqrt(x_mm * x_mm + z_mm * z_mm)
        print("Radius: " + str(radius))
        # calculate theta
        theta = 0
        if x_mm > 0:
            theta += math.atan(z_mm / x_mm) * self.rad_to_deg  # theta += arcsin(opposite / adjacent)
        else:
            theta = 90 - math.atan(x_mm / z_mm) * self.rad_to_deg
        print(" Theta: " + str(theta))
        # print height
        print("Height: " + str(y_mm))
        # now use cylindrical function
        print("< Done >")
        return self.angles_from_cylindrical(radius, theta, y_mm)

    def __del__(self):
        print("< Returning Home... >")
        self.go_home(2)
        # Set all motors to idle/unpowered (pulse = 0)
        print("< Idling motors... >")
        for i in range(0, 6):
            print(("#" + str(i) + " P" + str(0) + "\r").encode())
            self.sp.write(("#" + str(i) + " P" + str(0) + "\r").encode())
        print("< Done >")
        del self.sp


arm = AL5D()
time.sleep(2)
arm.write_angles_to_servos(arm.current_angles, 30)

while input("Continue?(y/n) ") == "y":
    while input("Cartesian   | Continue?(y/n) ") == "y":
        x = input("x: ")
        y = input("y: ")
        z = input("z: ")
        arm.current_angles = arm.angles_from_cartesian(int(x), int(y), int(z))
        arm.write_angles_to_servos(arm.current_angles, 10)

    while input("Cylindrical | Continue?(y/n) ") == "y":
        radius = int(input("radius: "))
        theta = int(input("theta: "))
        height = int(input("height: "))
        arm.current_angles = arm.angles_from_cylindrical(radius, theta, height)
        arm.write_angles_to_servos(arm.current_angles, 10)

    while input("Servos      | Continue?(y/n) ") == "y":
        servo = input("enter servo number: ")
        while servo.isnumeric() and int(servo) <= 4 and int(servo) >= 0:
            arm.current_angles[int(servo)] = int(input("enter angle in degrees: "))
            arm.write_angles_to_servos(arm.current_angles, 10)
            servo = input("enter servo number: ")
