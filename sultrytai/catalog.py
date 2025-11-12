import json
from pathlib import Path
from typing import List, Dict, Any
from jsonschema import validate, ValidationError

ROOT = Path(__file__).parent.parent
INDEX_PATH = ROOT / 'factors_catalog' / 'index.json'
SCHEMA_PATH = ROOT / 'schemas' / 'factor.schema.json'


class FactorCatalog:
    def __init__(self, index_path: Path = INDEX_PATH, schema_path: Path = SCHEMA_PATH):
        self.index_path = index_path
        self.schema_path = schema_path
        self.factors: List[Dict[str, Any]] = []

    def load(self) -> List[Dict[str, Any]]:
        if not self.index_path.exists():
            raise FileNotFoundError(f"Index not found: {self.index_path}")
        with self.index_path.open('r', encoding='utf-8') as f:
            index = json.load(f)
        all_factors = []
        for dom, info in index.items():
            path = self.index_path.parent / info.get('file')
            if not path.exists():
                raise FileNotFoundError(f"Domain file missing: {path}")
            with path.open('r', encoding='utf-8') as df:
                entries = json.load(df)
            all_factors.extend(entries)
        self.factors = all_factors
        return self.factors

    def validate(self) -> List[str]:
        errors = []
        if not self.schema_path.exists():
            errors.append(f'schema not found: {self.schema_path}')
            return errors
        schema = json.loads(self.schema_path.read_text(encoding='utf-8'))
        for i, f in enumerate(self.factors):
            try:
                validate(instance=f, schema=schema)
            except ValidationError as e:
                errors.append(f'factor[{i}] schema error: {e.message}')
        return errors

    def find_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        return [f for f in self.factors if f.get('domain') == domain]
