
sed_types = {
    'sbml': {
        '_super': 'string',
        '_default': '"something.sbml"',
        '_description': 'sbml model file'
    }
}

sed_compositions = {
    'estimate_and_run': {
        'data': 'tree[any]',
        'model': 'sbml',
        'parameters': 'tree[any]',
        'simulation_results': 'tree[any]',
        'analysis_results': 'tree[any]',
        'parameter_estimation': {
            '_type': 'step',
            '_ports': {
                'inputs': {
                    'data': 'tree[any]',
                    'model': 'sbml'},
                'outputs': {
                    'parameters': 'tree[any]'}}},
        'simulator': {
            '_type': 'step',
            '_ports': {
                'inputs': {
                    'model': 'sbml',
                    'parameters': 'tree[any]'},
                'outputs': {
                    'simulation_results': 'tree[any]'}}},
        'analysis': {
            '_type': 'step',
            '_ports': {
                'inputs': {
                    'simulation_results': 'tree[any]'},
                'outputs': {
                    'analysis_results': 'tree[any]'}}}},
}