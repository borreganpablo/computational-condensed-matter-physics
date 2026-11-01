# Vibrational frequencies: minimum or transition state?

Harmonic vibrational frequencies computed with ORCA (B3LYP/def2-SVP) to classify stationary points. At a true minimum all frequencies are real. A first-order transition state has exactly one imaginary frequency, which corresponds to the direction of the reaction.

## H₂O: a true minimum

After geometry optimisation, all three normal modes have real frequencies, confirming a minimum.

| Mode | B3LYP/def2-SVP (cm⁻¹) | Exp. harmonic (cm⁻¹) |
| --- | --- | --- |
| Bending | 1638 | 1648 |
| Symmetric stretch | 3788 | 3832 |
| Antisymmetric stretch | 3882 | 3943 |

The computed frequencies lie within about 2 % of the experimental harmonic values.

## Linear H₃: the expected transition state

The symmetric linear H–H–H geometry (H–H = 0.90 Å, doublet, unrestricted) is the classic transition state of the exchange reaction H + H₂ → H₂ + H. It should show one imaginary frequency along the antisymmetric stretch.

| Mode | UB3LYP/def2-SVP (cm⁻¹) |
| --- | --- |
| Bending (×2, degenerate) | 435 |
| Antisymmetric stretch (central H moves, H + H₂ exchange direction) | 1601 |
| Symmetric stretch (outer H move, central H fixed) | 2336 |

**No imaginary frequency appears.** With B3LYP, the symmetric H₃ structure is a local minimum instead of a saddle point. This is a known failure of approximate density functionals: their self-interaction (delocalisation) error over-stabilises the three-centre radical, in which the unpaired electron is spread over all three atoms. That flattens or even removes the reaction barrier. Hartree–Fock, which has no self-interaction error, recovers the expected saddle point at this geometry.

The lesson is that a frequency calculation only classifies a structure correctly if the electronic-structure method describes that region of the potential energy surface well.

## Files

`*.xyz`: structures · `*.out`: full ORCA output, including the normal modes and thermochemistry.
