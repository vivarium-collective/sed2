from process_bigraph.type_system import types  #ProcessTypes

# types = ProcessTypes()   # TODO -- how will Composite know these types?

types.type_registry.register('sbml', {
    '_super': 'string',
    '_default': '"something.sbml"',
    '_description': 'sbml model file'})
