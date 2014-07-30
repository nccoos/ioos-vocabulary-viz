ioos-vocabulary-viz
===================

This GUI is a demonstration of a dyanmic web tool (CGI) used to create SPARQL queries to MMI Ontology Registry and Repository (ORR) for the purpose of visualizing the IOOS Vocabulary terms and their mappings.  Being able to  is a key step in making registered vocabs on MMI ORR more useful. This demostration GUI lets users see and investigate vocabulary terms and their context based on simple skos mappings (exactMatch, closeMatch, narrowMatch and broadMatch) to other like terms or broader concepts.  

### Demonstration of orrviz.py

IOOS Parameter Vocabulary Visualizer [http://www.unc.edu/usr-bin/haines/orrviz.py](http://www.unc.edu/usr-bin/haines/orrviz.py)

### Running Demo Locally

* Clone the repo `git clone https://github.com/nccoos/ioos-vocabulary-viz.git`
* run `$ ./server.py` 
* open `orrviz.py` in your browser as [http://localhost:8010/orrviz.py](http://localhost:8010/orrviz.py)
