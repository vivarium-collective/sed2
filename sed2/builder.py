import pprint

pretty = pprint.PrettyPrinter(indent=2)


def pf(x):
    return pretty.pformat(x)


class Builder:
    def __init__(self, bigraph_dict=None):
        self.bigraph_dict = bigraph_dict or {}

    def __setitem__(self, keys, value):
        # Navigate through the keys, creating nested dictionaries as needed
        d = self.bigraph_dict
        for key in keys[:-1]:  # iterate over keys to create the nested structure
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value  # set the value at the final level

    def __getitem__(self, keys):
        # Navigate through the keys to retrieve the value
        d = self.bigraph_dict
        for key in keys:
            d = d[key]  # move deeper into the dictionary
        return d  # return the value found at the final level

    def __repr__(self):
        return f"{pf(self.bigraph_dict)}"



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


if __name__ == '__main__':
    test_builder()