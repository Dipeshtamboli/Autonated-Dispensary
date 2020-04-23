import serial
import Sliding_Windows as SWL
import pyautogui
import os
ser = serial.Serial('COM4',9600,timeout=None)
dictionary = {b'1':'crocin', b'2':'digene', b'3':'flagyl', b'4':'norflox', b'5':'wikoryl'}
size=[1687,1362] #Hardcoded in SLW, change if changed here
steps_x = 1700	#no. of steps the CNC moves over a complete traversal
steps_y = 1500
def capture():
	'''
	Basically switches the window to capture a photograph of the table
	'''
	pyautogui.hotkey('alt', 'tab')
	pyautogui.PAUSE=2.5
	pyautogui.click(x=722,y=481)
	pyautogui.PAUSE=7	
	pyautogui.click(x=910,y=754)
	pyautogui.PAUSE=3
	pyautogui.click(x=1344,y=297)

def get_string_from_coords(coords):
	x = int((coords[0][0]/size[0])*steps_x)	
	y = int((coords[0][1]/size[1])*steps_y)
	str = 'r'*(x+40) + 'u'*y + 'p' + 'l'*(x+40) + 'd'*y + 'x' 
	return str

def getName():
	#name = dictionary[ser.read()]
	print("Awaiting Input...")
	while(ser.in_waiting == 0):
		pass
	inString = ser.read(1)
	print("Input received")
	return dictionary[inString]

def moveMotors(dir):
	i = 0
	for i in range(0, len(dir)):
		ser.write(dir[i].encode())	#the string is passed one character at a time since Arduino serial buffer is only 64 bytes long
		print("Waiting for response from Arduino...")
		while (ser.in_waiting == 0):
			pass
		print("Arduino's response: ", ser.read(1))

if __name__ == "__main__":
	print("Give Input")
	name=getName()
	print("Capturing Image...")
	#capture()
	path='Picture 17.jpg'	#Fix path here
	print("Extracting coordinates")
	coords = SWL.main(path,name)
	print(coords)
	# os.remove(path)
	dir = get_string_from_coords(coords)
	print("Moving Arm")
	moveMotors(dir)
