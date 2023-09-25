"""
COBRA FBA Process
"""
from process_bigraph import Process, Step, Composite, process_registry
from cobra.io import read_sbml_model
# from cobra_process.library import pf


class CobraProcess(Process):
    config_schema = {
        'model_file': 'string'
    }

    def __init__(self, config=None):
        super().__init__(config)
        self.model = read_sbml_model(self.config['model_file'])
        self.reactions = self.model.reactions
        self.metabolites = self.model.metabolites
        self.objective = self.model.objective
        self.boundary = self.model.boundary

    def initial_state(self):
        solution = self.model.optimize()
        optimized_fluxes = solution.fluxes

        state = {'fluxes': {}, 'reaction_bounds': {}}
        for reaction in self.model.reactions:
            state['fluxes'][reaction.id] = optimized_fluxes[reaction.id]
            state['reaction_bounds'][reaction.id] = {
                'lower_bound': reaction.lower_bound,
                'upper_bound': reaction.upper_bound}
        return state

    def schema(self):
        return {
            'fluxes': {
                reaction.id: 'float' for reaction in self.reactions
            },
            'objective_value': 'float',
            'reaction_bounds': {
                reaction.id: {
                    'upper_bound': 'float',
                    'lower_bound': 'float'
                } for reaction in self.reactions
            },
        }

    def update(self, state, interval):

        # set reaction bounds
        reaction_bounds = state['reaction_bounds']
        for reaction_id, bounds in reaction_bounds.items():
            self.model.reactions.get_by_id(reaction_id).bounds = (bounds['lower_bound'], bounds['upper_bound'])

        # run solver
        solution = self.model.optimize()

        return {
            'fluxes': solution.fluxes.to_dict(),
            'objective_value': solution.objective_value
        }


process_registry.register('cobra', CobraProcess)


def test_process():

    instance = {
        'fba': {
            '_type': 'process',
            'address': 'local:cobra',
            'config': {
                'model_file': 'cobra_process/models/e_coli_core.xml'
            },
            'wires': {
                'fluxes': ['fluxes_store'],
                'objective_value': ['objective_value_store'],
                'reaction_bounds': ['reaction_bounds_store'],
            }
        },
        'emitter': {
            '_type': 'step',
            'address': 'local:ram-emitter',
            'config': {
                'ports': {
                    'inputs': {
                        'fluxes': 'tree[float]',
                        'objective_value': 'tree[float]'
                    }
                }
            },
            'wires': {
                'inputs': {
                    'fluxes': ['fluxes_store'],
                    'objective_value': ['objective_value_store']
                }
            }
        }
    }

    # make the composite
    workflow = Composite({
        'state': instance
    })

    # run
    workflow.run(1)

    # gather results
    results = workflow.gather_results()
    print(f'RESULTS: {pf(results)}')


if __name__ == '__main__':
    test_process()
