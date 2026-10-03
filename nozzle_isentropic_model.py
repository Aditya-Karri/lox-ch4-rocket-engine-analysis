import numpy as np
from scipy.optimize import brentq

# INPUTS
Pc = 3.0e6          # Chamber pressure [Pa]
Tc = 3500.0         # Chamber temperature [K]
gamma = 1.20        # Ratio of specific heats [-]
R = 350.0           # Specific gas constant [J/(kg K)]

At = 0.01           # Throat area [m^2]
expansion_ratio = 20.0  # Ae / At [-]

Pa = 0      # Ambient pressure [Pa]

# GEOMETRY
Ae = expansion_ratio * At

# AREA-MACH RELATION
def area_mach(M, gamma):
    """Return A/A* for isentropic flow."""
    term1 = 1.0 / M
    term2 = 2.0 / (gamma + 1.0)
    term3 = 1.0 + (gamma - 1.0) / 2.0 * M**2

    exponent = (gamma + 1.0) / (2.0 * (gamma - 1.0))

    return term1 * (term2 * term3) ** exponent


# Solve for the supersonic exit Mach number
target_area_ratio = expansion_ratio

Me = brentq(
    lambda M: area_mach(M, gamma) - target_area_ratio,
    1.000001,
    20.0
)

# EXIT THERMODYNAMIC CONDITIONS
Te = Tc / (1.0 + (gamma - 1.0) / 2.0 * Me**2)

Pe = Pc * (
    1.0 + (gamma - 1.0) / 2.0 * Me**2
) ** (-gamma / (gamma - 1.0))

# EXIT VELOCITY
ae = np.sqrt(gamma * R * Te)
Ve = Me * ae

# CHOKED MASS FLOW
mdot = (
    Pc
    * At
    * np.sqrt(gamma / (R * Tc))
    * (2.0 / (gamma + 1.0))
    ** ((gamma + 1.0) / (2.0 * (gamma - 1.0)))
)

# THRUST
momentum_thrust = mdot * Ve

pressure_thrust = (Pe - Pa) * Ae

thrust = momentum_thrust + pressure_thrust

# SPECIFIC IMPULSE
g0 = 9.80665

Isp = thrust / (mdot * g0)

# OUTPUT
print("\nROCKET NOZZLE PERFORMANCE")

print(f"Chamber pressure       : {Pc/1e6:.3f} MPa")
print(f"Chamber temperature    : {Tc:.1f} K")
print(f"Throat area            : {At:.6f} m^2")
print(f"Exit area              : {Ae:.6f} m^2")
print(f"Expansion ratio        : {expansion_ratio:.2f}")

print(f"\nExit Mach number       : {Me:.3f}")
print(f"Exit temperature      : {Te:.1f} K")
print(f"Exit pressure         : {Pe/1000:.2f} kPa")
print(f"Exit velocity         : {Ve:.1f} m/s")

print(f"\nMass flow              : {mdot:.3f} kg/s")

print(f"\nMomentum thrust        : {momentum_thrust/1000:.3f} kN")
print(f"Pressure thrust        : {pressure_thrust/1000:.3f} kN")
print(f"Total thrust           : {thrust/1000:.3f} kN")

print(f"Specific impulse       : {Isp:.2f} s")