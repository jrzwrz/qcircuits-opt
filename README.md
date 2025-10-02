### Installation
Clone the repository

    git clone git@github.com:jrzwrz/qcircuits-opt.git

Create a virtual environment

    cd qcircuits-opt
    python -m venv venv
    source venv/bin/activate

Install the dependencies

    pip install -r requirements.txt

### Running the algorithm
First run

    python generate_cayley_graph.py

To generate the file with the Cayley Graph. Then run

    python shortest_path.py

To find the shortest path for a random test case.