
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

Socket library example code:
	


"""

from math import ceil
import pygame
import socket

# Define constants
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
ACTUAL_BUTTONS_IN_USE = 10
FPS = 60.0
FRAME_EVERY_X_MILLIS = ceil(1000.0 / FPS)
buttonMap = ["A", "B", "X", "Y", "LB", "RB", "BACK", "START", "LS", "RS"]
axisMap = ["LS Left-Right", "LS Up-Down", "RS Left-Right", "RS Up-Down", "LT", "RT"]
dPadMap = ["right", "down"]

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

# Initialize pygame library and controllers
pygame.init()
pygame.joystick.init()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
frame_time = 0

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Controller Input")

# Initialize textPrint object to display text in pygame
textPrint = TextPrint()

# Loop until the user clicks the close button.
done = False

# Controller Input Loop
while not done:

	# Possible events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # User closed the window
			done = True
		elif event.type == pygame.JOYDEVICEREMOVED: # Controller connection lost
			joystick_count = pygame.joystick.get_count()
			print("Controller disconnected!\nRemaining controllers connected: %d"\
				%joystick_count)
			if not joystick_count:
				# Prompt user to continue or exit maybe?
				done = True
				continue
		# event.type == pygame.JOYBUTTONDOWN: Joystick button pressed
		# event.type == pygame.JOYBUTTONUP: Joystick button released

	# Check to see if it's time to draw another frame
	frame_time += clock.tick()
	if frame_time < FRAME_EVERY_X_MILLIS:
		continue
 
	# START DRAWING
	frame_time = 0
	screen.fill(WHITE)
	textPrint.reset()

	# Get count of joysticks
	joystick_count = pygame.joystick.get_count()

	textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
	textPrint.indent()

	# For each joystick:
	for controller_num in range(joystick_count):
		joystick = pygame.joystick.Joystick(controller_num)
		joystick.init()

		try:
			jid = joystick.get_instance_id()
		except AttributeError:
			# get_instance_id() is an SDL2 method
			jid = joystick.get_id()
		textPrint.tprint(screen, "Joystick {}".format(jid))
		textPrint.indent()

		# Get the name from the OS for the controller
		name = joystick.get_name()
		textPrint.tprint(screen, "Joystick name: {}".format(name))

		try:
			guid = joystick.get_guid()
		except AttributeError:
			# get_guid() is an SDL2 method
			pass
		else:
			textPrint.tprint(screen, "GUID: {}".format(guid))

		# Check axis movement
		axes = joystick.get_numaxes()
		textPrint.tprint(screen, "Number of axes: {}".format(axes))
		textPrint.indent()

		for i in range(axes):
			axis = joystick.get_axis(i)
			textPrint.tprint(screen, "{} value: {:>6.3f}".format(axisMap[i], axis))
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

	# STOP DRAWING
	# Update the screen
	pygame.display.flip()
 
	# Record millis passed since last call to clock.tick()
	frame_time = clock.tick()

# Close the window and quit.
pygame.quit()