import difflib
import glob
import os
import shutil

import fire
import jsonpickle

NOW = "now"
LAST = "last"

_DIRNAME = ".golden_samples"

class Checker:
    def __init__(self, path):
        self.path = os.path.abspath(os.path.join(path, _DIRNAME))
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def list(self):
        for val in self._get_list():
            print(f"Name: {val['name']} Conflict: {val['conflict']}")

    def _get_list(self):
        result = []
        cands = glob.glob(os.path.join(self.path, "*.last"))
        for cand in cands:
            name = os.path.basename(cand).replace(".last", "").lower()
            conflict = os.path.exists(cand.replace(".last", ".now"))
            result.append({"name": name, "conflict": conflict, "filepath": cand})
        return result


    def review(self, name=None):
        read = lambda fn: open(fn, mode="r", encoding="utf-8").read().split("\n")
        for cand in self._get_entries(name, True):
            last_name = cand['filepath']
            last_cont = read(last_name)
            now_name = cand['filepath'].replace(".last", ".now")
            now_cont = read(now_name)
            diff = list(difflib.unified_diff(last_cont, now_cont,
                                             tofile=now_name, fromfile=last_name))
            print("\n".join(diff[2:]))

    def _get_entries(self, name, only_conflict=False):
        cands = self._get_list()
        if name is not None:
            cands = [c for c in cands if c['name'] == name.lower()
                     and (not only_conflict or c['conflict'])]
        return cands


    def approve(self, name=None):
        for cand in self._get_entries(name, True):
            last = cand['filepath']
            now = last.replace(".last", ".now")
            print(f"{os.path.basename(now)} => {os.path.basename(last)}")
            shutil.move(now, last)

    def check(self, obj, name):
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
        now_text = jsonpickle.encode(obj, unpicklable=False)

        last_filename = self._get_filename(name, LAST)
        if os.path.exists(last_filename):
            last_text = open(last_filename, mode="r", encoding="utf-8").read()
            diff = difflib.unified_diff(now_text.split("\n"), last_text.split("\n"))
            if len(list(diff)) != 0:
                now_filename = self._get_filename(name, NOW)
                self._write_file(now_filename, now_text)
                return False
            else:
                return True
        else:
            self._write_file(last_filename, now_text)
            return True

    def _get_filename(self, name, last):
        return os.path.join(self.path, f"{name}.{last}")

    def _write_file(self, filename, content):
        with open(filename, mode="w", encoding="utf-8") as out:
            out.write(content)



def api_list(self, path):
    checker = Checker(path)
    checker.list()

def api_review(self, path, name=None):
    checker = Checker(path)
    checker.review(name)

def api_approve(self, path, name=None):
    checker = Checker(path)
    checker.approve(name)

if __name__ == '__main__':
    fire.Fire({
        'list': api_list,
        'review': api_review,
        'approve': api_approve
    })

