import numpy as np
from PIL import Image


class Renderer:
    #def __init__(self,theta=1.570796,scale_x=-1,scale_y=-1,scale_z=0.5,center=(200,200)):
    def __init__(self,theta,scale_x,scale_y,scale_z,center=(0,0):
        self.theta = theta # Y Rotation
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z
        self.center = center
    def project_2d(self,X):
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
        [[np.cos(self.theta), 0,np.sin(self.theta)], #
        [0, 1, 0],
        [-1*np.sin(self.theta), 0, np.cos(self.theta)]]
      )

      # Transformation matrix, maps X into a 2d vector
      # Negatives apparently flip it (making it right side up in this case)
      V = np.array(
        [[self.scale_x, 0, self.scale_z*np.sqrt(2)],
        [0, self.scale_y, self.scale_z*np.sqrt(2)]]
      )

      X = np.array([np.dot(R,X) for R in R_y])
      return ( self.center[0]+int(np.dot(V[0],X)),self.center[1]+int(np.dot(V[1],X)) )
