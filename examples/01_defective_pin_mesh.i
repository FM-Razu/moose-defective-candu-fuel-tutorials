# Teaching geometry only: 2-D cross-section of a fuel element.
# All dimensions are illustrative, not values from Lewis (2024).
[Mesh]
  [pin]
    type = PolygonConcentricCircleMeshGenerator
    num_sides = 6
    num_sectors_per_side = '2 2 2 2 2 2'
    polygon_size = 0.7
    ring_radii = '0.40 0.42 0.48'
    ring_intervals = '2 1 1'
    ring_block_ids = '10 11 12 13'
    ring_block_names = 'fuel_center fuel gap sheath'
    background_intervals = 1
    background_block_ids = 20
    background_block_names = coolant
    preserve_volumes = on
  []
[]
