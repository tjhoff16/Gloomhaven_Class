class val(object):
    """docstring for val."""
    def __init__(self, val):
        self.val = val
        self.name = str(val)

a, b = val(1),val(2)
ch = min (a,b,key=val)
print (ch)
