from process_bigraph import Process, Step, process_registry
import matplotlib.pyplot as plt
import numpy as np


class Plot2D(Step):
    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {
            'inputs': {
                'results': 'dict',
                'curves': 'dict',
                'name': 'str'},
            'outputs': {
                'figure': 'Fig'
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


