# Run-data provenance

The user ran the three exercises with the `idaholab/moose:latest` Docker image in Ubuntu 24.04 under WSL 2 on Windows 11, then copied the three exact input files and three generated outputs from `~/moose-practice` into the shared workspace on 28 September 2026. The files in `examples/` are those copied inputs. This `data/` folder contains the copied outputs, with the CSV files given shorter repository names:

| Ubuntu run file | Repository file | SHA-256 of original output |
| --- | --- | --- |
| `01_defective_pin_mesh_in.e` | `01_defective_pin_mesh_in.e` | `c4f323ea9126caf3205f0b198caadba5d1fbc5675a7e5a8e295d57a1036a8910` |
| `02_conductivity_and_temperature_out.csv` | `heat_center.csv` | `1aa03d0e3cd8ecdb4dbe3ac95484d8613c11a68b21d4f346ddbeb2db33c60718` |
| `03_oxygen_ingress_out.csv` | `oxygen_center.csv` | `cdd2b13cea71f163570f0b6f052480cc0c5a00e25a45e5342828e4294058a3cf` |

The `*.e` file is a 9,516-byte binary Exodus mesh. The CSV values are normalized teaching outputs, not measured CANDU fuel data or numerical reproductions of Lewis (2024). The Docker image tag `latest` is mutable; the image digest and MOOSE version were not captured during the runs.
