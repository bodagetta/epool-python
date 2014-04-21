#!/usr/bin/env python
import serial
import httplib2, urllib
import time

global parseWSNDemoData 
def parseWSNDemoData(buf): 
  import struct 
  def get(d): 
    d.reverse() 
    res = 0L 
    for i in d: 
      res = (res << 8) | i 
    return res 

  res = {} 
  res['messageType']     = buf[0] 
  res['nodeType']        = buf[1] 
  res['extAddr']         = get(buf[2:9]) 
  res['shortAddr']       = get(buf[10:11]) 
  res['softVersion']     = get(buf[12:15]) 
  res['channelMask']     = get(buf[16:19]) 
  res['panID']           = get(buf[20:21]) 
  res['workingChannel']  = buf[22] 
  res['parentShortAddr'] = get(buf[23:24]) 
  res['lqi']             = buf[25] 
  res['rssi']            = struct.unpack('b', chr(buf[26]))[0] 
  res['boardType']       = buf[27] 
  res['sensorsSize']     = buf[28] 
  res['battery']         = get(buf[29:32]) 
  res['temperature']     = get(buf[33:36]) 
  res['light']           = get(buf[37:38]) 
  res['ph'] 		 = get(buf[37:39])
  res['orp']		 = get(buf[41:43])
  return res 

# WSNDemo protocol state machine. Must be caled on every received byte. 
# If correct (length and check summ) frame received data (decoded) 
# returned, otherwise Null returned. 
global smState, fullData, dataBuffer 
smState = 0 
def WSNDemoProtocolSM(c): 
  global smState, fullData, dataBuffer 
  IDLE_STATE       = 0 
  IDLE_CMD_STATE   = 1 
  RCV_STATE        = 2 
  RCV_CMD_STATE    = 3 
  RCV_CSUMM_STATE  = 4 

  if smState == IDLE_STATE: 
    fullData = [] 
    dataBuffer = [] 

  fullData += [c] 

  if smState == IDLE_STATE: 
    if c == 0x10: 
      smState = IDLE_CMD_STATE 

  elif smState == IDLE_CMD_STATE: 
    if c == 0x02: 
      smState = RCV_STATE 
    else: 
      smState = IDLE_STATE 

  elif smState == RCV_STATE: 
    if c == 0x10: 
      smState = RCV_CMD_STATE 
    else: 
      if len(dataBuffer) == 57: 
        smState = IDLE_STATE 
      else: 
        dataBuffer += [c] 

  elif smState == RCV_CMD_STATE: 
    if c == 0x10: 
      dataBuffer += [c] 
      smState = RCV_STATE 
    elif c == 0x03: 
      smState = RCV_CSUMM_STATE 
    else: 
      smState = IDLE_CMD_STATE 

  elif smState == RCV_CSUMM_STATE: 
    smState = IDLE_STATE; 

    if (len(dataBuffer) == 57) and (c == ((sum(fullData)-c) & 0xff)):
	print dataBuffer
        return parseWSNDemoData(dataBuffer) 

  return None 


def sendData(frame):

	params = urllib.urlencode({'point[boardType]': frame['boardType'],
		'point[shortAddr]': frame['shortAddr'],
		'point[extAddr]': frame['extAddr'],
		'point[nodeType]': frame['nodeType'],
		'point[temperature]': frame['temperature'],
		'point[softVersion]': frame['softVersion'],
		'point[battery]': frame['battery'],
		'point[light]': frame['light'],
		'point[messageType]': frame['messageType'],
		'point[workingChannel]': frame['workingChannel'],
		'point[sensorsSize]': frame['sensorsSize'],
		'point[lqi]': frame['lqi'],
		'point[rssi]': frame['rssi'],
		'point[parentShortAddr]': frame['parentShortAddr'],
		'point[panID]': frame['panID'],
		'point[channelMask]': frame['channelMask'],
		'point[ph]' : frame['ph'],
		'point[orp]' : frame['orp']
		})
	headers = {}
	h = httplib2.Http()
        resp, content = h.request("http://www.poollog.net/points", "POST", params, headers)
	#conn.request("POST", "/points", params, headers)
	#response = conn.getresponse()
	#print response.status, response.reason
	#data = response.read()
	#print data
        print resp


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

while 1==1:
    readValue = ser.read()
    #print readValue.encode('hex'),
    frame = WSNDemoProtocolSM(int(readValue.encode('hex'), 16))
    #print len(dataBuffer)  
    #print smState
    #print readValue.encode('hex')
    #if int(readValue.encode('hex'), 16) == 0x10:
    #	print "GOT 0x10"
    if frame != None:
	print time.strftime("%c")
        print frame
        if(frame['shortAddr'] != 0):
            sendData(frame)
        #sendData()
