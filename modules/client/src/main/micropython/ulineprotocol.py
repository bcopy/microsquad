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
    vals = {}
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
            valuesFragment = frag.split(",")
            for valueFragment in map(lambda v: v.split("="),valuesFragment):
                vals[valueFragment[0]] = valueFragment[1]
    frag = _pop_head_or_none(frags)
    if frag is not None:
        tmstp = int(frag)
    return (meas, tags, vals, tmstp)

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