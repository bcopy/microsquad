from microbit import display,Image,sleep, button_a, button_b, accelerometer, running_time

import radio 
import random

SIMULATOR = False
try:
  import machine
  DEVICE_ID = machine.unique_id()
except ImportError:
  DEVICE_ID = random.getrandbits(32)
  SIMULATOR = True
  print("Could not import machine module, DEVICE ID : "+str(DEVICE_ID))

radio.config(length=251, queue=6, channel=12, group=1)
radio.on()



# Create the "flash" animation frames.
IMG_FLASH = [(Image("99999:99999:99999:99999:99999") * (i/9)) for i in range(9, -1, -1)]

############################
#  uLineProtocol

# Very simple and probably buggy line protocol parser
# Do not reuse !

def _pop_head_or_none(arr, peek_only = False):
    if arr and len(arr)>0:
        if peek_only:
          return arr[0]
        else:
          return arr.pop(0)
    else:
        return None


def ulp_parse(msg):
    measurement = None
    tags = {}
    values = {}
    timestamp = None

    fragments = msg.split(" ")
    fragment = _pop_head_or_none(fragments)
    if fragment is not None:
        measurementFragments = fragment.split(",")
        if len(measurementFragments) > 0:
            measurement = measurementFragments[0]
        if  len(measurementFragments) > 1:
            for tagFragment in measurementFragments[1:]:
                tagKV = tagFragment.split("=")
                tags[tagKV[0]] = tagKV[1].strip('"\'') # Strip any trailing / leading characters
        
    fragment = _pop_head_or_none(fragments,True)
    if fragment is not None:
        if("=" in fragment):
            fragment = _pop_head_or_none(fragments)
            valuesFragment = fragment.split(",")
            for valueFragment in map(lambda v: v.split("="),valuesFragment):
                values[valueFragment[0]] = valueFragment[1]

    fragment = _pop_head_or_none(fragments)
    if fragment is not None:
        timestamp = int(fragment)
        
    return (measurement, tags, values, timestamp)

def ulp_serialize(measurement, tags=None, values=None, timestamp=None): 
    result = measurement
    if tags is not None:
      result += (','.join('{}="{}"'.format(key, value) for key, value in tags.items())) + " "
    if values is not None:
      result += (','.join('{}={}'.format(key, value) for key, value in values.items())) + " "
    if timestamp is not None:
      result += timestamp
    else:
      result += str(running_time())
    return result


# uLineProtocol
############################

def usquad_send(measurement, tags= None, values=None, timestamp=None):
  """
     Broadcast the given line protocol message, tagged with the microbit's unique ID
  """
  tagz = {"dev_id":DEVICE_ID}
  if tags is not None:
    tagz.update(tags)
  msg = ulp_serialize(measurement, tagz, values, timestamp)
  radio.send(msg)
  if SIMULATOR == True:
    print("Sending : "+msg)
  
#######
# uSquad protocol methods
###

def usquad_flash(tags= None, values=None, timestamp=None):
  """
     Displays a quick flashing animation
  """
  display.show(IMG_FLASH, delay=50, wait=True)


def usquad_image(tags, values=None, timestamp=None):
  """
     Displays the given list of images from a string representation.
     Image lines are separated by ':' while images
     are separated by ';'
  """
  images_str = tags['value']
  img = [(Image(img_str)) for img_str in images_str.split(";")]
  _delay = int(tags.get('delay',50))
  _wait = (tags.get('wait', "true").lower()=="true")
  _clear = (tags.get('clear', "true").lower()=="true")
  display.show(img, delay=_delay, wait=_wait, clear=_clear)

def usquad_text(tags, values=None, timestamp=None):
  """ 
    Displays text on the screen (tag "value")
  """
  text_str = tags['value'].replace("_", " ")
  _delay = int(tags.get('delay',50))
  _wait = (tags.get('wait', "true").lower()=="true")
  _clear = (tags.get('clear', "true").lower()=="true")
  display.show(text_str, delay=_delay, wait=_wait, clear=_clear)

def usquad_read_accel(tags= None, values=None, timestamp=None):
  """
     Requests an accelerometer reading via radio
  """
  x,y,z = accelerometer.get_values()
  usquad_send("read_accel", values = {"x":x,"y":y,"z":z})

def usquad_device_id(tags, values=None, timestamp=None):
  """
     Set a new Device ID on that device.
  """
  DEVICE_ID = tags.get('id',machine.unique_id())

############################



usquad_methods = {
  'flash'     : usquad_flash,
  'image'     : usquad_image,
  'accel'     : usquad_read_accel,
  'text'      : usquad_text,
  'device_id' : usquad_device_id
}


################################
# Main Method
################################

# Report to the gateway
display.show(Image.TARGET)
usquad_send("bonjour")

while True:
    measurement = ""
    tags = ""
    values = ""
    timestamp = 0
    incoming = None
    if SIMULATOR == False:
      incoming = radio.receive()
    elif button_a.was_pressed():
        #incoming = 'image,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999",delay=500,clear=false,wait=true'
        #incoming = 'text,value="Show_me_the_money",clear=true,wait=true'
        incoming = 'accel'

    if incoming is not None:
      measurement = ""
      measurement,tags,values,timestamp = ulp_parse(incoming)
      method = usquad_methods.get(measurement, None)
      if method is not None:
        method(tags,values, timestamp)
      else:
        usquad_text({"value":measurement,"wait":"true"} )

    sleep(200)
    #display.show(Image.TARGET)