import serial

class HardwareControl:

	Data = 0
	angle = 0

	def __init__( self ):
	
		self.Data = 0
		self.arduino = serial.Serial('/dev/ttyACM0', 9600,serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)	
       
 	def  write(self):
          try:       		
		self.arduino.write(chr(self.Data))
		self.arduino.flushOutput()		
	  except:	       
	       print "Error In Write"	

 	def  read(self):
          try:  
		
		#self.arduino.flushInput()
		while self.arduino.inWaiting() == 0 :
			print "waiting"     		
		currentAngle=self.arduino.readline()
		self.arduino.flushInput()
				
	  except:	       
	       print "Error In Read"	
	  return currentAngle
 
	
	def serialOn(self) :
		self.Data = 16	
		self.write()

	def serialOff(self):
		self.Data = 0
		self.write()

	def serialOn1(self) :
		self.Data = 32	
		self.write()

	def serialOff1(self):
		self.Data = 0
		self.write()	
	
	def setAngle(self):
		self.Data |=4
		#self.write()
		#self.writeAngle()
		#self.resetAngle()
		#self.write()

	def resetAngle(self):
		self.Data &=123

	def writeAngle(self):	
		
		try:       		
			self.arduino.write(chr(self.angle))
			self.arduino.flushOutput()		
	 	except:	       
	       		print "Error In Write1"	

	def getAngle(self)	:		
		
		self.Data |=8
		self.write()
		angle = self.read()
		#print "swap"
		self.Data&=119
		self.write()
		return angle
	

	def forward(self):
		self.Data |=1
		
	def forwardStop(self):
		self.Data&=126
		
	def reverse(self):
		self.Data|=2
		
	def reverseStop(self):
		self.Data&=125


