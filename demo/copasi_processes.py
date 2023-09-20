"""
Processes for the demo
"""
from process_bigraph import Process, Composite, process_registry
from basico import load_model, get_species


class CopasiProcess(Process):
    config_schema = {'model_file': 'string'}

    def __init__(self, config=None):
        super().__init__(config)
        # Load the single cell model into Basico
        self.copasi_model_object = load_model(self.config['model_file'])
        self.species_list = get_species(model=self.copasi_model_object).index.tolist()

    def initial_state(self):
        return {}

    def schema(self):
        return {
            'species': {
                species_id: 'float' for species_id in self.species_list
            },
            # 'reactions': {
            #     reaction_id: 'float' for reaction_id in self.reactions_list
            # },
        }

    def update(self, state, interval):
        return {}
        # # set the states
        # for species_id, value in state['species'].items():
        #     self.tellurium_object.set_species(species_id, value)
        #
        # sim_result = self.model.sbml_model.simulate(
        #     start=0, end=interval, points=1, selections=selection_list)
        # return {column: sim_result[column] for column in sim_result.colnames}


process_registry.register('copasi', CopasiProcess)


def test_process():

    # this is the instance for the composite process to run
    initial_sim_state = {
        'odeint': {
            '_type': 'process',
            'address': 'local:copasi',  # using a local toy process
            'config': {
                'model_file': 'demo/Caravagna2010.xml'  #
            },
            'wires': {
                'species': ['species_store'],
                # 'reactions': ['reactions_store'],
            }
        },
        'emitter': {
            '_type': 'step',
            'address': 'local:ram-emitter',
            'config': {
                'ports': {
                    'inputs': {
                        'floating_species': 'tree[float]'
                    }
                }
            },
            'wires': {
                'inputs': {
                    'floating_species': ['floating_species_store'],
                }
            }
        }
    }

    # make the composite
    workflow = Composite({
        'state': initial_sim_state
    })

    # workflow.export_composite(filename='cobra_template')

    # run
    workflow.run(10)

    # gather results
    results = workflow.gather_results()
    print(f'RESULTS: {results}')


if __name__ == '__main__':
    test_process()
