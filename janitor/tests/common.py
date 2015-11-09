import json
import inspect
import os
import unittest
import tempfile
import yaml

from janitor import policy

class BaseTest(unittest.TestCase):

    def load_policy(self, data):
        t = tempfile.NamedTemporaryFile()
        t.write(yaml.dump(data, Dumper=yaml.SafeDumper))
        t.flush()
        self.addCleanup(t.close)
        e = Config.empty()
        return policy.load(e, t.name)


def instance(state=None, **kw):
    data = json.loads(open(
        os.path.join(
            os.path.dirname(__file__), 'data',
            'instance.json')).read())
    if state:
        data.update(state)
    if kw:
        data.update(kw)
    return data


class Bag(dict):
        
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)
        
class Config(Bag):

    @classmethod
    def empty(cls, **kw):
        d = {}
        d.update({
            'region': "us-east-1",
            'cache': '',
            'output_dir': 's3://test-example/foo',
            'cache_period': 0,
            'dryrun': False})
        d.update(kw)
        return cls(d)

    
class Instance(Bag): pass
class Reservation(Bag): pass



class Client(object):

    def __init__(self, instances):
        self.instances = instances
        self.filters = None

    def get_all_instances(self, filters=None):
        self.filters = filters
        return [Reservation(
            {'instances': [i for i in self.instances]})]
        
        
