import time

def _pop_head_or_none(arr, peek_only = False):
    """
    Simple static utility function that can pop or peek the head of an array list
    and return None if it is empty
    """
    if arr and len(arr)>0:
        if peek_only:
            return arr[0]
        else:
            return arr.pop(0)
    else:
        return None
            
class LineProtocolParser:
    """ 
    A simple, homemade, self-contained Line protocol parser.
    The parser tolerates even non-standard line protocol messages (e.g. missing fields).
    It does not strictly implement the line protocol standard. Use at your own risks.
    """
    def parse(self,msg):
        measure = None
        tags = {}
        fields = {}
        timestamp = None

        frags = msg.split(" ")
        frag = _pop_head_or_none(frags)
        if frag is not None:
            measFrags = frag.split(",")
            if len(measFrags) > 0:
                measure = measFrags[0]
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
                    fields[fieldFragment[0]] = float(fieldFragment[1])
        frag = _pop_head_or_none(frags)
        if frag is not None:
            timestamp = int(frag)
        return (measure, tags, fields, timestamp)

    def serialize(self,measurement, tags=None, fields=None, timestamp=None): 
        result : str = measurement
        if tags is not None:
          result += (','.join('{}="{}"'.format(key, value) for key, value in tags.items())) + " "
        if fields is not None:
          result += (','.join('{}={}'.format(key, value) for key, value in fields.items())) + " "
        if timestamp is not None:
          result += timestamp
        else:
          result += str(time.time_ns())
        return result