import datetime
import difflib
import re

import deepdiff
import jsonpickle


class JustSomeObject:
    def __init__(self):
        self.a = "Hello"
        self.b = 1
        self.c = 2.33433
        self.d = [1, 2.3333, 3.3332]
        self.e = "2020-05-12"
        self.f = datetime.datetime.now()


p = JustSomeObject()
p2 = JustSomeObject()
p2.d.pop()
p2.c += 0.5

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)


def clean_fp(ser, digits=2):
    rx = r"(\d+\.\d{X})\d*".replace("X", str(digits))
    result = re.sub(rx, r"\1", ser)
    return result


def clean_date(ser, replacement="DATE"):
    rx = "\d{4}-\d{2}-\d{2}"
    result = re.sub(rx, replacement, ser)
    return result


def diff_json(o1, o2):
    def process(o):
        s = jsonpickle.encode(o, unpicklable=False)
        s2 = clean_fp(s, 1)
        s3 = clean_date(s2)
        return s3.split("\n")

    s1 = process(o1)
    s2 = process(o2)
    result = difflib.unified_diff(s1, s2)
    return list(result)


def diff_deepdiff(o1, o2):
    opts = dict(
        exclude_types=[datetime.datetime],
        significant_digits=1
    )
    return deepdiff.DeepDiff(o1, o2, **opts).to_dict()


d1 = diff_json(p, p2)
d1b = diff_json(p,p)
#d2 = diff_deepdiff(test_data, changed_test_data)

a = 1


