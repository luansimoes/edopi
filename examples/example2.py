from domain import TonalSystem

system = TonalSystem(27)
generators = system.get_generators()
for gen in generators[1:-1]:
    system.set_generator(gen)
    x = int(gen/2)
    diagram = system.balzano_diagram(x, gen-x)
    if diagram.contains_scale():
        system.diatonic_scale().show()
        diagram.show()