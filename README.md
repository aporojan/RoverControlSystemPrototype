# RoverControlSystemPrototype

To control the rover, the Python script takes controller input and displays it on screen using the pygame library, then sends motor control values via TCP connections (work in progress) using the socket library to two Arduinos.

The Arduinos connect to the Python script using a TCP library (work in progress) and drive servo motors (work in progress).
