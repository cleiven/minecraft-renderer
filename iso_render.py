import numpy as np
from PIL import Image

def project_2d(X,t=1.570796,f=-0.5,center=(0,0)):
  # Rotation matrices, rotate X before projecting:
  # https://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations
  X = np.asarray(X)

  #Z rotation matrix, unused
  #R_z = np.array(
    #[[np.cos(t), -1*np.sin(t), 0], #
    #[np.sin(t), np.cos(t), 0],
    #[0, 0, 1]]
  #)
  R_y = np.array(
    [[np.cos(t), 0,np.sin(t)], #
    [0, 1, 0],
    [-1*np.sin(t), 0, np.cos(t)]]
  )

  # Transformation matrix, maps X into a 2d vector
  # Negatives apparently flip it (making it right side up in this case)
  V = np.array(
    [[-1, 0, f*np.sqrt(2)],
    [0, -1, f*np.sqrt(2)]]
  )

  X = np.array([np.dot(R,X) for R in R_y])
  return ( center[0]+int(np.dot(V[0],X)),center[1]+int(np.dot(V[1],X)) )
