from microbit import display,Image,sleep, button_a, button_b, accelerometer, running_time


import radio 

SIMU = False
try:
  import machine
  DEVID = machine.unique_id()
except ImportError:
  DEVID = "123456789123456789"
  SIMU = True
  print("Could not import machine module, DEVICE ID : "+str(DEVID))

radio.config(channel=12, group=1, length=128)
radio.on()

IMG_SEND = [(Image.ARROW_N * (i/3)) for i in range(3, -1, -1)]

def _pop_head_or_none(arr):
    if arr and len(arr)>0:
      return arr.pop(0)
    else:
      return None

def ulp_parse(msg):
    meas = None
    tags = {}
    tmstp = None

    frags = msg.split(" ")
    frag = _pop_head_or_none(frags)
    if frag is not None:
        measFrags = frag.split(",")
        if len(measFrags) > 0:
            meas = measFrags[0]
        if  len(measFrags) > 1:
            for tagFrag in measFrags[1:]:
                tagKV = tagFrag.split("=")
                tags[tagKV[0]] = tagKV[1].strip('"\'')
    frag = _pop_head_or_none(frags)
    if frag is not None:
        tmstp = int(frag)
    return (meas, tags, tmstp)

def ulp_serialize(measurement, tags=None, timestamp=None): 
    result = measurement
    if tags is not None:
      for key, value in tags.items():
        result += ','+str(key)+"=\""+str(value)+"\""
    if timestamp is not None:
      result += " "+str(timestamp)
    else:
      result += " "+str(running_time())
    return result

def usquad_send(measurement, tags= None, timestamp=None):
  tagz = {"dev_id":DEVID}
  if tags is not None:
    tagz.update(tags)
  msg = ulp_serialize(measurement, tagz, timestamp)
  radio.send(msg)
  if SIMU == True:
    print("Sending : "+msg)
  
def usquad_image(tags, timestamp=None):
  images_str = tags['value']
  img = [(Image(img_str)) for img_str in images_str.split(";")]
  _delay = int(tags.get('delay',1000))
  _wait = (tags.get('wait', "true").lower()=="true")
  _clear = (tags.get('clear', "true").lower()=="true")
  display.show(img, delay=_delay, wait=_wait, clear=_clear)

def usquad_text(tags, timestamp=None):
  text_str = tags['value'].replace("_", " ")
  _delay = int(tags.get('delay',1000))
  _wait = (tags.get('wait', "true").lower()=="true")
  _clear = (tags.get('clear', "true").lower()=="true")
  display.show(text_str, delay=_delay, wait=_wait, clear=_clear)

def usquad_read_accel(tags= None, timestamp=None):
  x,y,z = accelerometer.get_values()
  usquad_send("read_accel", tags = {"x":x,"y":y,"z":z})

def usquad_device_id(tags, timestamp=None):
  global DEVID
  DEVID = tags.get('id',machine.unique_id())

def usquad_vote(tags, timestamp=None):
  images_str = tags['value']
  choices =  [(Image(img_str)) for img_str in images_str.split(";")]
  _max_votes = int(tags.get('votes',1))
  vote_cn = 0
  choices_max = len(choices)
  choice = 0
  button_a.get_presses()
  button_b.was_pressed()
  display.show(choices[choice], delay=50, clear=False,wait=True)
  while (vote_cn < _max_votes):
    a_presses = button_a.get_presses()
    if a_presses > 0:
      choice = (choice + a_presses) % choices_max
      display.show(choices[choice])
    if button_b.was_pressed():
      usquad_send("read_vote",{"value":choice, "index":vote_cn})
      display.show(IMG_SEND, delay=50, wait=True, clear=True)
      vote_cn += 1
      votes_left = _max_votes - vote_cn
      if(votes_left > 0):
        display.show(str(votes_left), clear=False, wait=True)
        sleep(1500)
        button_b.was_pressed()
        display.show(choices[choice], clear=False,wait=False)
  display.show(Image.TARGET)
  
usquad_methods = {
  'image'     : usquad_image,
  'accel'     : usquad_read_accel,
  'text'      : usquad_text,
  'vote'      : usquad_vote,
  'device_id' : usquad_device_id,
  #'buttons'   : usquad_buttons
}
incoming = None
  

def poll_messages():
  global incoming
  if SIMU == False:
    incoming = radio.receive()
  if button_a.was_pressed():
    incoming = 'vote,value=90009:09090:00900:09090:90009;00900:09090:90009:09090:00900;55555:50005:50005:50005:55555,duration=4000,votes=4'
    #incoming = 'buttons'
  
display.show(Image.TARGET)
usquad_send("bonjour")

while True:
  meas = ""
  tags = ""
  stamp = 0
  
  poll_messages()

  while incoming is not None:
    meas,tags,stamp = ulp_parse(incoming)
    incoming = None
    method = usquad_methods.get(meas, None)
    if method is not None:
      method(tags,stamp)

  sleep(200)