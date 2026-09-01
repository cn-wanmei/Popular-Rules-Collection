# Legacy migration boundary

The `legacy/migration/` tree is the only location permitted to contain
compatibility tooling for the retired 2.X data model or CLI shape.

Production execution must use `src.engine` exclusively.

The retired `scripts/normalize.py` and `scripts/v2fly_parser.py` are not
production pipeline components. Their V2Fly format parsing responsibility is
implemented by `src.engine.ingest.formats.v2fly`; record normalization is
implemented by `src.engine.ingest.normalizer` and the V3 canonical store.
