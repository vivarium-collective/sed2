'''simulation experiment design demos

The composition schema was developed for integrative simulations, but can also be used for workflows such as simulation
experiments. This experimental notebook demonstrates simulation experiments as composites, going from the declarative
JSON format to executable python script.

Example scripts were provided here: https://docs.google.com/document/d/1jZkaNhM_cOqMWtd4sJZ9b0VGXPTLsDKsRNI5Yvu4nOA/edit
'''

from process_bigraph import Composite
from sed2 import pf


def test_sed1():
    instance = {
        # 'time_start': 0,
        # 'time_end': 10,
        # 'num_points': 50,
        # 'selection_list': ['time', 'S', 'Z'],
        # 'model_path': 'demo/BIOMD0000000061_url.xml',
        # 'curves': {
        #     'Susceptible': {'x': 'time', 'y': 'S'},
        #     'Zombie': {'x': 'time', 'y': 'Z'}
        # },
        # 'figure1name': '"Figure1"',
        # 'sbml_model_from_path': {
        #     '_type': 'model_path',
        #     'wires': {
        #         'path_to_sbml': 'model_path',
        #         'model': 'model_instance'
        #     },
        # },
        'plot2d': {
            '_type': 'step',
            'address': 'local:plot2d',
            'config': {},
            'wires': {
                'results': 'results',
                'curves': 'curves',
                'name': 'figure1name',
                'figure': 'figure'
            },
            '_depends_on': ['uniform_time_course'],
        },
        'uniform_time_course': {
            '_type': 'process',
            'address': 'local:tellurium',
            'config': {
                'sbml_model_path': 'demo/BIOMD0000000061_url.xml',
            },
            'wires': {
                'time': ['time_store'],
                'floating_species': ['floating_species_store'],
                'boundary_species': ['boundary_species_store'],
                'model_parameters': ['model_parameters_store'],
                'reactions': ['reactions_store'],
            }
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
