# Teaching analogue of oxygen entering fuel near a sheath defect.
# Concentration, length, diffusivity, and time are normalized.
[Mesh]
  [fuel_path]
    type = GeneratedMeshGenerator
    dim = 1
    nx = 40
    xmin = 0
    xmax = 1
  []
[]

[Variables]
  [c]
    initial_condition = 0
  []
[]

[Kernels]
  [accumulation]
    type = TimeDerivative
    variable = c
  []
  [diffusion]
    type = MatDiffusion
    variable = c
    diffusivity = D
  []
[]

[Materials]
  [oxygen_diffusivity]
    type = GenericConstantMaterial
    prop_names = D
    prop_values = 0.1
  []
[]

[BCs]
  [defect_side]
    type = DirichletBC
    variable = c
    boundary = left
    value = 1
  []
[]

[Postprocessors]
  [center_c]
    type = PointValue
    variable = c
    point = '0.5 0 0'
  []
[]

[Executioner]
  type = Transient
  dt = 0.05
  end_time = 1
[]

[Outputs]
  csv = true
[]
