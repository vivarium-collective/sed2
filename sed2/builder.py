import pprint

pretty = pprint.PrettyPrinter(indent=2)


def pf(x):
    return pretty.pformat(x)


def make_process_config(
        type=None,
        address=None,
        config=None,
        wires=None
):
    return {
        '_type': type,
        'address': address,
        'config': config,
        'wires': wires or {},
    }


class Node(dict):
    def add_process(self, process_id, **kwargs):
        self[process_id] = make_process_config(**kwargs)


class Builder:
    def __init__(self, bigraph_dict=None):
        self.bigraph_dict = bigraph_dict or {}

    def __setitem__(self, keys, value):
        # Convert single key to tuple
        keys = (keys,) if isinstance(keys, str) else keys

        # Navigate through the keys, creating nested dictionaries as needed
        d = self.bigraph_dict
        for key in keys[:-1]:  # iterate over keys to create the nested structure
            if key not in d:
                d[key] = Node()
            d = d[key]
        d[keys[-1]] = value  # set the value at the final level

    def __getitem__(self, keys):
        # Convert single key to tuple
        keys = (keys,) if isinstance(keys, str) else keys

        d = self.bigraph_dict
        for key in keys:
            d = d[key]  # move deeper into the dictionary
        return d

    def __repr__(self):
        return f"{pf(self.bigraph_dict)}"

    def add_process(self, process_id, **kwargs):
        # Add the process with the given ID and attributes
        self.bigraph_dict[process_id] = make_process_config(**kwargs)


def test_builder():
    # Testing the Builder class
    b = Builder()
    b['path', 'to', 'node'] = 1.0
    print(b.bigraph_dict)

    # Accessing the value
    value = b['path', 'to', 'node']
    print(value)

    b['path', 'b2', 'c'] = 12.0
    print(b)


    b.add_process(process_id='process1')
    b['path', 'to'].add_process(process_id='p1', type='example_type')
    b['path']


if __name__ == '__main__':
    test_builder()
