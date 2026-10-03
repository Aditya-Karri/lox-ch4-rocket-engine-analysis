"""
Preliminary LOX/CH4 rocket-engine performance, injector and
thermal screening model.
- This is a preliminary engineering study.
- CEA outputs are treated as the thermochemical reference.
- Injector and cooling calculations contain explicit screening assumptions.
- No hardware validation is claimed.
"""

import math

# CEA-selected design point
TARGET_THRUST_N = 20000.0
PC_PA = 3000000.0       # Chamber pressure [pascal]
OF = 3.0                # Oxidizer-to-fuel mass ratio
EXPANSION_RATIO = 10.0  # Nozzle expansion ratio = exit area / throat area 

TC_K = 3373.82          # CEA chamber temperature [kelvin]
GAMMA_C = 1.1345        # Ratio of specific heats (gamma) at the CEA chamber condition
MW_C_KG_KMOL = 20.265   # Molecular weight of the CEA chamber gas [kg/kmol]
CSTAR_MPS = 1851.6      # Characteristic velocity c* from CEA [m/s]
CF = 1.6357             # Thrust coefficient Cf from CEA

# Engine sizing
AT_M2 = TARGET_THRUST_N / (CF * PC_PA)  # Throat area [m^2]
DT_M = math.sqrt(4 * AT_M2 / math.pi)   # Throat diameter [m]

AE_M2 = EXPANSION_RATIO * AT_M2         # Nozzle exit area [m^2]
DE_M = math.sqrt(4 * AE_M2 / math.pi)   # nozzle exit diameter [m]

MDOT_KG_S = PC_PA * AT_M2 / CSTAR_MPS # Total propellant mass flow rate [kg/s]
MDOT_FUEL_KG_S = MDOT_KG_S / (1 + OF) # Fuel mass flow rate [kg/s]
MDOT_OX_KG_S = OF * MDOT_FUEL_KG_S # Oxidizer mass flow rate [kg/s]

# Injector screening assumptions
DP_INJ_PA = 0.20 * PC_PA    # Assumed injector pressure drop [Pa]
CD = 0.80                   # Assumed injector discharge coefficient
RHO_LOX = 1141.0            # Assumed LOX [kg/m^3] for preliminary injector sizing
RHO_CH4 = 422.0             # Assumed liquid methane density [kg/m^3] for preliminary injector sizing

A_LOX_M2 = MDOT_OX_KG_S / (CD * math.sqrt(2 * RHO_LOX * DP_INJ_PA)) # Total effective LOX injector flow area [m^2]
A_CH4_M2 = MDOT_FUEL_KG_S / (CD * math.sqrt(2 * RHO_CH4 * DP_INJ_PA)) # Total effective methane injector flow area [m^2]

#   Thermal screening assumptions
T_THROAT_K = 3200.33    # CEA throat static temperature [K]
GAMMA_THROAT = 1.1340   # Ratio of specific heats at the throat from CEA
PR_THROAT = 0.5028      # Prandtl number at the throat from CEA
RECOVERY_FACTOR = PR_THROAT ** (1 / 3) # Approximate recovery factor for turbulent flow
TAW_K = T_THROAT_K * (
    1 + RECOVERY_FACTOR * (GAMMA_THROAT - 1) / 2
) # Estimated adiabatic/recovery wall temperature at the throat [K]

HG_W_M2K = 26300.0  # Estimated hot-gas-side heat-transfer coefficient [W/(m^2 K)]
HC_W_M2K = 60000.0  # Estimated coolant-side heat-transfer coefficient [W/(m^2 K)]
WALL_THICKNESS_M = 0.0015   # Assumed chamber wall thickness = 1.5 mm
WALL_K_W_MK = 300.0         # Assumed wall thermal conductivity [W/(m K)]
COOLANT_BULK_T_K = 400.0    # Assumed local bulk coolant temperature [K]

R_THERMAL = (
    1/HG_W_M2K
    + WALL_THICKNESS_M/WALL_K_W_MK
    + 1/HC_W_M2K
) # Total thermal resistance [m^2 K/W]

QFLUX_W_M2 = (TAW_K - COOLANT_BULK_T_K) / R_THERMAL # Estimated throat heat flux [W/m^2]
T_WALL_HOT_K = TAW_K - QFLUX_W_M2 / HG_W_M2K        # Estimated hot-gas-side wall temperature [K]
T_WALL_COLD_K = T_WALL_HOT_K - QFLUX_W_M2 * WALL_THICKNESS_M / WALL_K_W_MK # Estimated coolant-side wall temperature [K]
 
# Report
print("PRELIMINARY LOX/CH4 ENGINE")
print(f"Target thrust          : {TARGET_THRUST_N/1000:.2f} kN")
print(f"Chamber pressure       : {PC_PA/1e5:.1f} bar")
print(f"O/F                    : {OF:.2f}")
print(f"Expansion ratio        : {EXPANSION_RATIO:.1f}")
print(f"Throat diameter        : {DT_M*1000:.2f} mm")
print(f"Exit diameter          : {DE_M*1000:.2f} mm")
print(f"Total mass flow        : {MDOT_KG_S:.3f} kg/s")
print(f"CH4 mass flow          : {MDOT_FUEL_KG_S:.3f} kg/s")
print(f"LOX mass flow          : {MDOT_OX_KG_S:.3f} kg/s")
print(f"LOX injector area      : {A_LOX_M2*1e6:.1f} mm^2")
print(f"CH4 injector area      : {A_CH4_M2*1e6:.1f} mm^2")
print(f"Screening heat flux    : {QFLUX_W_M2/1e6:.2f} MW/m^2")
print(f"Hot-side wall temp     : {T_WALL_HOT_K:.0f} K")
print(f"Coolant-side wall temp : {T_WALL_COLD_K:.0f} K")
