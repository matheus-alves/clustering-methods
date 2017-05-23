# clustering-methods

Master's coursework containing python implementations for the EM and K-Means clustering algorithms

## Requirements

- Python 3.x

## Setup

To install the requirements simply run the following command:

    pip install -r requirements.txt
    
## Execution

To run this solution use the following command:

    python clustering.py DATA_FILE_PATH NUM_OF_ITERATIONS
    
Where DATA_FILE_PATH is the path to the data file (there is a sample at samples/data.txt)
and NUM_OF_ITERATIONS is an optional number of iterations and defaults to 10.

The data file is basically a series of coordinates in a matrix of the points to be classified between the *'red'* and *'blue'* classes.

The obtained results can be seen in the following files:

 - original_matrix.png : Presents the original matrix before the clustering process.
 - kmeans.png          : Presents the results of the K-means algorithm. 
 - em.png              : Presents the results of the EM algorithm.
