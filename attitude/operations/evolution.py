""" Simple attitude rate from body rate ODEs. 
"""
import jax.numpy as jnp
from jax import jit

@jit
def evolve_CRP(omega_dot: jnp.ndarray, q: jnp.ndarray) -> jnp.ndarray:
    """ Returns dq/dt given q(t) and omega_dot(t).

    Args:
        omega_dot (jnp.ndarray): Body angular rotation rates. 
        q (jnp.ndarray): 1x3 matrix of q parameteters.

    Returns:
        jnp.ndarray: dq/dt at time t.
    """
    in_shape = q.shape

    m = jnp.array(
        [[1. + q[0]**2., q[0] * q[1] - q[2], q[0] * q[2] + q[1]],
         [q[0] * q[1] + q[2], 1. + q[1]**2., q[1] * q[2] - q[0]],
         [q[0] * q[2] - q[1], q[1] * q[2] + q[0], 1. + q[2]**2.]]
    ) * 0.5
    return jnp.dot(m, omega_dot.reshape((3, 1))).reshape(in_shape)

@jit
def evolve_MRP(omega_dot: jnp.ndarray, s: jnp.ndarray) -> jnp.ndarray:
    """Returns ds/dt given s(t) and omega_dot(t).

    Args:
        omega_dot (jnp.ndarray): Body angular rotation rates. 
        s (jnp.ndarray): 1x3 matrix of s parameteters.

    Returns:
        jnp.ndarray: ds/dt at time t.
    """
    in_shape = s.shape
    dot_s = jnp.dot(s, s)
    m = jnp.array(
        [[1. - dot_s + 2. * s[0]**2., 2. * (s[0] * s[1] - s[2]), 2. * (s[0] * s[2] + s[1])],
         [2. * (s[0] * s[1] + s[2]), 1. - dot_s + 2. * s[1]**2., 2. * (s[1] * s[2] - s[0])], 
         [2. * (s[0] * s[2] - s[1]), 2. * (s[1] * s[2] + s[0]), 1. - dot_s + 2. * s[2]**2.]]
    ) * 0.25
    return jnp.dot(m, omega_dot.reshape((3, 1))).reshape(in_shape)

@jit
def evolve_quat(omega_dot: jnp.ndarray, b: jnp.ndarray) -> jnp.ndarray:
    """ Returns db/dt given b(t) and omega_dot(t).

    Args:
        omega_dot (jnp.ndarray): Body angular rotation rates. 
        b (jnp.ndarray): 1x4 matrix of b parameteters.

    Returns:
    jnp.ndarray: db/dt at time t.
    """
    # Append zero to omega_dot rate vector
    zero = jnp.zeros((1, 1))
    omega_dot4 = jnp.hstack([zero, omega_dot])
    in_shape = b.shape

    row1 = jnp.array([b[0], -b[1], -b[2], -b[3]])
    row2 = jnp.array([b[1], b[0], -b[3], b[2]])
    row3 = jnp.array([b[2], b[3], b[0], -b[1]])
    row4 = jnp.array([b[3], -b[2], b[1], b[0]])

    # |b|^2=1 at all times, so enforcing orthonormality is important.
    m = jnp.vstack(
        [row1 / jnp.linalg.norm(row1),
         row2 / jnp.linalg.norm(row2),
         row3 / jnp.linalg.norm(row3),
         row4 / jnp.linalg.norm(row4)]
    ) * 0.5
    return jnp.dot(m, omega_dot4.reshape((4, 1))).reshape(in_shape)
