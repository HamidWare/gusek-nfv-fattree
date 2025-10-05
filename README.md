# NFV VNF Placement on a Fat-Tree (Gusek/GLPK + GMPL)

Formulate and solve an **NFV placement + routing** model for multiple flows on a **fat-tree** data-center topology using **Gusek** (GLPK IDE) and **GNU MathProg (GMPL)**. Flows require ordered VNF chains; the model enforces node CPU/MEM and link capacity, plus optional policies like VNF colocation.

> Gusek is a Windows IDE bundling GLPK; you can also run GLPK from the command line via `glpsol`. The fat-tree provides many equal-cost paths; start with **k = 4**, then extend to **k = 8**.

---

## Project structure

    gusek-nfv-fattree/
    ├─ src/
    │  └─ nfv_placement.mod              # GMPL model
    ├─ scripts/
    │  ├─ gen_link_costs.py              # generates link costs CSV
    │  └─ gen_node_caps.py               # generates node CPU/MEM CSV
    ├─ docs/
    │  └─ Assignment3_EN.md              # English problem statement
    ├─ results/
    │  └─ run_primary_source.log         # solver log from your first run
    ├─ requirements.txt                  # deps for the helper scripts
    ├─ .gitignore
    ├─ LICENSE
    └─ README.md

---

## Requirements

- **GLPK** (with Gusek on Windows, or native GLPK on any OS)
- Optional (only if you use the helper scripts):

      # requirements.txt
      pandas>=2.0
      networkx>=3.2
      numpy>=1.25
      matplotlib>=3.7

Install the optional Python deps:

    pip install -r requirements.txt

---

## How to run the model

### Option A — Gusek (GUI)

1. Open `src/nfv_placement.mod` in **Gusek**.
2. If your model contains a separate `data; ... end;` block inside the `.mod`, just run it.
3. If you externalize data later, set the active `.dat` file in Gusek and run again.

### Option B — `glpsol` (CLI)

- Model with inline data:

      glpsol -m src/nfv_placement.mod -o results/run_k4.txt

- Model plus external data (if you add it later):

      glpsol -m src/nfv_placement.mod -d src/k4.dat -o results/run_k4.txt

`-m` attaches the GMPL model, `-d` adds a data file, and `-o` writes the solver report.

---

## Inputs the model expects (conceptually)

- **Flows:** source, destination, demand, ordered list of required VNFs
- **Node caps:** per-node CPU and memory
- **Link attrs:** bandwidth and traversal cost

Your two small Python scripts can generate quick CSVs:
- `scripts/gen_link_costs.py` writes a **space-separated** `cost of each link.csv`.
- `scripts/gen_node_caps.py` writes a **space-separated** `cpu & memory.csv`.

Keep filenames or update the model’s `data` section accordingly.

---

## What’s inside the model (high level)

- **Variables**
  - `x[i,j,f] ∈ {0,1}` — flow `f` uses link `(i,j)`
  - `y[n,f,m] ∈ {0,1}` — place VNF `m` of flow `f` on node `n`

- **Objective**
  - minimize link traversal cost × demand + node CPU/MEM usage cost

- **Constraints**
  - flow conservation; link capacity; node CPU/MEM capacity
  - each required VNF sits on a node the path actually visits
  - preserve VNF order (if required)
  - no cycles (anti-cycle or hop cap)
  - **policy toggles** via parameters (e.g., `COLOCATE`, `AVOID_LOOPS`, `PATHLEN_CAP`) so scenarios switch without editing constraints

---

## Reproduce the included log

`results/run_primary_source.log` comes from a baseline `glpsol` run. To generate a fresh log:

    glpsol -m src/nfv_placement.mod -o results/run_primary_source.log

If you move to k=8 and externalize data:

    glpsol -m src/nfv_placement.mod -d src/k8.dat -o results/run_k8.txt

---

## Notes & tips

- Keep data tables clean and consistent (space-separated CSVs or a `.dat` file).
- If the solver declares infeasibility, first relax cycles or the path-length cap, then re-add optional constraints one by one.
- Fat-tree quick sanity: k-ary fat-tree has `(k/2)^2` core switches and two layers per pod (edge/aggregation). Start with **k=4** to validate, then scale to **k=8**.

---

## Acknowledgments

- GLPK + Gusek for MathProg modeling and solving.
- Classic fat-tree/Clos topology notes.
