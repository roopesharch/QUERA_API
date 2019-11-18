import json
import _ctypes
import re

class OneDictPerLine(object):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        if not isinstance(self.value, list):
            return repr(self.value)
        else:  # Sort the representation of any dicts in the list.
            reps = ('{{{}}}'.format(', '.join(
                        ('{!r}: {}'.format(k, v) for k, v in sorted(v.items()))
                    )) if isinstance(v, dict)
                        else
                    repr(v) for v in self.value)
            return '[' + ',\n'.join(reps) + ']'


def di(obj_id):
    """ Reverse of id() function. """
    # from https://stackoverflow.com/a/15012814/355230
    return _ctypes.PyObj_FromPtr(obj_id)


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = "@@{}@@"
    regex = re.compile(FORMAT_SPEC.format(r"(\d+)"))

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, OneDictPerLine)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON repr.

        # Replace any marked-up object ids in the JSON repr with the value
        # returned from the repr() of the corresponding Python object.
        for match in self.regex.finditer(json_repr):
            id = int(match.group(1))
            # Replace marked-up id with actual Python object repr().
            json_repr = json_repr.replace(
                       '"{}"'.format(format_spec.format(id)), repr(di(id)))

        return json_repr


inline={}
m="make it"
inline[m] = {'first_name': "John","isAlive": True,"age": 27,"address": {
"streetAddress": "21 2nd Street",
"city": "New York",
"state": "NY",
"postalCode": "10021-3100"
},
"hasMortgage": None
}

rat=json.dumps(OneDictPerLine(inline), cls=MyEncoder)
# with open('inline.json', 'a') as f:  # writing JSON object
#     json.dump(rat+'\n', f)

with open("inline.json",'a') as file:
    rat = json.dumps(inline[m])
    file.write(rat+'\n')

# open('inline.json', 'r').read()   # reading JSON object as string
# '{"hasMortgage": null, "isAlive": true, "age": 27, "address": {"state": "NY", "streetAddress": "21 2nd Street", "city": "New York", "postalCode": "10021-3100"}, "first_name": "John"}'


# type(open('inline.json', 'r').read())   

print(json.dumps(OneDictPerLine(inline), cls=MyEncoder))
# http://54.183.51.244/z-ent-7-wound_id_G-2501811622081094345

