from edopi import TonalSystem

system = TonalSystem(28, 15)
scale = system.diatonic_scale()
scale.export_scala_files('ken_28.scl')


elements = scale.elements
elements[1] -=1
altered_scale = system.scale(elements=elements, name='Altered Kennedy 28-EDO Scale')
altered_scale.export_scala_files('ken_28_alt.scl')


altered_scale.show()