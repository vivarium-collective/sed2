"""
Tellurium Process
"""
from process_bigraph import Process, Composite, process_registry
import tellurium


class TelluriumProcess(Process):
    config_schema = {'model_file': 'string'}

    def __init__(self, config=None):
        super().__init__(config)

        # initialize a tellurium(roadrunner) simulation object. Load the model in using either sbml(default) or antimony
        self.simulator = tellurium.loadSBMLModel(self.config['model_file'])

        # extract the variables
        self.floating_species_list = self.simulator.getFloatingSpeciesIds()
        self.boundary_species_list = self.simulator.getBoundarySpeciesIds()
        self.reaction_list = self.simulator.getReactionIds()

    @classmethod
    def load(cls, sbml_model):
        return cls({'model_file': sbml_model})

    def schema(self):
        fluxes_schema = {
            reaction.name: 'float' for reaction in self.floating_species_list}
        return {
            'species': fluxes_schema,  # 'dict[string,float]',
        }

    def update(self, state, interval):
        # set the states in tellurium according to what is passing in states
        for species_id, value in state['species'].items():
            self.tellurium_object.set_species(species_id, value)

        # run the simulation
        self.tellurium_object.simulate(0, interval, 1)

        # extract the results. TODO -- get the final values of the self.config['exposed_species'] and put them in the update
        update = {'species': {}}
        results = self.tellurium_object.get_data()

        return update


process_registry.register('tellurium', TelluriumProcess)


def test_process():

    # this is the schema for the FBA process. It should be pulled from an ontology.
    # TODO -- this does not match process schema. there should be warnings.
    sbml_schema = {
        'species_store': 'tree[any]',  # 'dict[string,float]',
        'tellurium': {
            '_type': 'process',
            '_ports': {
                'species': 'tree[any]',
            }
        },
    }

    # this is the instance for the composite process to run
    initial_sim_state = {
        'species_store': {},
        'tellurium': {
            'address': 'local:tellurium',  # using a local toy process
            'config': {
                'model_file': '"demo/Caravagna2010.xml"'
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

    # run
    update = workflow.update({}, 1)
    print(f'UPDATE: {update}')


if __name__ == '__main__':
    test_process()
