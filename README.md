### Installation
Clone the repository, and move to the desired branch

    git clone https://github.com/jrzwrz/qcircuits-opt.git
    git checkout final

Create a virtual environment

    cd qcircuits-opt
    python -m venv venv
    source venv/bin/activate

Install the dependencies

    pip install -r requirements.txt

### Running the algorithm

If the Cayley graph is not created already, run:

    python generate_cayley_graph.py

The above generates a Cayley graph and stores it in a .pkl file, which is then loaded into the programme as and when required. 

To run the subroutine for small random circuits, run the following command;

    python shortest_path.py

To run the optimization subroutine for a bunch of random test cases, run the following command:

    python random_data.py

The data will be saved as `random_dat.pkl` for possible reloading and as `out.csv` in a human-readable format.

To perform the analysis for some known test cases, run the following command:

    python known_cases.py

The data will be saved as `ex_circuits.pkl` for possible reloading and as `ex_circuits.csv` in a human-readable format.
