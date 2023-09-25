from process_bigraph import Process, Step, process_registry, types
import matplotlib.pyplot as plt
import pickle
import numpy as np

# serializers
def to_pickle(value, bindings=None, types=None):
    filepath = 'plot.pkl'
    # Save the value using pickle
    with open(filepath, 'wb') as file:
        pickle.dump(value, file)
    return filepath


# deserializers
def from_pickle(serialized, bindings=None, types=None):
    value = pickle.load(serialized)
    return value


types.serialize_registry.register('to_pickle', to_pickle)
types.deserialize_registry.register('from_pickle', from_pickle)


# types
demo_type_library = {
    # abstract number type
    'figure': {
        '_type': 'figure',
        '_apply': 'set',
        '_serialize': 'to_pickle',
        '_deserialize': 'from_pickle',
        '_description': 'matplotlib figure'},
}

types.type_registry.register_multiple(demo_type_library)


class Plot2D(Step):
    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {
            'inputs': {
                'results': 'dict',
                'curves': 'dict',
                'name': 'string'
            },
            'outputs': {
                'figure': 'figure'
            }
        }

    def update(self, inputs):
        results = inputs['results']
        curves = inputs['curves']
        name = inputs['name']

        plt.figure(name)
        for curve_name, axes in curves.items():
            x_values = results[axes['x']]
            y_values = results[axes['y']]
            plt.plot(x_values, y_values, label=name)

        return {
            'figure': plt
        }


