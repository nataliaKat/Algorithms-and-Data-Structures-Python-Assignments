# Network Destruction
The purpose of theese algorithms is to remove a number of nodes from a social network so that it is gradually decomposed. The first one is a simple approach removing the nodes with the largest number of neighbours. The second one is a bit more complex, as it decides which one to remove based on its "collective influence".

## Usage
```bash
python network_destruction.py [-c] [-r RADIUS] num_nodes input_file
```
where -c is given in order to run the first algorithm, -r followed by the radius is given for the second algorithm, num_nodes is the number of nodes to be removed and input_file is a file containing the graph. For more details visit https://nbviewer.jupyter.org/github/dmst-algorithms-course/assignment-2020-2/blob/master/assignment_2020_2.ipynb?flush_cache=true.
