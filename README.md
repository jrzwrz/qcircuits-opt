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
In order to run the algorithm, a gate set has to be defined in the `gate_maps.py` file. Inside the main function, you can
set the number of qubits and the target state. Once everything is set, just run:

    python main.py