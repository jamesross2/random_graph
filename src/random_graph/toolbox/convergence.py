"""Functions to help estimate convergence properties for various graph degree sequences"""

import typing
import warnings


def estimate_iterations(d: typing.Sequence[int], epsilon: float = 1e-3) -> int:
    """Estimate the number of iterations required so that the total variation distance is below epsilon.

    This function uses the big-O bounds for convergence as presented in the References, below.

    Args:
        d: The degree sequence of interest. Note that the provided convergence formulae use properties like mean degree
            and max degree, so small changes in degree sequence may have no impact on the required iterations.
        epsilon: The desired difference between the sampling distribution and the uniform distribution, measured using
            total variation distance. Smaller epsilon requires more iterations, by a factor of log(1 / epsilon).

    Returns:
        An integer, specifying the minimum number of iterations suggested. Note that this is a theoretical upper bound;
            the true number of iterations required may be much smaller.

    References:
        # TODO: find convergence formula references.
    """
    warnings.warn("Number of iterations currently estimated as a fixed constant.")
    return int(1e6)
