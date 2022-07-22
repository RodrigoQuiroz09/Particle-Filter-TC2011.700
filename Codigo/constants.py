import numpy as np

PARTICLES = 500
SPEED = 0.4
POSITION_CHANGE = .85
VELOCITY_CHANGE = 0.4
change_tuple = (PARTICLES, 1)
WALKING_DEFAULT = np.array((156,74,38))
TERMO_DEFAULT = np.array((105,134,65))
CONCAT = np.array((WALKING_DEFAULT,TERMO_DEFAULT))
TEST_VIDEOS=("walking.mp4","GreenBottle.mp4")