"""python -m src.engine.cli [stage|all]"""
from src.engine.pipeline.run import main
if __name__ == "__main__":
    raise SystemExit(main())
