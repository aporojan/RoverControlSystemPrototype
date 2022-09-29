
# main controller input program

"""

Requirements:
    use pygame library to take controller input
    all motors on the rover must be independently controllable:
        leftWheel1, leftWheel2, leftWheel3, rightWheel1, rightWheel2, rightWheel3
        upperExtender, lowerExtender, screwdriver, claw, hoist, swivel
    use socket library to send packets to 2 microcontrollers
    all packets sent must be print()ed


Strict format for sending drive and arm command packets:
    DriveCommand_leftWheel1_rightWheel1_leftWheel2_rightWheel2_leftWheel3_rightWheel3
    ArmCommand_upperExtender_lowerExtender_screwdriver_claw_hoist_swivel

"""