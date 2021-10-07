# def usquad_poll_messages():
#   measurement = ""
#   tags = ""
#   values = ""
#   timestamp = 0
#   incoming = None
#   if SIMULATOR == False:
#     incoming = radio.receive()
#   elif button_a.was_pressed():
#       #incoming = 'image,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999",delay=500,clear=false,wait=true'
#       #incoming = 'text,value="Show_me_the_money",clear=true,wait=true'
#       #incoming = 'accel'
#       incoming = 'vote,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999;55555:50005:00000:50005:55555",duration=4000,votes=4'

#   if incoming is not None:
#     measurement,tags,values,timestamp = ulp_parse(incoming)
#     method = usquad_methods.get(measurement, None)
#     if method is not None:
#       method(tags,values, timestamp)
#     elif SIMULATOR == True: # Debug
#       usquad_text({"value":measurement,"wait":"true"} )

# def usquad_text(tags, timestamp=None):
#   text_str = tags['value'].replace("_", " ")
#   _delay = int(tags.get('delay',50))
#   _wait = (tags.get('wait', "true").lower()=="true")
#   _clear = (tags.get('clear', "true").lower()=="true")
#   display.show(text_str, delay=_delay, wait=_wait, clear=_clear)

# def usquad_read_accel(tags= None, timestamp=None):
#   x,y,z = accelerometer.get_values()
#   usquad_send("read_accel", tags = {"x":x,"y":y,"z":z})

# def usquad_device_id(tags, timestamp=None):
#   global DEVID
#   DEVID = tags.get('id',machine.unique_id())


      #incoming = 'image,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999",delay=500,clear=false,wait=true'
      #incoming = 'text,value="Show_me_the_money",clear=true,wait=true'
      #incoming = 'accel'
      #incoming = 'vote,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999;55555:50005:00000:50005:55555",duration=4000,votes=4'


# METHOD_MAP = {
#   'image'     : usquad_image,
#   'accel'     : usquad_read_accel,
#   'text'      : usquad_text,
#   'vote'      : usquad_vote,
#   'device_id' : usquad_device_id,
#   'buttons'   : usquad_buttons
# }