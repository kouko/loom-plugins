"""Explicit experiment entry points; importing or preparing never invokes a model."""
import sys

if __name__=='__main__':
    if sys.argv[1]=='public-run':
        from public_runner import run_public
        run_public()
    else:
        from paired_experiment import prepare,run
        {'prepare':prepare,'run':run}[sys.argv[1]]()
