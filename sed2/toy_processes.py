from process_bigraph.composite import Step


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
