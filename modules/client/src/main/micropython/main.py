from microbit import display,Image,sleep, button_a
import radio

radio.config(length=251, queue=6, channel=12, group=1)
radio.on()

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


def parse_lineprotocol_message(msg):
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
                tags[tagKV[0]] = tagKV[1]
        
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

def serialize_lineprotocol_message(measurement, tags= None, values=None, timestamp=None): 
    result = measurement
    if tags is not None:
      result += (','.join('{}="{}"'.format(key, value) for key, value in tags.items())) + " "
    if values is not None:
      result += (','.join('{}={}'.format(key, value) for key, value in values.items())) + " "
    if timestamp is not None:
      result += timestamp
    else:
      result += microbit.running_time()
    return result

# uLineProtocol
############################

############################


# Create the "flash" animation frames.
full = Image("99999:99999:99999:99999:99999")

flash = [(full * (i/9)) for i in range(9, -1, -1)]

display.show(Image.TARGET)
while True:
    measurement = ""
    tags = ""
    values = ""
    timestamp = 0
    if button_a.was_pressed():
        display.show(flash, delay=50, wait=True)

    incoming = radio.receive()
    if incoming is not None:
      measurement = ""
      measurement,tags,values,timestamp = parse_lineprotocol_message(incoming)
      if measurement == 'flash':
          display.show(flash, delay=50, wait=True)
      else:
          display.show(measurement, wait=True)

    sleep(200)
    display.show(Image.TARGET)