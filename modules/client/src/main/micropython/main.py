from microbit import display,Image,sleep, button_a, button_b, running_time
from micropython import const
import radio 

SIMU = False
try:
  import machine
  DEVID = str(int.from_bytes(machine.unique_id(), "big"))
except ImportError:
  DEVID = "JOGE"
  SIMU = True
  print("Could not import machine module, DEVICE ID : "+str(DEVID))

radio.config(channel=12, group=12, length=200)
radio.on()

IMG_SEND = const([(Image.ARROW_N * (i/3)) for i in range(3, -1, -1)])

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

def usquad_send(measurement, tags= {}, timestamp=None):
  tags["dev_id"] = DEVID
  msg = ulp_serialize(measurement, tags, timestamp)
  radio.send(msg)
  if SIMU == True:
    print("Sending : "+msg)
  
def usquad_image(tags, timestamp=None):
  images_str = tags['value']
  img = [(Image(img_str)) for img_str in images_str.split(";")]
  _delay = int(tags.get('delay',50))
  _sleep = int(tags.get('sleep',2000))
  _wait = (tags.get('wait', "true").lower()=="true")
  _clear = (tags.get('clear', "true").lower()=="true")
  display.show(img, delay=_delay, wait=_wait, clear=_clear)
  sleep(_sleep)


def usquad_vote(tags, timestamp=None):
  images_str = tags['value']
  choices =  [(Image(img_str)) for img_str in images_str.split(";")]
  _max_votes = int(tags.get('votes',1))
  vote_cn = 0
  choices_max = len(choices)
  choice = 0
  button_a.get_presses()
  button_b.was_pressed()
  stop = False
  display.show(choices[choice], delay=50, clear=False,wait=True)
  while (not stop) and (vote_cn < _max_votes):
    a_presses = button_a.get_presses()
    if a_presses > 0:
      choice = (choice + a_presses) % choices_max
      display.show(choices[choice])
    if button_b.was_pressed():
      usquad_send("read_vote",{"value":choice, "index":vote_cn})
      display.show(IMG_SEND, delay=30, wait=True, clear=True)
      vote_cn += 1
      votes_left = _max_votes - vote_cn
      if(votes_left > 0):
        display.show(str(votes_left), clear=False, wait=True)
        sleep(1500)
        display.show(choices[choice], clear=False,wait=False)
    poll_messages()
    if incoming is not None and (ulp_parse(incoming)[0] in METHOD_LIST):
      stop = True
  display.show(Image.HEART)

def usquad_buttons(tags = None, timestamp=None):
  global incoming
  button_a.was_pressed()
  button_b.was_pressed()
  display.show(Image.TRIANGLE)
  stop = False
  while not stop:
    if button_a.was_pressed():
      usquad_send("read_button",{"button":"a"})
      display.show("a")
    if button_b.was_pressed():
      usquad_send("read_button",{"button":"b"})
      display.show("b")
    poll_messages()
    if incoming is not None and (ulp_parse(incoming)[0] in METHOD_LIST):
      stop = True
    else:
      sleep(250)
      display.show(Image.SQUARE_SMALL)
      
  
METHOD_MAP = const({
  'image'     : usquad_image,
  'vote'      : usquad_vote,
  'buttons'   : usquad_buttons
})
METHOD_LIST = const(METHOD_MAP.keys())
incoming = None
  

def poll_messages():
  global incoming
  if SIMU == False:
    incoming = radio.receive()
  
display.show(Image.HEART)
usquad_send("bonjour")

while True:
  meas = ""
  tags = ""
  stamp = 0
  
  poll_messages()

  while incoming is not None:
    meas,tags,stamp = ulp_parse(incoming)
    incoming = None
    execute = True
    if("dev_id" in tags.keys() and tags["dev_id"] != DEVID):
      execute = False
    method = METHOD_MAP.get(meas, None)
    if method is None:
      execute = False
    if execute:
      method(tags,stamp)
  sleep(100)