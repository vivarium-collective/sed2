from process_bigraph import Process, Step, process_registry, types
import matplotlib.pyplot as plt
import pickle


class DataOperation(Step):
    config_schema = {
        'observables': 'dict',
        'operations': 'dict',
    }

    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {}

    def update(self, inputs):
        return {}



class Plot2D(Step):
    config_schema = {
        'filename': 'string'
    }
    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {
            'inputs': {
                'results': {'_type': 'numpy_array', '_apply': 'set'},
                'curves': 'list[dict]',
            },
            'outputs': {
                'figure_path': 'string'
            }
        }

    def update(self, inputs):
        results = inputs['results']
        curves = inputs['curves']
        name = self.config['filename']

        plt.figure(name)
        for curve in curves:
            x_values = results[curve['x']]
            y_values = results[curve['y']]
            plt.plot(x_values, y_values, label=name)

        figure_path = f'out/{name}'
        plt.savefig(figure_path)

        return {
            'figure_path': figure_path
        }
