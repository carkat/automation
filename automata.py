from collections import OrderedDict
from pprint      import pprint
import sys

def take(n,l):
    return l[:n] if n > 0 else l[n:]

def drop(n,l):
    return l[n:] if n > 0 else l[:n]

def first(l):
    return take(1,l)[0]

##### Data driven programming example
json = {
    'Do Standalone Functions': {
        'steps': [
            {
                'name': 'fun'
            }
        ]
    },

    'Do Things With Class Instance': {
        'class': True,
        'name': 'ClassExample',
        'args': [1,2,3],
        'steps': [
            {
                'name': 'method',
            },
            {
                'name': 'args_method',
                'args': [4]
            },
            {
                'name': 'cached_method',
                'cache': 'Do Standalone Functions/fun'
            },
            {
                'name': 'cached_with_args',
                'args': [12,2],
                'cache': 'Do Standalone Functions/fun'
            }
        ]
    }
}


### Simple Function Example
def fun():
    print('having fun')
    return 'had fun already'

##### Simple Class Example
class ClassExample:
    def __init__(self,a,b,c):
        print('doing things with my custom class')
        self.a = a
        self.b = b
        self.c = c

    def method(self):
        print('executing method')
        return 'success'

    def args_method(self, d):
        print(self.a+self.b+self.c+d)
        return 'something else'

    def cached_method(self, cached_result):
        return 'I got "{}"'.format(cached_result)

    def cached_with_args(self, a, b, cached_result):
        return 'I got "{}, {}, {}"'.format(a,b,cached_result)

##### The test runner consumes json
class runner:
    def __init__(self, behavior_data):
        self.results = {}
        self.__consume(behavior_data)

    def get_cached_result(self, obj):
        path = obj.get('cache').split('/')
        return self.recursive_get_cached_result(self.results, path)

    def recursive_get_cached_result(self, current_results, path):
        if len(path) > 1:
            return self.recursive_get_cached_result(current_results.get(first(path)), drop(1, path))
        return current_results.get(first(path))

    def build_eval_str(self, obj, i):
        cache, args  = [x in obj for x in ['cache', 'args']]
        evalstr      = 'i.'               if i is not  None else '' 
        argsstr      = '{}(*{}'           if args     else '{}('
        cachestr     = ', cached_result)' if cache and args  else 'cached_result)' if cache else ')'
        finalstr     = evalstr + argsstr + cachestr
        return finalstr

    def call(self, obj, i = None):
        eval_str      = self.build_eval_str(obj, i)
        cached_result = self.get_cached_result(obj) if 'cache' in obj else None
        try:
            if 'args' in obj:
                return eval(eval_str.format(obj.get('name'), obj.get('args')))
            else:
                return eval(eval_str.format(obj.get('name')))

        except Exception as e:
            print('Failed at:\nObject: ')
            pprint(obj)
            print('Instance: {}'.format(i))
            print('Eval String: {}'.format(eval_str))
            print('\nWith Error:\nError: {}'.format(e))
            print('System Info (if any): ')
            print(sys.exec_info()[0])


    def __consume(self, process_dict):
        for name, process in process_dict.items():
            i = self.call(process) if 'class' in process else None
            self.results[name] = {}
            for obj in process.get('steps'):
                self.results.get(name)[obj.get('name')] = self.call(obj, i)
        print(self.results)

runner(json)
