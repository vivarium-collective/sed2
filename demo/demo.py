'''simulation experiment design demos

The composition schema was developed for integrative simulations, but can also be used for workflows such as simulation
experiments. This experimental notebook demonstrates simulation experiments as composites, going from the declarative
JSON format to executable python script.

Example scripts were provided here: https://docs.google.com/document/d/1jZkaNhM_cOqMWtd4sJZ9b0VGXPTLsDKsRNI5Yvu4nOA/edit
'''

from process_bigraph import Composite, process_registry, types
from sed2 import pf
from demo_processes import process_registry  # trigger process registration by importing
# import importlib
# importlib.reload(demo_processes)


def test_sed1():
    instance = {
        'start_time_store': 0,
        'run_time_store': 1,
        'uniform_time_course': {
            '_type': 'step',   # TODO -- should this be a step that runs once?
            'address': 'local:tellurium_step',
            'config': {
                'sbml_model_path': 'demo_processes/BIOMD0000000061_url.xml',
            },
            'wires': {
                'inputs': {
                    'time': ['start_time_store'],
                    'run_time': ['run_time_store'],
                    'floating_species': ['floating_species_store'],
                    'boundary_species': ['boundary_species_store'],
                    'model_parameters': ['model_parameters_store'],
                    'reactions': ['reactions_store'],
                },
                'outputs': {
                    'results': ['results_store'],
                }
            }
        },
        'plot2d': {
            '_type': 'step',
            'address': 'local:plot2d',
            'config': {},
            'wires': {
                'inputs': {
                    'results': ['results'],
                    'curves': ['curves'],
                    'name': ['figure1name']
                },
                'outputs': {
                    'figure': ['figure_store']
                }
            },
            '_depends_on': ['uniform_time_course'],
        },

    }

    workflow = Composite({'state': instance})

    # run
    workflow.run(10)

    # gather results
    results = workflow.gather_results()
    print(f'RESULTS: {pf(results)}')


def test_sed2():
    pass



if __name__ == '__main__':
    test_sed1()
    test_sed2()
