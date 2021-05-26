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



      #incoming = 'image,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999",delay=500,clear=false,wait=true'
      #incoming = 'text,value="Show_me_the_money",clear=true,wait=true'
      #incoming = 'accel'
      #incoming = 'vote,value="99999:99999:99099:99999:99999;99999:55555:55055:55555:99999;55555:50005:00000:50005:55555",duration=4000,votes=4'


def usquad_buttons(tags = None, timestamp=None):
  global incoming
  button_a.was_pressed()
  button_b.was_pressed()
  display.show(Image.TRIANGLE)
  stop = False
  while not stop:
    if button_a.was_pressed():
      usquad_send("read_button",{"value":"a"})
      display.show("a")
    if button_b.was_pressed():
      usquad_send("read_button",{"value":"b"})
      display.show("b")
    poll_messages()
    if incoming is not None:
      stop = True
    else:
      sleep(200)
      display.show(Image.TRIANGLE)
      

