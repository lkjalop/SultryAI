import pytest
from sultrytai.catalog import FactorCatalog

def test_catalog_load_indexed():
    c = FactorCatalog()
    # index.json is present in the repo after split; load should succeed
    c.load()
    assert hasattr(c, 'factors')
    assert isinstance(c.factors, list)
    # basic sanity: expect > 0 factors
    assert len(c.factors) > 0
