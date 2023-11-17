"""
Builder
=======
"""

import pprint

pretty = pprint.PrettyPrinter(indent=2)


def pf(x):
    return pretty.pformat(x)


class Node(dict):
    def add_process(
            self,
            name,
            process_type=None,
            address=None,
            config=None,
            inputs=None,
            outputs=None,
    ):
        self[name] = {
            '_type': process_type or 'process',
            'address': address or '',
            'config': config or {},
            'wires': {
                'inputs': inputs or {},
                'outputs': outputs or {},
            },
        }
        return self[name]

    def add_task(
            self,
            name,
            inputs=None,
            outputs=None
    ):
        self[name] = Node({
            '_type': 'task',
            'inputs': inputs or {},
            'outputs': outputs or {},
        })
        return self[name]  # Return the new task node

    def add_simulation(
            self,
            name,
            simulator_id=None,
            model_id=None,
            start_time=None,
            end_time=None,
            number_of_points=None,
            inputs=None,
            outputs=None
    ):
        self[name] = Node({
            '_type': 'simulation',
            'config': {
                'simulator_id': simulator_id,
                'model_id': model_id,
                'start_time': start_time,
                'end_time': end_time,
                'number_of_points': number_of_points,
            },
            'wires': {
                'inputs': inputs,
                'outputs': outputs,
            }
        })
        return self[name]  # Return the new simulation node

    def add_data_generator(self, name, inputs=None, outputs=None, **kwargs):
        self[name] = Node({
            '_type': 'data_generator',
            'config': dict(kwargs),
            'wires': {
                'inputs': inputs,
                'outputs': outputs,
            }
        })
        return self[name]  # Return the new node

    def add_visualization(self, name, inputs=None, outputs=None, **kwargs):
        self[name] = Node({
            '_type': 'visualization',
            'config': dict(kwargs),
            'wires': {
                'inputs': inputs,
                'outputs': outputs,
            }
        })
        return self[name]  # Return the new node

    def add_repeated_task(self, name, range=None, inputs=None, outputs=None):
        pass
    

class Builder(Node):

    def __init__(self, tree=None):
        super().__init__()
        self.tree = tree or {}

    def __setitem__(self, keys, value):
        # Convert single key to tuple
        keys = (keys,) if isinstance(keys, str) else keys

        # Navigate through the keys, creating nested dictionaries as needed
        d = self.tree
        for key in keys[:-1]:  # iterate over keys to create the nested structure
            if key not in d:
                d[key] = Node()
            d = d[key]
        d[keys[-1]] = value  # set the value at the final level

    def __getitem__(self, keys):
        # Convert single key to tuple
        keys = (keys,) if isinstance(keys, str) else keys

        d = self.tree
        for key in keys:
            d = d[key]  # move deeper into the dictionary
        return d

    def __repr__(self):
        return f"{pf(self.tree)}"



def test_builder():
    # Testing the Builder class
    b = Builder()
    b['path', 'to', 'node'] = 1.0
    print(b.tree)

    # Accessing the value
    value = b['path', 'to', 'node']
    print(value)

    b['path', 'b2', 'c'] = 12.0
    print(b)

    b.add_process(process_id='process1')
    b['path', 'to'].add_process(process_id='p1', process_type='example_type')
    print(b['path'])



def test_builder_demo():

    sed_schema = {
        'models': {},
        'algorithms': {},
        'visualizations': {},
        'tasks': {},
    }
    a = Builder(sed_schema)

    # or
    b = Builder()
    b['models'] = {}
    b['algorithms'] = {}
    b['visualizations'] = {}
    b['tasks'] = {}

    b.add_process(process_id='p1', address='', config={}, inputs={}, outputs={})
    b



if __name__ == '__main__':
    # test_builder()
    test_builder_demo()
