from sultrytai.catalog import FactorCatalog
import sys

def main():
    c = FactorCatalog()
    try:
        c.load()
    except Exception as e:
        print('Load error:', e)
        return 2
    errs = c.validate()
    if errs:
        for e in errs[:20]:
            print('ERROR:', e)
        print(f'Found {len(errs)} validation errors')
        return 3
    print('All factors validated OK, count=', len(c.factors))
    return 0

if __name__ == '__main__':
    sys.exit(main())
