'''simulation experiment design demos

The composition schema was developed for integrative simulations, but can also be used for workflows such as simulation
experiments. This experimental notebook demonstrates simulation experiments as composites, going from the declarative
JSON format to executable python script.

Example scripts were provided here: https://docs.google.com/document/d/1jZkaNhM_cOqMWtd4sJZ9b0VGXPTLsDKsRNI5Yvu4nOA/edit
'''

from process_bigraph import Composite, process_registry, types
from sed2 import pf
from demo_processes import process_registry  # trigger process registration by importing


def test_sed1():
    instance = {
        'start_time_store': 0,
        'run_time_store': 10,
        'curves_store': [
            ['time', 'GlcX'],
            ['time', 'Glc']
        ],
        'figure_store': {
            '_type': 'string'},  # TODO -- this should not be needed. Step output ports needs to project into schema.
        'uniform_time_course': {
            '_type': 'step',
            'address': 'local:tellurium_step',
            'config': {
                'sbml_model_path': 'demo_processes/BIOMD0000000061_url.xml',
            },
            'wires': {
                'inputs': {
                    'time': ['start_time_store'],
                    'run_time': ['run_time_store'],
                },
                'outputs': {
                    'results': ['results_store'],   # This is named array
                }
            }
        },
        'plot2d': {
            '_type': 'step',
            'address': 'local:plot2d',
            'config': {
                'filename': 'figure1'
            },
            'wires': {
                'inputs': {
                    'results': ['results_store'],  # This will run when the results are updated
                    'curves': ['curves_store'],
                },
                'outputs': {
                    'figure_path': ['figure_store']
                }
            }
        }
    }

    workflow = Composite({
        'state': instance
    })

    fig = workflow.state['figure_store']


def test_sed2():
    pass



if __name__ == '__main__':
    test_sed1()
    test_sed2()
