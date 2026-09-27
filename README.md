# MOOSE exercises inspired by defective CANDU fuel research

Three small, runnable MOOSE exercises introduce ideas from B. J. Lewis, ["Modelling of defective CANDU fuel phenomena"](https://doi.org/10.1016/j.jnucmat.2023.154877), *Journal of Nuclear Materials* **590** (2024), 154877. The paper studies coupled fuel oxidation, heat conduction, fission product transport, and sheath hydriding after a fuel defect. These examples are teaching analogues with illustrative, normalized values. **They do not reproduce or validate the paper's model.**

![Conceptual connections among the exercises](figures/conceptual_coupling.svg)

| Example | Input | Main output | Idea |
| --- | --- | --- | --- |
| 1. Fuel element regions | [`examples/01_defective_pin_mesh.i`](examples/01_defective_pin_mesh.i) | [Exodus mesh](data/01_defective_pin_mesh_in.e) | Distinguish fuel, gap, sheath, and coolant regions |
| 2. Heat and conductivity | [`examples/02_conductivity_and_temperature.i`](examples/02_conductivity_and_temperature.i) | [`data/heat_center.csv`](data/heat_center.csv) | Lower conductivity raises center temperature under the same heating |
| 3. Oxygen ingress | [`examples/03_oxygen_ingress.i`](examples/03_oxygen_ingress.i) | [`data/oxygen_center.csv`](data/oxygen_center.csv) | Oxygen diffuses inward from a defect-side boundary |

The observed heat run ended at **301.00000000004** model temperature units at the center. The observed oxygen run rose from **0** to **0.25974969442372** normalized concentration at the midpoint by model time 1. See the [detailed report](docs/report.md) for equations, every input section, plots, interpretation, limits, and data provenance.

## Run in your Ubuntu WSL installation

These commands assume the official `idaholab/moose:latest` Docker image is already installed. Work in the Linux home directory for better WSL performance. At your **Ubuntu prompt**:

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/FM-Razu/moose-defective-candu-fuel-tutorials.git
cd ~/projects/moose-defective-candu-fuel-tutorials
sudo docker run --rm -it -v "$PWD:/work" -w /work idaholab/moose:latest
```

At the **container prompt** (`bash-4.4#`), run:

```bash
cd examples
moose-opt -i 01_defective_pin_mesh.i --mesh-only
moose-opt -i 02_conductivity_and_temperature.i
moose-opt -i 03_oxygen_ingress.i
exit
```

MOOSE writes results alongside each input file. After `exit`, the generated results will be in `examples/`. The files in `data/` are the original outputs copied from the user's successful runs. The first example creates a mesh but has no physics solve; use `--mesh-only` for that input.

To regenerate the figures after updating `data/oxygen_center.csv`, run `python3 scripts/generate_figures.py` in Ubuntu. The script uses only the Python standard library.

## Source and provenance

- [Lewis (2024), DOI: 10.1016/j.jnucmat.2023.154877](https://doi.org/10.1016/j.jnucmat.2023.154877)
- [MOOSE Reactor Module geometry guide](https://mooseframework.inl.gov/getting_started/examples_and_tutorials/tutorial04_meshing/step05_common_geom.html)
- [MOOSE `--mesh-only` workflow](https://mooseframework.inl.gov/getting_started/examples_and_tutorials/tutorial04_meshing/step03_workflow.html)
- [MOOSE Docker image guide](https://mooseframework.inl.gov/getting_started/installation/docker.html)
- [Run-data provenance](data/PROVENANCE.md)

The paper's PDF is intentionally not redistributed here. No license is asserted for the paper or MOOSE. The teaching inputs, report, and figures in this repository are original educational materials.
