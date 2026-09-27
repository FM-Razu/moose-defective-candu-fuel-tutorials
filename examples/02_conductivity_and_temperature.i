# Teaching analogue of heat generation in fuel.
# Geometry, conductivity, and source are normalized example values.
[Mesh]
  [fuel]
    type = GeneratedMeshGenerator
    dim = 1
    nx = 20
    xmin = 0
    xmax = 1
  []
[]

[Variables]
  [T]
  []
[]

[Kernels]
  [conduction]
    type = MatDiffusion
    variable = T
    diffusivity = k
  []
  [heat_generation]
    type = BodyForce
    variable = T
    value = 8
  []
[]

[Materials]
  [fuel_conductivity]
    type = GenericConstantMaterial
    prop_names = k
    prop_values = 1
  []
[]

[BCs]
  [left]
    type = DirichletBC
    variable = T
    boundary = left
    value = 300
  []
  [right]
    type = DirichletBC
    variable = T
    boundary = right
    value = 300
  []
[]

[Postprocessors]
  [center_T]
    type = PointValue
    variable = T
    point = '0.5 0 0'
  []
[]

[Executioner]
  type = Steady
[]

[Outputs]
  csv = true
[]
