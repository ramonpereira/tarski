# Tarksi ANTLR4 Parsers

Tarski uses [ANTLR4](http://www.antlr.org/) in order to parse `PDDL` and `FSTRIPS` problems.

## Using the parsers
In order to use the Tarski ANTLR-based parsers, you should just install the `antlr4-python3-runtime` Python package.
Development notes for the ANTLR Python target can be found
[here](https://github.com/antlr/antlr4/blob/master/doc/python-target.md).

## Generating the parsers
If you modify the grammar or for some other reason want to regenerate the parsers, you need to install the core ANTLR
Java packages into your local machine, as explained in [ANTLR4 website](http://www.antlr.org/).

Once that is done, you should be able to run the `build.py` script in the `${TARSKI_ROOT}/utils/parsers` directory. 
At the moment `PDDL` and `FSTRIPS` grammars are supported. 


