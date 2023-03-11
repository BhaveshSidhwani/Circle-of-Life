
import predator as pred
import prey


# Constants for graph
START = 0
SIZE = 50
GRAPH = {}

# Constants for game characters
AGENT_POS = 0
PREDATOR_POS: pred.predator = None
PREY_POS: prey.prey = None

# Constants for data extraction
PREY_CAUGHT_NUM = 0
PRED_CAUGHT_NUM = 0
STEPS = 0
TIME_OUT_STEPS = 5000

# Function to reset the data constants after every execution
def reset_constants():
    AGENT_POS = 0
    PREDATOR_POS: pred.predator = None
    PREY_POS: prey.prey = None

    PREY_CAUGHT_NUM = 0
    PRED_CAUGHT_NUM = 0
    STEPS = 0
