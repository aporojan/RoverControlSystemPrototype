/*

Requirements:
	exclude Serial library from final product
	use Servo.h library to control the motors
	board IP address starts with 192.168.1
	??designate LED pins on the Arduino file responsible for handling the drive commands??
	??control the LEDs on the rover on the Arduino file responsible for handling the drive commands??

DRIVE PINS
	leftWheel1 11 
	leftWheel2 12 
	leftWheel3 24 
	rightWheel1 25 
	rightWheel2 28 
	rightWheel3 29 
	LEDRedValue 33
	LEDBlueValue 34
	LEDGreenValue 35

ARM PINS
	upperExtender 24
	lowerExtender 29
	hoist 25
	screwdriver 11
	claw 28
	swivel 12

*above notes duplicated in firmware_Arm.ino
*/

// #include <NativeEthernet.h>
// #include <NativeEthernetTcp.h>
#include <Servo.h>

const byte leftWheel1 = 11, leftWheel2 = 12, leftWheel3 = 24, 
			rightWheel1 = 25, rightWheel2 = 28, rightWheel3 = 29, 
			LEDRedValue = 33, LEDBlueValue = 34, LEDGreenValue = 35;

const byte upperExtender = 24, lowerExtender = 29, hoist = 25,
			screwdriver = 11, claw = 28, swivel = 12;

const uint16_t port = 8090;
const char * host = "192.168.1.83";

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}