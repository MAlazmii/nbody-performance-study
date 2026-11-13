# Measurement method and source

## Cirrus coursework record

The historical table comes from Table 3.1 of the author's 2024–25 Performance
Programming optimisation report at the University of Edinburgh. The six rows
represent recorded 500-step runtimes on Cirrus. They span compiler and source
changes, so adjacent rows describe cumulative configurations. The final
exploratory configuration used `-Ofast -ipo -xHost`. The archived Makefile uses
`-O3 -ipo`. Sample counts, a verified mapping from each stage to a saved binary
and source revision, and detailed machine configuration are unavailable.

The saved profiling report attributes 43.86 sampled CPU seconds to five calls
to the simulation update routine. This identified where to investigate. The
profiling record cannot be linked to a particular row of the timing table.

## Archive checks

The 100-step snapshot and the reference inside the submitted ZIP are byte
identical. All five saved snapshots and that reference contain 4,096 rows of
nine finite numeric fields each. The reference's producing build is unknown.
The archive contains one reference for that comparison. A comparison of a later
snapshot against the same file cannot establish error at the later timestep.

The submission's driver and coordinate header match the supplied teaching
files byte for byte. Its simulation and utility source contain modifications.
This case study contains derived measurements, original explanatory text and
plotting code. The assignment source, supplied input, snapshots and report stay
in the coursework archive.

## Local follow-up

Both saved C implementations were rebuilt using the same Apple Clang command,
with `-std=gnu17 -O3 -ffp-contract=off`. Each used the same archived 4,096-particle
input, identical to the teaching input. The common driver was changed in
temporary copies to call the update routine once per process. The submitted
routine frees a coefficient buffer on return and remembers the last timestep.
A later call with the same timestep can allocate a new buffer and skip
initialising it. Using one call controls for that defect.

One preliminary 20-step run per implementation preceded five measured pairs.
Each sample used a fresh process. The order alternated by pair. The timed
region surrounds the entire update call and excludes input loading and snapshot
writing. It includes allocations, memory first touches, timer calls and the
progress output of each implementation. The common driver still allocates
the original workspace for both versions. The measurements do not isolate the
effect of tiling, compiler vectorisation or any single transformation.

The output check compares particle fields at the same step. It reports maximum
absolute coordinate and velocity differences in the serialized snapshots,
which use eight fractional digits in scientific notation. It also checks
finiteness and compares final collision counts. The local 100-step runs are
a separate numerical check and do not contribute to the runtime medians.

## Acknowledgement

The historical optimisation study used the Cirrus HPC service at EPCC.
[Cirrus service documentation](https://docs.cirrus.ac.uk/user-guide/introduction/#acknowledging-cirrus)
