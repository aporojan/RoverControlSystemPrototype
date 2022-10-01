
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

Pygame library joystick example code:
	https://www.pygame.org/docs/ref/joystick.html#module-pygame.joystick

Socket library documentation:
	https://docs.python.org/3/library/socket.html

"""

from asyncio.windows_events import NULL
from math import ceil
import pygame
import socket
debug = False

# Simple class to print to the screen in pygame
class TextPrint(object):
	def __init__(self):
		self.reset()
		self.font = pygame.font.Font(None, 20)

	def tprint(self, screen, textString):
		textBitmap = self.font.render(textString, True, BLACK)
		screen.blit(textBitmap, (self.x, self.y))
		self.y += self.line_height

	def reset(self):
		self.x = 10
		self.y = 10
		self.line_height = 15

	def indent(self):
		self.x += 10

	def unindent(self):
		self.x -= 10

# Function to update the screen
def DrawFrame():
	global frame_time, joystick

	frame_time = 0
	screen.fill(WHITE)
	textPrint.reset()

	if joystick_count == 0:
		textPrint.tprint(screen, "No Joystick detected!")

	else:
		textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
		textPrint.indent()

		textPrint.tprint(screen, "Joystick: {}".format(jid))
		textPrint.indent()

		textPrint.tprint(screen, "Joystick name: {}".format(name))
		textPrint.tprint(screen, "GUID: {}".format(guid))

		# Check axis movement
		axes = joystick.get_numaxes()
		textPrint.tprint(screen, "Number of axes: {}".format(axes))
		textPrint.indent()

		for i in range(axes):
			axis = joystick.get_axis(i)
			textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(axisMap[i], axis))
		textPrint.unindent()

		# Check button press/release
		buttons = joystick.get_numbuttons()
		textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
		textPrint.indent()

		for i in range(ACTUAL_BUTTONS_IN_USE):
			button = joystick.get_button(i)
			textPrint.tprint(screen, "{} value: {}".format(buttonMap[i], button))
		textPrint.unindent()

		# Check D-pad button press/release
		hats = joystick.get_numhats()
		textPrint.tprint(screen, "Number of hats: {}".format(hats))
		textPrint.indent()

		# Hat position is a tuple of int values (x, y)
		for i in range(hats):
			hat = joystick.get_hat(i)
			if hat[0] == 1: dPadMap[0] = "right"
			elif hat[0] == -1: dPadMap[0] = "left"
			else: dPadMap[0] = ""
			if hat[1] == 1: dPadMap[1] = "up"
			elif hat[1] == -1: dPadMap[1] = "down"
			else: dPadMap[1] = ""
			textPrint.tprint(screen, "DPAD horizontal value: {} {}".format(str(hat), dPadMap[0]))
			textPrint.tprint(screen, "DPAD vertical value: {} {}".format(str(hat), dPadMap[1]))
		
		textPrint.unindent()
		textPrint.unindent()
	
	# Update the screen
	pygame.display.flip()

	# Record millis passed since last call to clock.tick()
	frame_time = clock.tick()

# Screen variables
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
ACTUAL_BUTTONS_IN_USE = 10
FPS = 60.0
FRAME_EVERY_X_MILLIS = ceil(1000.0 / FPS)

# Controller variables
buttonMap = ["A", "B", "X", "Y", "LB", "RB", "BACK", "START", "LS", "RS"]
buttonValues = {buttonMap[i]:False for i in range(len(buttonMap))}
if debug: print(buttonValues)

axisMap = ["LS Left-Right", "LS Up-Down", "RS Left-Right", "RS Up-Down", "LT", "RT"]
axisValues = {axisMap[i]:0.0 if i<(len(axisMap)-2) else -1 for i in range(len(axisMap))}
if debug: print(axisValues)

dPadMap = ["right", "down"]
DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT = [0 for i in range(4)]

# Initialize pygame library, joystick module, clock, frame time tracking
pygame.init()
pygame.joystick.init()
joystick_count = 0
clock = pygame.time.Clock()
frame_time = 0

# Set the width and height of the screen as (width, height)
#	and initialize textPrint object to display text in pygame
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Controller Input")
textPrint = TextPrint()

# Actuator variables
leftDriveModeOption = [0, 1, 2, 3, 6]
leftDriveModeOptionIndex = 0
leftDriveMode = 0

rightDriveModeOption = [0, 1, 2, 3, 6]
rightDriveModeOptionIndex = 0
rightDriveMode = 0

upperExtender, lowerExtender, screwdriver, claw, hoist, swivel = [0 for i in range(6)]
leftWheel1, rightWheel1, leftWheel2, rightWheel2, leftWheel3, rightWheel3 = [0 for i in range(6)]

# Loop until the user clicks the close button
done = False

# Controller Input Loop
while not done:

	# Possible events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
	# event.type == pygame.JOYBUTTONDOWN: Joystick button pressed
	# event.type == pygame.JOYBUTTONUP: Joystick button released

	# Read events waiting since last loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # User closed the window
			done = True

		elif event.type == pygame.JOYDEVICEREMOVED: # Controller connection lost
			joystick_count = pygame.joystick.get_count()
			print("Controller disconnected!")
			print("Remaining controllers connected: {}".format(joystick_count))
			if not joystick_count:
				# Prompt user to wait or exit maybe?
				print("\t What to do?")

		elif event.type == pygame.JOYDEVICEADDED: # New controller detected
			joystick_count = pygame.joystick.get_count()

			# Wait and do nothing if no controllers detected
			if joystick_count == NULL: continue
			else: controller_num = joystick_count - 1

			joystick = pygame.joystick.Joystick(controller_num)
			joystick.init()
			name = joystick.get_name()

			try: jid = joystick.get_instance_id() # get_instance_id() is an SDL2 method
			except AttributeError: jid = joystick.get_id()

			try: guid = joystick.get_guid() # get_guid() is an SDL2 method
			except AttributeError: pass


	# Check to see if it's time to draw another frame
	frame_time += clock.tick()
	if frame_time < FRAME_EVERY_X_MILLIS: continue

	DrawFrame()

	# Send control packets over socket connection
	# print("DriveCommand_{}_{}_{}_{}_{}_{}".format(leftWheel1, rightWheel1, leftWheel2, rightWheel2, leftWheel3, rightWheel3))
	# print("ArmCommand_{}_{}_{}_{}_{}_{}".format(upperExtender, lowerExtender, screwdriver, claw, hoist, swivel))

# Close the window and quit
pygame.quit()