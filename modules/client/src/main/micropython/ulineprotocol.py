def _pop_head_or_none(arr, peek_only = False):
    if arr and len(arr)>0:
        if peek_only:
          return arr[0]
        else:
          return arr.pop(0)
    else:
        return None


def ulp_parse(msg):
    meas = None
    tags = {}
    fields = {}
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
    frag = _pop_head_or_none(frags,True)
    if frag is not None:
        if("=" in frag):
            frag = _pop_head_or_none(frags)
            fieldsFragment = frag.split(",")
            for fieldFragment in map(lambda v: v.split("="),fieldsFragment):
                fields[fieldFragment[0]] = fieldFragment[1]
    frag = _pop_head_or_none(frags)
    if frag is not None:
        tmstp = int(frag)
    return (meas, tags, fields, tmstp)

def ulp_serialize(measurement, tags=None, fields=None, timestamp=None): 
    result = measurement
    if tags is not None:
      result += (','.join('{}="{}"'.format(key, value) for key, value in tags.items())) + " "
    if fields is not None:
      result += (','.join('{}={}'.format(key, value) for key, value in fields.items())) + " "
    if timestamp is not None:
      result += timestamp
    else:
      result += str(running_time())
    return result