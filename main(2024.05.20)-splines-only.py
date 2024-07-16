import ezdxf
import numpy as np
import math
from scipy.interpolate import BSpline
import matplotlib.pyplot as plt

z_up = 2.00
z_down = 0.00
slow_feed_rate = 100.00
fast_feed_rate = 1000.00
y_max = 220.00
z_max = 150.00

file_name = "dxf/some-splines"
f360 = ezdxf.readfile(file_name + ".dxf")

msp = f360.modelspace()


def base_angle(angle):
    # Compute
    if angle >= 180:
        new_angle = base_angle(angle - 360)
    elif angle < -180:
        new_angle = base_angle(angle + 360)
    else:
        new_angle = angle
    return new_angle


def reset_angle(angle):
    if angle >= 0:
        if base_angle(angle) >= 0:
            new_angle = 360 * math.floor(angle / 360)
        else:
            new_angle = 360 * math.ceil(angle / 360)
    else:
        if base_angle(angle) >= 0:
            new_angle = (-360) * math.ceil(angle / (-360))
        else:
            new_angle = (-360) * math.floor(angle / (-360))
    return new_angle


gcodes = []
gcode = "G92 E0.00;"
print(gcode)
gcodes.append(gcode)
gcode = "G1 Z" + str('%.2f' %(z_up)) + " F" + str('%.2f' % (fast_feed_rate)) + ";"
print(gcode)
gcodes.append(gcode)
for entity in msp:
    if entity.dxftype() == 'SPLINE':
        # print("G1 X" + str(0) + " Y" + str(0) + "; Spline Started")
        spline_entity = entity
        control_points = np.array(spline_entity.control_points)
        knots = np.array(spline_entity.knots)
        degree = spline_entity.dxf.degree
        bspline = BSpline(knots, control_points, degree)
        x_control_points = [point[0] for point in control_points]
        y_control_points = [point[1] for point in control_points]
        num_segments = 100  # Number of segments
        t = np.linspace(knots[degree], knots[-(degree + 1)], num_segments + 1)
        bspline_points = bspline(t)
        # plt.plot(x_control_points, y_control_points, 'ro--', label='Control Points', alpha=0.50)
        # plt.plot(bspline_points[0], bspline_points[1], 'b-', label='B-Spline Curve')
        x_bspline_points = [point[0] for point in bspline_points]
        y_bspline_points = [point[1] for point in bspline_points]
        plt.plot(x_bspline_points, y_bspline_points, 'b-')
        plt.plot(x_bspline_points, y_bspline_points, 'bo-', label='BSpline Points', alpha=0.75)
        dbspline = bspline.derivative(nu=1)
        dbspline_points = dbspline(t)
        dbspline_norms = [np.linalg.norm(point) for point in dbspline_points]
        x_dbspline_points = [point[0] / norm for point, norm in zip(dbspline_points, dbspline_norms)]
        y_dbspline_points = [point[1] / norm for point, norm in zip(dbspline_points, dbspline_norms)]
        # plt.plot(x_dbspline_points, y_dbspline_points, 'go-', label='DBSpline Points', alpha=0.75)
        bspline_tangent_angle = []
        # Compute angles
        for i in range(len(x_bspline_points)):
            plt.arrow(x_bspline_points[i], y_bspline_points[i], x_dbspline_points[i], y_dbspline_points[i], width=0.10, color='r', alpha=0.5)
            if x_dbspline_points[i] > 0 and y_dbspline_points[i] == 0:
                angle = 0
            elif x_dbspline_points[i] == 0 and y_dbspline_points[i] > 0:
                angle = 90
            elif x_dbspline_points[i] < 0 and y_dbspline_points[i] == 0:
                angle = 180
            elif x_dbspline_points[i] == 0 and y_dbspline_points[i] < 0:
                angle = 270
            elif x_dbspline_points[i] != 0 and y_dbspline_points[i] > 0:
                angle = math.degrees(np.arccos(np.dot([x_dbspline_points[i], y_dbspline_points[i]], [1, 0])))
            elif x_dbspline_points[i] != 0 and y_dbspline_points[i] < 0:
                angle = 360 - math.degrees(np.arccos(np.dot([x_dbspline_points[i], y_dbspline_points[i]], [1, 0])))
            bspline_tangent_angle.append(angle)
        # Arrange angles
        for i in range(len(bspline_tangent_angle)):
            if i == 0:
                if bspline_tangent_angle[i] < -180:
                    bspline_tangent_angle[i] = bspline_tangent_angle[i] + 360
                if bspline_tangent_angle[i] > 180:
                    bspline_tangent_angle[i] = bspline_tangent_angle[i] - 360
            else:
                if bspline_tangent_angle[i] - bspline_tangent_angle[i - 1] < -180:
                    bspline_tangent_angle[i] = bspline_tangent_angle[i] + 360
                if bspline_tangent_angle[i] - bspline_tangent_angle[i - 1] > 180:
                    bspline_tangent_angle[i] = bspline_tangent_angle[i] - 360
        for i in range(len(bspline_tangent_angle)):
            if i == 0:
                gcode = "G1 X" + str('%.2f' %(x_bspline_points[i])) + " Y" + str('%.2f' %(y_bspline_points[i])) + " E" + str('%.2f' %(bspline_tangent_angle[i])) + "; Cutting Spline Started"
                print(gcode)
                gcodes.append(gcode)
                gcode = "G1 Z" + str('%.2f' %(z_down)) + " F" + str('%.2f' %(slow_feed_rate)) + ";"
                print(gcode)
                gcodes.append(gcode)
            else:
                gcode = "G1 X" + str('%.2f' %(x_bspline_points[i])) + " Y" + str('%.2f' %(y_bspline_points[i])) + " E" + str('%.2f' %(bspline_tangent_angle[i])) + ";"
                print(gcode)
                gcodes.append(gcode)
        gcode = "G1 Z" + str('%.2f' %(z_up)) + " F" + str('%.2f' % (fast_feed_rate)) + "; Cutting Spline Finished"
        print(gcode)
        gcodes.append(gcode)
        final_angle = reset_angle(bspline_tangent_angle[-1])
        gcode = "G1 E" + str('%.2f' %(final_angle)) + ";"
        print(gcode)
        gcodes.append(gcode)
        gcode = "G92 E0.00;"
        print(gcode)
        gcodes.append(gcode)
gcode = "G1 Z" + str('%.2f' %(z_max)) + "; Process Finished"
print(gcode)
gcodes.append(gcode)
gcode = "G1 Y" + str('%.2f' %(y_max)) + ";"
print(gcode)
gcodes.append(gcode)
gcode = ""
print(gcode)
gcodes.append(gcode)

# Save the GCode File
gcode_file = open(file_name + ".gcode", "w")
gcode_file.write("\n".join(gcodes))
gcode_file.close()

# Add labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('B-Spline Curve')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
