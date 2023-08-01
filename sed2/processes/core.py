from process_bigraph.composite import Step, Composite


class EstimateParameters(Step):
    defaults = {}

    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {
            'inputs': {
                'data': 'tree[any]',
                'model': 'sbml'},
            'outputs': {
                'parameters': 'tree[any]'
            }
        }

    def update(self, input):
        return {}


class UniformTimecourse(Step):
    defaults = {}

    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {
            'inputs': {
                'model': 'sbml',
                'parameters': 'tree[any]'
            },
            'outputs': {
                'simulation_results': 'tree[any]'
            }
        }

    def update(self, input):
        return {}


class AnalyzeResults(Step):
    defaults = {}

    def __init__(self, config=None):
        super().__init__(config)

    def schema(self):
        return {
            'inputs': {
                'simulation_results': 'tree[any]'
            },
            'outputs': {
                'analysis_results': 'tree[any]'
            }
        }

    def update(self, input):
        return {}




def test_sed_composite():

    workflow = Composite({
        'composition': {
            'data': 'tree[any]',
            'model': 'sbml',
            'parameters': 'tree[any]',
            'simulation_results': 'tree[any]',
            'analysis_results': 'tree[any]',
            'parameter_estimation': {
                '_type': 'step',
                '_ports': {   # TODO -- this is provided by the Process schema, why is it required here?
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
        'schema': {
            'results': 'tree[any]'},
        'bridge': {
            'results': ['analysis_results']},
        'state': {
            'data': {},
            'model': '"something.sbml"',
            'parameter_estimation': {
                'address': 'local:process_bigraph.experiments.toys.EstimateParameters',
                'config': {},
                'wires': {
                    'inputs': {
                        'data': ['data'],
                        'model': ['model']},
                    'outputs': {
                        'parameters': ['parameters']}}},
            'simulator': {
                'address': 'local:process_bigraph.experiments.toys.UniformTimecourse',
                'config': {},
                'wires': {
                    'inputs': {
                        'model': ['model'],
                        'parameters': ['parameters']},
                    'outputs': {
                        'simulation_results': ['simulation_results']}}},
            'analysis': {
                'address': 'local:process_bigraph.experiments.toys.AnalyzeResults',
                'config': {},
                'wires': {
                    'inputs': {
                        'simulation_results': ['simulation_results']},
                    'outputs': {
                        'analysis_results': ['analysis_results']}}}}},
    )
