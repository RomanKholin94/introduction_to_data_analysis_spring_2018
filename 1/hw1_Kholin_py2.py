#!/bin/bash
# -*- coding: utf-8 -*-

import json
import csv
from random import randint

class SuperDict:
    def __init__(self, init):
        if isinstance(init, dict):
            self.d = init
        elif isinstance(init, str):
            if (init.endswith(".json")):
                with open(init) as f_in:
                    self.d = json.load(f_in)
                with open(init) as f_in:
                    self.d = json.loads(f_in.read())
            elif (init.endswith(".csv")):
                pass
            else:
                self.d = {}
        else:
            self.d = {}
    def __getitem__ (self, *args, **kwargs):
        return self.d. __getitem__ (*args, **kwargs)
    def clear (self, *args, **kwargs):
        return self.d. clear (*args, **kwargs)
    def items (self, *args, **kwargs):
        return self.d. items (*args, **kwargs)
    def keys (self, *args, **kwargs):
        return self.d. keys (*args, **kwargs)
    def values (self, *args, **kwargs):
        return self.d. values (*args, **kwargs)
    def iteritems (self, *args, **kwargs):
        return self.d. iteritems (*args, **kwargs)
    def iterkeys (self, *args, **kwargs):
        return self.d. iterkeys (*args, **kwargs)
    def itervalues (self, *args, **kwargs):
        return self.d. itervalues (*args, **kwargs)
    def __iter__ (self, *args, **kwargs):
        return self.d. __iter__ (*args, **kwargs)
    def __eq__ (self, *args, **kwargs):
        return self.d. __eq__ (*args, **kwargs)
    def __len__ (self, *args, **kwargs):
        return self.d. __len__ (*args, **kwargs)
    def __add__ (self, other):
        ans = SuperDict({})
        ans.d.update(self.d)
        ans.d.update(other.d)
        return ans
    def to_json(self, fout):
        with open(fout, 'w') as f_out:
            json.dump(self.d, f_out)
        with open(fout, 'w') as f_out:
            f_out.write(json.dumps(self.d))
    def get_key_starts_from(self, s):
        for i in self.d.iterkeys():
            if i.startswith(s):
                print s
    def get_random_key(self):
        r = randint(0, len(self.d))
        for i, j in enumerate(self.d.itervalues()):
            if i == r:
                print j
