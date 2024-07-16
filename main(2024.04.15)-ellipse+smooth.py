import ezdxf
import math

file_name = "dxf/eyes"
f360 = ezdxf.readfile(file_name + ".dxf")
XOffset = 60.0
YOffset = 20.0
ZUp = 1.0
ZDown = 0.1

msp = f360.modelspace()

# Read Circles and Append in an Array
# Convert Them into Ellipses
circles = [entity for entity in msp if entity.dxftype() == "CIRCLE"]
for circle in circles:
    circle.to_ellipse(True)

# Read Ellipses and Append in an Array
ellipses = [entity for entity in msp if entity.dxftype() == "ELLIPSE"]
gcode = []
gcode.append("G1 F250")
gcode.append("G92 X0 Y0")
# Go to Origin
for ellipse in ellipses:
    center_x = float(ellipse.dxf.center[0])
    center_y = float(ellipse.dxf.center[1])
    radius_a = abs(float(ellipse.dxf.major_axis[0]))
    radius_b = abs(float(ellipse.minor_axis[1]))

    numlines = 10 * math.ceil(math.sqrt(radius_a ** 2 + radius_b ** 2))
    for k in range(numlines + 1):
        s = float(k * 2 * math.pi / numlines - math.pi / 2)
        xp = float(center_x + radius_a * math.cos(s))
        yp = float(center_y + radius_b * math.sin(s))

        if k == 0:
            gcode.append("G0 X" + str('%.2f' % (xp)) + " Y" + str('%.2f' % (yp)))
            gcode.append("G1 Z" + str(ZDown) + "; Z Down")
        else:
            if math.sin(s) == 0:
                if math.cos(s) > 0:
                    angle = 90.00
                elif math.cos(s) < 0:
                    angle = 270.00
            if math.sin(s) > 0 and math.cos(s) > 0:
                # First Quadrant
                angle = 180 + float(math.degrees((-1) * math.atan((radius_b * math.cos(s)) / (radius_a * math.sin(s)))))
            elif math.sin(s) < 0 and math.cos(s) > 0:
                # Second Quadrant
                angle = float(math.degrees((-1) * math.atan((radius_b * math.cos(s)) / (radius_a * math.sin(s)))))
            elif math.sin(s) < 0 and math.cos(s) < 0:
                # Third Quadrant
                angle = 360 + float(math.degrees((-1) * math.atan((radius_b * math.cos(s)) / (radius_a * math.sin(s)))))
            elif math.sin(s) > 0 and math.cos(s) < 0:
                # Fourth Quadrant
                angle = 180 + float(math.degrees((-1) * math.atan((radius_b * math.cos(s)) / (radius_a * math.sin(s)))))
            print(k, angle, xp, yp, math.sin(s), math.cos(s))
            gcode.append("G1 X" + str('%.2f' % (xp)) + " Y" + str('%.2f' % (yp)) + " E" + str('%.2f' % (angle)))

    gcode.append("G1 Z" + str(ZUp) + "; Z Up")
    # Leave the Blade Parallel to the x-Axis
    gcode.append("G92 E0; Reset the Blade Angle")
gcode.append("")

# Save the GCode File
gcode_file = open(file_name + ".gcode", "w")
gcode_file.write("\n".join(gcode))
gcode_file.close()
