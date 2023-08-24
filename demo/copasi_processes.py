"""
Processes for the demo
"""
from process_bigraph import Process, Composite, process_registry
# import libsbml
# from libsbml import SBMLReader
from basico import load_model, get_species


class CopasiProcess(Process):
    config_schema = {'model_file': 'string'}

    def __init__(self, config=None):
        super().__init__(config)
        # Load the single cell model into Basico
        self.copasi_model_object = load_model(self.config['model_file'])
        self.species_list = get_species(model=self.copasi_model_object).index.tolist()

    # @classmethod
    # def load(cls, sbml_model):
    #     return cls({'model_file': sbml_model})

    def schema(self):
        return {
            'species': {
                species_id: 'float' for species_id in self.species_list
            },
            'reactions': {
                reaction_id: 'float' for reaction_id in self.reactions_list
            },
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

    sbml_schema = {
        'species_store': 'tree[any]',  # 'dict[string,float]',
        'odeint': {
            '_type': 'process',
            '_ports': {
                'species': 'tree[any]',
            }
        },
    }

    # this is the instance for the composite process to run
    initial_sim_state = {
        'species_store': {},
        'odeint': {
            'address': 'local:copasi',  # using a local toy process
            'config': {
                'model_file': '"demo/Caravagna2010.xml"'  #
            },
            'interval': '1.0',
            'wires': {
                'species': 'species_store',
            }
        },
    }

    # make the composite
    workflow = Composite({
        'composition': sbml_schema,
        'schema': {
            'results': 'tree[any]'},
        'bridge': {
            'results': ['fluxes']},
        'state': initial_sim_state
    })

    # workflow.export_composite(filename='cobra_template')

    # run
    update = workflow.update({}, 1)  # TODO -- this is a step-only workflow, should not require interval. Also need emitter.
    print(f'UPDATE: {update}')


if __name__ == '__main__':
    test_process()
