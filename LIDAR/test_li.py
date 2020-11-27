scan = [100, 234.54, 180.3456789]

print("STOPPING - collision {:.2f}cm away".format(scan[2]/10))


def collision(safety_zone = 160):
    """
    Will detect if the robot is going to collide with an object
    """
    for scan in lidar.inter_scan():
        if scan[2] <= safety_zone:
            pi.set_servo_pulsewidth(ESC_both, min_throttle)