"""
surface_kmc.py

Rejection-free Kinetic Monte Carlo (KMC) simulation of one-dimensional
surface growth by molecular deposition and edge diffusion.

Model summary
-------------
The surface is discretised into N lattice sites with periodic boundary
conditions. The state is an array of integer heights h_i.

Two types of events are possible:
  1. Deposition at site i:            h_i -> h_i + 1          (rate rd)
  2. Diffusion from site i to a
     nearest neighbour j = i-1 or i+1: h_i -> h_i-1, h_j -> h_j+1
     Only allowed if h_i >= h_j + 1 (horizontal or downhill move).
     - horizontal (h_i == h_j + 1):  rate ra = nu * exp(-Ea)
     - downhill   (h_i >  h_j + 1):  rate rs = nu * exp(-Es)

At every step, the full list of currently enabled events and their rates
is built, the total rate R is computed, one event is selected with
probability proportional to its rate, and the simulation clock is
advanced by an exponentially distributed waiting time Delta t = -ln(u)/R.
This is the "rejection-free" (n-fold way / Gillespie direct) algorithm:
every sampled event is guaranteed to occur, so no proposals are wasted.
"""

import numpy as np


def build_event_list(heights, N, rd, ra, rs):
    """
    Builds the list of all events enabled in the current configuration.

    Returns
    -------
    events : list of tuples
        ('dep', i)        -> deposition at site i
        ('diff', i, j)     -> particle at site i moves to neighbour j
    rates : np.ndarray
        Rate associated with each event, same order as `events`.
    """
    events = []
    rates = []

    # deposition is always possible at every site
    for i in range(N):
        events.append(('dep', i))
        rates.append(rd)

    # diffusion: only the top particle of a column may move, and only
    # horizontally or downhill (h_i >= h_j + 1)
    for i in range(N):
        hi = heights[i]
        for j in ((i - 1) % N, (i + 1) % N):
            hj = heights[j]
            if hi >= hj + 1:
                if hi == hj + 1:
                    rate = ra   # horizontal move
                else:
                    rate = rs   # downhill move
                events.append(('diff', i, j))
                rates.append(rate)

    return events, np.array(rates)


def select_event(rates, R, u1):
    """
    Selects one event index with probability proportional to its rate,
    using the cumulative-sum ("rate-weighted interval") method:
    finds alpha such that sum_{k<alpha} r_k < u1*R <= sum_{k<=alpha} r_k.
    """
    cumulative = np.cumsum(rates)
    target = u1 * R
    idx = np.searchsorted(cumulative, target, side="left")
    if idx >= len(rates):
        idx = len(rates) - 1
    return idx


def apply_event(heights, event):
    """Applies the selected event to the heights array, in place."""
    if event[0] == 'dep':
        _, i = event
        heights[i] += 1
    else:
        _, i, j = event
        heights[i] -= 1
        heights[j] += 1


def mean_height_and_roughness(heights):
    """
    Computes the mean surface height h_bar and the surface roughness
    W = sqrt(mean((h_i - h_bar)^2)).
    """
    mean_h = float(np.mean(heights))
    roughness = float(np.sqrt(np.mean((heights - mean_h) ** 2)))
    return mean_h, roughness


def run_kmc(N, rd, Ea, Es, nu, t_end, output_interval, seed):
    """
    Runs the rejection-free KMC simulation.

    Parameters
    ----------
    N : int                number of lattice sites
    rd : float              deposition rate per site
    Ea, Es : float           diffusion barriers (in units of kBT)
    nu : float               attempt frequency (prefactor)
    t_end : float            simulation end time
    output_interval : float  time spacing at which to record observables
    seed : int               random seed (for reproducibility)

    Returns
    -------
    time_series : list of dict  {time, mean_height, surface_roughness}
    final_state : dict          {time, mean_height, surface_roughness, heights}
    """
    rng = np.random.default_rng(seed)

    ra = nu * np.exp(-Ea)   # horizontal diffusion rate
    rs = nu * np.exp(-Es)   # downhill diffusion rate

    heights = np.zeros(N, dtype=np.int64)
    t = 0.0
    next_output = 0.0
    time_series = []

    while t < t_end:
        events, rates = build_event_list(heights, N, rd, ra, rs)
        R = rates.sum()

        u1 = rng.random()
        u2 = rng.random()

        idx = select_event(rates, R, u1)
        dt = -np.log(u2) / R
        t_new = t + dt

        # record the (most recent) configuration for every output time
        # crossed between t and t_new
        while next_output <= t_new and next_output <= t_end:
            mean_h, rough = mean_height_and_roughness(heights)
            time_series.append({
                "time": round(next_output, 6),
                "mean_height": mean_h,
                "surface_roughness": rough,
            })
            next_output += output_interval

        apply_event(heights, events[idx])
        t = t_new

    mean_h, rough = mean_height_and_roughness(heights)
    final_state = {
        "time": t,
        "mean_height": mean_h,
        "surface_roughness": rough,
        "heights": heights.tolist(),
    }

    return time_series, final_state
