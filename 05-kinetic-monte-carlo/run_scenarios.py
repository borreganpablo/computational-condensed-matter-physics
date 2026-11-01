"""
run_scenarios.py

Runs the 5 required KMC scenarios (problem sheet, section II.C),
saves one JSON file per scenario, and produces all required plots.
"""

import numpy as np
from surface_kmc import run_kmc
from surface_analysis import (
    save_scenario_json, plot_mean_height, plot_roughness, plot_final_profiles
)

# ---- common parameters (section II.C) ----
N = 50
rd = 1.0
t_end = 100.0
output_interval = 1.0
seed = 12345
nu = 10.0          # attempt frequency, chosen so that barriers stay positive

# ---- scenario definitions ----
# Equal-barrier scenarios: Ea = Es = ln(nu / target_rate)
def equal_barrier_energy(target_rate):
    return float(np.log(nu / target_rate))

Ea1 = Es1 = equal_barrier_energy(0.1 * rd)   # scenario 1: rdiff/rd = 0.1
Ea2 = Es2 = equal_barrier_energy(1.0 * rd)   # scenario 2: rdiff/rd = 1.0
Ea3 = Es3 = equal_barrier_energy(2.0 * rd)   # scenario 3: rdiff/rd = 2.0

# Unequal-barrier scenarios (slow-diffusion regime, rdiff/rd = 0.1):
# keep the horizontal rate ra equal to the scenario-1 value (0.1*rd),
# and shift Es by +/-1 kBT to make downhill diffusion slower/faster
# than horizontal diffusion.
Ea4 = equal_barrier_energy(0.1 * rd)
Es4 = Ea4 + 1.0        # Es > Ea -> downhill slower than horizontal

Ea5 = equal_barrier_energy(0.1 * rd)
Es5 = Ea5 - 1.0        # Es < Ea -> downhill faster than horizontal

scenarios = [
    {
        "key": "eq_01",
        "name": "equal_barriers_diffusion_10_percent",
        "description": "Ea = Es; diffusion rate per site is 10% of the deposition rate",
        "Ea": Ea1, "Es": Es1, "ratio_label": "r_diff/r_d = 0.1 (Ea=Es)",
    },
    {
        "key": "eq_100",
        "name": "equal_barriers_diffusion_100_percent",
        "description": "Ea = Es; diffusion rate per site equals the deposition rate",
        "Ea": Ea2, "Es": Es2, "ratio_label": "r_diff/r_d = 1.0 (Ea=Es)",
    },
    {
        "key": "eq_200",
        "name": "equal_barriers_diffusion_200_percent",
        "description": "Ea = Es; diffusion rate per site is 200% of the deposition rate",
        "Ea": Ea3, "Es": Es3, "ratio_label": "r_diff/r_d = 2.0 (Ea=Es)",
    },
    {
        "key": "es_gt_ea",
        "name": "slow_diffusion_Es_greater_than_Ea",
        "description": "Es > Ea (downhill slower than horizontal); horizontal rate ra = 0.1*rd",
        "Ea": Ea4, "Es": Es4, "ratio_label": "r_diff/r_d = 0.1, Es>Ea",
    },
    {
        "key": "es_lt_ea",
        "name": "slow_diffusion_Es_less_than_Ea",
        "description": "Es < Ea (downhill faster than horizontal); horizontal rate ra = 0.1*rd",
        "Ea": Ea5, "Es": Es5, "ratio_label": "r_diff/r_d = 0.1, Es<Ea",
    },
]

results = {}

for sc in scenarios:
    Ea, Es = sc["Ea"], sc["Es"]
    ra = nu * np.exp(-Ea)
    rs = nu * np.exp(-Es)

    time_series, final_state = run_kmc(
        N=N, rd=rd, Ea=Ea, Es=Es, nu=nu,
        t_end=t_end, output_interval=output_interval, seed=seed,
    )

    parameters = {
        "number_of_sites": N,
        "Ea": Ea,
        "Es": Es,
        "attempt_frequency": nu,
        "deposition_rate_per_site": rd,
        "horizontal_diffusion_rate_ra": ra,
        "downhill_diffusion_rate_rs": rs,
        "temperature_units": "energies in kBT",
        "boundary_conditions": "periodic",
        "simulation_end_time": t_end,
        "output_interval": output_interval,
        "random_seed": seed,
    }

    save_scenario_json(
        f"./results/{sc['key']}.json",
        sc["name"], sc["description"], parameters, time_series, final_state,
    )

    results[sc["key"]] = {
        "label": sc["ratio_label"],
        "time_series": time_series,
        "final_state": final_state,
        "ra": ra, "rs": rs, "Ea": Ea, "Es": Es,
    }
    print(f"{sc['key']}: Ea={Ea:.4f} Es={Es:.4f} ra={ra:.4f} rs={rs:.4f}  "
          f"-> final mean_h={final_state['mean_height']:.3f}  "
          f"W={final_state['surface_roughness']:.3f}  steps recorded={len(time_series)}")

# ---- Plots: equal-barrier comparison (scenarios 1,2,3) ----
eq_scen = [
    (results["eq_01"]["label"], results["eq_01"]["time_series"]),
    (results["eq_100"]["label"], results["eq_100"]["time_series"]),
    (results["eq_200"]["label"], results["eq_200"]["time_series"]),
]
plot_mean_height(eq_scen, "./results/plot_mean_height_equal_barriers.png",
                  "Mean height vs time - equal diffusion barriers (Ea = Es)")
plot_roughness(eq_scen, "./results/plot_roughness_equal_barriers.png",
               "Surface roughness vs time - equal diffusion barriers (Ea = Es)")

eq_profiles = [
    (results["eq_01"]["label"], results["eq_01"]["final_state"]["heights"]),
    (results["eq_100"]["label"], results["eq_100"]["final_state"]["heights"]),
    (results["eq_200"]["label"], results["eq_200"]["final_state"]["heights"]),
]
plot_final_profiles(eq_profiles, "./results/plot_profile_equal_barriers.png",
                     "Final surface profile (t=100) - equal diffusion barriers")

# ---- Plots: unequal-barrier comparison (scenarios 1,4,5; all rdiff/rd=0.1) ----
uneq_scen = [
    ("Ea=Es (baseline)", results["eq_01"]["time_series"]),
    (results["es_gt_ea"]["label"], results["es_gt_ea"]["time_series"]),
    (results["es_lt_ea"]["label"], results["es_lt_ea"]["time_series"]),
]
plot_mean_height(uneq_scen, "./results/plot_mean_height_unequal_barriers.png",
                  "Mean height vs time - slow diffusion, Ea vs Es comparison")
plot_roughness(uneq_scen, "./results/plot_roughness_unequal_barriers.png",
               "Surface roughness vs time - slow diffusion, Ea vs Es comparison")

uneq_profiles = [
    ("Ea=Es (baseline)", results["eq_01"]["final_state"]["heights"]),
    (results["es_gt_ea"]["label"], results["es_gt_ea"]["final_state"]["heights"]),
    (results["es_lt_ea"]["label"], results["es_lt_ea"]["final_state"]["heights"]),
]
plot_final_profiles(uneq_profiles, "./results/plot_profile_unequal_barriers.png",
                     "Final surface profile (t=100) - slow diffusion, Ea vs Es comparison")

print("\nAll scenarios completed. JSON files and plots saved in ./")
