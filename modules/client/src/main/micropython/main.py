from microbit import display,Image,sleep, button_a, button_b, running_time
from micropython import const
import radio 

SIMU = False
import machine

DEVID = const(str(int.from_bytes(machine.unique_id(), "big")))

radio.config(channel=12, group=12, length=128)
radio.on()

# IMG_SEND = const([(Image.ARROW_N * (i/2)) for i in range(2, -1, -1)])
IMG_SEND = Image.ARROW_N

PROTON_DISPLAY =   const("09990:99399:99999:99990:99000")
ELECTRON_DISPLAY = const("90009:09090:00000:99999:90909")
PHOTON_DISPLAY =   const("90900:90900:99990:99399:99999")
NEUTRON_DISPLAY =  const("09900:99390:99999:00099:99990")

def _pop_or_none(arr):
    if arr and len(arr)>0:
      return arr.pop(0)
    else:
      return None

def ulp_parse(msg):
    meas = None
    tags = {}
    tmstp = None

    frags = msg.split(" ")
    frag = _pop_or_none(frags)
    if frag is not None:
        measFrags = frag.split(",")
        if len(measFrags) > 0:
            meas = measFrags[0]
        if  len(measFrags) > 1:
            for tagFrag in measFrags[1:]:
                tagKV = tagFrag.split("=")
                tags[tagKV[0]] = tagKV[1].strip('"\'')
    frag = _pop_or_none(frags)
    if frag is not None:
        tmstp = int(frag)
    return (meas, tags, tmstp)

def ulp_serialize(measurement, tags=None, timestamp=None): 
    result = measurement
    if tags is not None:
      for key, value in tags.items():
        result += ','+str(key)+"=\""+str(value)+"\""
    # if timestamp is not None:
    #   result += " "+str(timestamp)
    # else:
    #   result += " "+str(running_time())
    return result

def usquad_send(measurement, tags= {}, timestamp=None):
  tags["dev_id"] = DEVID
  msg = ulp_serialize(measurement, tags, timestamp)
  radio.send(msg)
  
def usquad_image(tags, timestamp=None):
  images_str = tags['value']
  img = [(Image(img_str)) for img_str in images_str.split(";")]
  _del = int(tags.get('delay',1000))
  _slp = int(tags.get('sleep',2000))
  _wait = (tags.get('wait', "true").lower()=="true")
  _clr = (tags.get('clear', "false").lower()=="true")
  display.show(img, delay=_del, wait=_wait, clear=_clr)
  sleep(_slp)

def usquad_vote_particles(tags, timestamp = None):
  usquad_vote({
    "value" : (PROTON_DISPLAY+";"+ELECTRON_DISPLAY+";"+PHOTON_DISPLAY+";"+NEUTRON_DISPLAY),
    "votes" : "1"
  })

def usquad_vote(tags, timestamp=None):
  global incoming,METHOD_LIST
  images_str = tags['value']
  choices =  [(Image(img_str)) for img_str in images_str.split(";")]
  _max_votes = int(tags.get('votes',1))
  vote_cn = 0
  choices_max = len(choices)
  choice = 0
  button_a.get_presses()
  button_b.was_pressed()
  stopVote = False
  display.show(choices[choice], delay=50, clear=False,wait=True)
  while (not stopVote) and (vote_cn < _max_votes):
    a_presses = button_a.get_presses()
    if a_presses > 0:
      choice = (choice + a_presses) % choices_max
      display.show(choices[choice])
    if button_b.was_pressed():
      usquad_send("read_vote",{"value":choice, "index":vote_cn})
      display.show(IMG_SEND, wait=True, clear=False)
      sleep(300)
      vote_cn += 1
      votes_left = _max_votes - vote_cn
      if(votes_left > 0):
        display.show(str(votes_left), clear=False, wait=True)
        sleep(100)
        display.show(choices[choice], clear=False,wait=False)
    poll_messages()
    if incoming is not None and (not(incoming.startswith("read_") or incoming.startswith("bonjour"))) and (ulp_parse(incoming)[0] in METHOD_LIST):
      stopVote = True # keep incoming
  display.show(Image.YES)

def usquad_buttons(tags = None, timestamp=None):
  global incoming,METHOD_LIST
  button_a.was_pressed()
  button_b.was_pressed()
  display.show(Image.TRIANGLE)
  stopBtn = False
  while not stopBtn:
    if button_a.was_pressed():
      usquad_send("read_button",{"button":"a"})
      display.show("a")
    if button_b.was_pressed():
      usquad_send("read_button",{"button":"b"})
      display.show("b")
    poll_messages()
    if incoming is not None and (not(incoming.startswith("read_") or incoming == "bonjour")) and (ulp_parse(incoming)[0] in METHOD_LIST):
      stopBtn = True # keep incoming
    else:
      sleep(250)
      display.show(Image.SQUARE_SMALL)
      
  
METHOD_MAP = const({
  'image'          : usquad_image,
  # 'vote'           : usquad_vote,
  'buttons'        : usquad_buttons,
  'vote_particles' : usquad_vote_particles
})
METHOD_LIST = const(METHOD_MAP.keys())
incoming = None

def poll_messages():
  global incoming
  incoming = radio.receive()
  

# START AND MAIN LOOP
display.show(Image.HEART)
usquad_send("bonjour")

while True:
  meas = ""
  tags = ""
  stamp = 0
  
  poll_messages()

  while incoming is not None:
    if incoming.startswith("read_") or incoming.startswith("bonjour"):
      incoming = None # skip the message, it comes from another terminal
    else:
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