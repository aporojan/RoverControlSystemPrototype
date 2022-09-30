
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

Pygame library XBOX example code:
	https://www.pygame.org/docs/ref/XBOX.html#module-pygame.XBOX

Socket library example code:

"""
import socket
from math import ceil
import pygame
import pygame._sdl2
from pygame._sdl2.controller import Controller


# Define constants
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
ACTUAL_BUTTONS_IN_USE = 10
FPS = 60.0
FRAME_EVERY_X_MILLIS = ceil(1000.0 / FPS)

pygame.init()
pygame._sdl2.controller.init()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
frame_time = 0

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

def CtrlRead(controller_num):
	global textPrint, pygame

	XBOX = pygame._sdl2.controller.Controller(controller_num)
	XBOX.init()

	try:
		ctrl_ID = XBOX.get_instance_id()
	except AttributeError:
		# get_id() is a pygame.Joystick method
		ctrl_ID = XBOX.get_init()
	textPrint.tprint(screen, "Controller {}".format(ctrl_ID))
	textPrint.indent()

	# Get the name from the OS for the controller
	#	get_name() is a pygame.Joystick method
	name = pygame._sdl2.controller.name_forindex(ctrl_num)
	textPrint.tprint(screen, "Controller name: {}".format(name))

	try:
		guid = XBOX.get_guid()
	except AttributeError:
		# get_guid() is an SDL2 method
		pass
	else:
		textPrint.tprint(screen, "GUID: {}".format(guid))

	# Check axis movement
	axes = XBOX.get_numaxes()
	textPrint.tprint(screen, "Number of axes: {}".format(axes))
	textPrint.indent()

	for i in range(axes):
		axis = XBOX.get_axis(i)
		textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
	textPrint.unindent()

	# Check button press/release
	buttons = XBOX.get_numbuttons()
	textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
	textPrint.indent()

	for i in range(ACTUAL_BUTTONS_IN_USE):
		button = XBOX.get_button(i)
		textPrint.tprint(screen, "Button {:>2} value: {}".format(i, button))
	textPrint.unindent()

	# Check D-pad button press/release
	hats = XBOX.get_numhats()
	textPrint.tprint(screen, "Number of hats: {}".format(hats))
	textPrint.indent()

	# Hat position is a tuple of int values (x, y)
	for i in range(hats):
		hat = XBOX.get_hat(i)
		textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Controller Input")

# Initialize textPrint object to display text in pygame
textPrint = TextPrint()

# Loop until the user clicks the close button.
done = False

# Controller Input Loop
while not done:

	# Possible events: CONTROLLERAXISMOTION, CONTROLLERBUTTONDOWN, CONTROLLERBUTTONUP,
	# 		CONTROLLERDEVICEREMAPPED, CONTROLLERDEVICEADDED, CONTROLLERDEVICEREMOVED
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # User closed the window
			done = True
		elif event.type == pygame.CONTROLLERDEVICEREMOVED: # Controller connection lost
			ctrl_count = pygame._sdl2.controller.get_count()
			print("Controller disconnected!\nRemaining controllers connected: %d"\
				%ctrl_count)
			if not ctrl_count:
				# Prompt user to continue or exit maybe?
				done = True
				continue
		# event.type == pygame.JOYBUTTONDOWN: Controller button pressed
		# event.type == pygame.JOYBUTTONUP: Controller button released

	# Check to see if it's time to draw another frame
	frame_time += clock.tick()
	if frame_time < FRAME_EVERY_X_MILLIS:
		continue
 
	# START DRAWING
	frame_time = 0
	screen.fill(WHITE)
	textPrint.reset()

	# Get count of controllers
	ctrl_count = pygame._sdl2.controller.get_count()

	textPrint.tprint(screen, "Number of controllers: {}".format(ctrl_count))
	textPrint.indent()

	# For each detected controller:
	for ctrl_num in range(ctrl_count):
		XBOX = pygame._sdl2.controller.Controller(ctrl_num)
		XBOX.init()
		print(XBOX.get_mapping())

		try:
			ctrl_ID = XBOX.get_instance_id()
		except AttributeError:
			# get_id() is a pygame.Joystick method
			ctrl_ID = XBOX.get_init()
		textPrint.tprint(screen, "Controller {}".format(ctrl_ID))
		textPrint.indent()

		# Get the controller name
  		# 	get_name() is a pygame.Joystick method
		name = pygame._sdl2.controller.name_forindex(ctrl_num)
		textPrint.tprint(screen, "Controller name: {}".format(name))

		try:
			guid = XBOX.get_guid()
		except AttributeError:
			# get_guid() is an SDL2 method
			pass
		else:
			textPrint.tprint(screen, "GUID: {}".format(guid))

		# Check axis movement
		axes = XBOX.get_numaxes()
		textPrint.tprint(screen, "Number of axes: {}".format(axes))
		textPrint.indent()

		for i in range(axes):
			axis = XBOX.get_axis(i)
			textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
		textPrint.unindent()

		# Check button press/release
		buttons = XBOX.get_numbuttons()
		textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
		textPrint.indent()

		for i in range(ACTUAL_BUTTONS_IN_USE):
			button = XBOX.get_button(i)
			textPrint.tprint(screen, "Button {:>2} value: {}".format(i, button))
		textPrint.unindent()

		# Check D-pad button press/release
		hats = XBOX.get_numhats()
		textPrint.tprint(screen, "Number of hats: {}".format(hats))
		textPrint.indent()

		# Hat position is a tuple of int values (x, y)
		for i in range(hats):
			hat = XBOX.get_hat(i)
			textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
		textPrint.unindent()
		textPrint.unindent()

	# STOP DRAWING
	# Update the screen
	pygame.display.flip()
 
	# Record millis passed since last call to clock.tick()
	frame_time = clock.tick()

# Close the window and quit.
pygame.quit()
