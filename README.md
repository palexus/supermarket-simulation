# supermarket-simulation.
This is a small Markov chain project. It is a simulation of a supermarket with 5 areas. We use a transition matrix to model the behavior in the supermarket which was calculated from a csv with customer data.

### How to use it?

Create a new python enviroment.

`conda create -n supermarket python=3.10`

`conda activate supermarket`

`pip install -r requirements.txt`

`python simulation.py`


The red dots represent customers. It is still not implemented to remove the dots if customers go the next area.
