from attitude.primitives import Primitive
import jax.numpy as jnp

class Quaternion(Primitive):
    """ quaternion rotation object. b0 is the scalar part and must 
        be the first element of the input tuple b. 
    """
    def __init__(self, b: jnp.ndarray) -> None:
        """

        Args:
            b (jnp.ndarray): 1x4 matrix of quaternion parameters. First component
                is the scalar component
        
        Attributes:
            b (jnp.ndarray): 1x4 matrix of quaternion parameters. First component
                is the scalar component
        """
        super().__init__()
        assert jnp.abs(jnp.linalg.norm(jnp.asarray(b)) - 1.) < 1e-7, 'Elements of b must have unit length.'
        self.b = b
        self.dcm = self._build_quanterion(b)

    
    def _build_quanterion(self, b: jnp.ndarray) -> jnp.ndarray:
        """ Builds dcm from quaternion parameters. 

        Args:
            b (jnp.ndarray): 1x4 matrix parameters. First component
                is the scalar component

        Returns:
            jnp.ndarray: dcm derived from buanternion parameters b. 
        """
        b0, b1, b2, b3 = b.tolist()

        return jnp.array(
            [[b0**2. + b1**2. - b2**2. - b3**2., 2. * (b1 * b2 + b0 * b3), 2. * (b1 * b3 - b0 * b2)],
            [2. * (b1 * b2 - b0 * b3), b0**2. - b1**2. + b2**2. - b3**2., 2. * (b2 * b3 + b0 * b1)],
            [2. * (b1 * b3 + b0 * b2), 2. * (b2 * b3 - b0 * b1), b0**2. - b1**2. - b2**2. + b3**2.]]
        )
    
    def get_PVR_from_b(self) -> tuple: 
        """ Generates PVR directly from b.

        Returns:
            tuple: sclar phi and 3x1 matrix e.
        """
        theta = 2. * jnp.arccos(self.b[0])
        e = jnp.array(
            [[self.b[1] / jnp.sin(theta)],
             [self.b[2] / jnp.sin(theta)],
             [self.b[3] / jnp.sin(theta)]]
        )
        return theta, e
    
    def get_q_from_b(self) -> jnp.ndarray:
        """ Generates CRP q vector from b.

        Returns:
            jnp.ndarray: 3x1 matrix of CRP q parameters.
        """
        return jnp.array(
            [self.b[1] / self.b[0],
             self.b[2] / self.b[0],
             self.b[3] / self.b[0]]
        )
    
    def get_s_from_b(self) -> jnp.ndarray:
        """ Generate MRP s vector from b.

        Returns:
            jnp.ndarray: 3x1 matrix of MRP s parameters.
        """
        return jnp.array(
            [self.b[1] / (1. + self.b[0]),
             self.b[2] / (1. + self.b[0]),
             self.b[3] / (1. + self.b[0])]
        )

