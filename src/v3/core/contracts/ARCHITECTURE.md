# V3 Architecture Contract

## Hard constraints
1. V3 does not import V2 scripts.* at runtime.
2. No legacy_body in V3 domain model.
3. Canonical Rule Store is the only rule body SSOT inside V3.
4. Entity Graph is DAG; Aggregate is a View, not a second body store.
5. Universal IR is the only client-agnostic intermediate representation.
6. Seven clients are Adapters over IR + Capability Contract.
7. Production cutover only after Full Differential + RC.
8. Rollback = Artifact rollback, not rebuild-from-V2.

## Pipeline order (mandatory)
Fetch → Snapshot → Validate → Normalize → Canonicalize →
Semantic → Hierarchy → View Resolve → Decision → IR →
Adapter → Golden → Artifact → Release Gate → Publish

## V2 role
- Legacy production until cutover
- Differential oracle
- Snapshot/data source via legacy_import
