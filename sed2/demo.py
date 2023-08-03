from process_bigraph.composite import Composite
from process_bigraph.type_system import types
from sed2.schemas import sed_types, sed_compositions

types.type_registry.register_multiple(sed_types)  # TODO -- this should go through __init__


def test_sed_composite():

    workflow = Composite({
        'composition': sed_compositions['estimate_and_run'],
        'schema': {
            'results': 'tree[any]'},
        'bridge': {
            'results': ['analysis_results']},
        'state': {
            'data': {},
            'model': '"something.sbml"',
            'parameter_estimation': {
                'address': 'local:sed2.toy_processes.EstimateParameters',  # using a local toy process
                'config': {},
                'wires': {
                    'inputs': {
                        'data': ['data'],
                        'model': ['model']},
                    'outputs': {
                        'parameters': ['parameters']}}},
            'simulator': {
                'address': 'local:sed2.toy_processes.UniformTimecourse',  # using a local toy process
                'config': {},
                'wires': {
                    'inputs': {
                        'model': ['model'],
                        'parameters': ['parameters']},
                    'outputs': {
                        'simulation_results': ['simulation_results']}}},
            'analysis': {
                'address': 'local:sed2.toy_processes.AnalyzeResults',  # using a local toy process
                'config': {},
                'wires': {
                    'inputs': {
                        'simulation_results': ['simulation_results']},
                    'outputs': {
                        'analysis_results': ['analysis_results']}}}}},
    )

    workflow.update({}, 0)   # TODO -- this is a step-only workflow, should not require interval


if __name__ == '__main__':
    test_sed_composite()
