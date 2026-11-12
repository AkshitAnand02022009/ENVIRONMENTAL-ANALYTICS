import math

# ==============================================================================
# 1. HISTORICAL DATA (1980 - 2024) TO BUILD THE CONVERSION FORMULA
# ==============================================================================
temp_celsius = [
    0.26,
    0.32,
    0.14,
    0.31,
    0.16,
    0.12,
    0.18,
    0.32,
    0.39,
    0.27,
    0.45,
    0.41,
    0.22,
    0.23,
    0.32,
    0.45,
    0.33,
    0.46,
    0.61,
    0.38,
    0.39,
    0.53,
    0.63,
    0.62,
    0.53,
    0.68,
    0.64,
    0.66,
    0.54,
    0.66,
    0.72,
    0.61,
    0.65,
    0.68,
    0.75,
    0.90,
    1.01,
    0.92,
    0.85,
    0.98,
    1.01,
    0.85,
    0.89,
    1.17,
    1.28,
]

water_level_mm = [
    0.0,
    3.1,
    1.5,
    4.8,
    3.9,
    5.2,
    6.4,
    8.9,
    11.2,
    12.5,
    15.8,
    17.1,
    16.0,
    18.2,
    21.0,
    24.3,
    25.8,
    28.5,
    33.1,
    32.0,
    35.4,
    39.2,
    43.5,
    46.1,
    48.0,
    52.4,
    55.1,
    58.3,
    59.8,
    63.5,
    67.2,
    68.0,
    72.4,
    76.1,
    80.5,
    85.8,
    91.2,
    94.0,
    97.5,
    102.1,
    106.4,
    108.2,
    112.5,
    118.9,
    124.5,
]

# Calculate Correlation (r) and Linear Formula: Water_Level = (m * Temp_C) + c
n = len(temp_celsius)
mean_x = sum(temp_celsius) / n
mean_y = sum(water_level_mm) / n

numerator = sum(
    (x - mean_x) * (y - mean_y) for x, y in zip(temp_celsius, water_level_mm)
)
denom_x = sum((x - mean_x) ** 2 for x in temp_celsius)
denom_y = sum((y - mean_y) ** 2 for y in water_level_mm)

correlation = numerator / math.sqrt(denom_x * denom_y)
slope = numerator / denom_x
intercept = mean_y - (slope * mean_x)


# ==============================================================================
# 2. CONVERSION FORMULAS
# ==============================================================================
def predict_water_level(temp_c):
  """Formula 1: Total Expected Water Level Rise (mm) from Temp (C)"""
  return max(0.0, (slope * temp_c) + intercept)


def thermal_expansion_only(temp_c):
  """Formula 2: Water expansion due to heat alone (dH = H0 * B * dT)"""
  H0_mm = 3688000  # Average ocean depth in mm
  beta = 0.00021  # Thermal expansion coefficient of water per C
  return max(0.0, H0_mm * beta * temp_c)


# ==============================================================================
# 3. INTERACTIVE USER INPUT & LIVE CALCULATION
# ==============================================================================
print("==========================================================")
print("   TEMPERATURE TO WATER LEVEL & FRESHWATER CALCULATOR")
print("==========================================================")
print(f"Historical Correlation (Temp vs Water Level): r = {correlation:.4f}")
print(
    f"Derived Formula: Water Level (mm) = ({slope:.2f} x Temp_C) +"
    f" ({intercept:.2f})\n"
)

user_temp = float(
    input("Enter temperature rise in Celsius (e.g., 1.5, 2.0, 3.5): ")
)

expected_wl_mm = predict_water_level(user_temp)
expected_wl_cm = expected_wl_mm / 10.0
expansion_mm = thermal_expansion_only(user_temp)
ice_melt_mm = max(0.0, expected_wl_mm - expansion_mm)

# ==============================================================================
# 4. REMAINING WATER BREAKDOWN (SALT VS FRESH) AFTER MELT
# ==============================================================================
total_earth_water_km3 = 1386000000
ocean_area_km2 = 361800000

saltwater_km3 = total_earth_water_km3 * 0.9750  # 97.50% Saltwater
glaciers_km3 = total_earth_water_km3 * 0.0172  # 1.72% Glaciers & Ice Caps
groundwater_km3 = total_earth_water_km3 * 0.0075  # 0.75% Groundwater
usable_fresh_km3 = total_earth_water_km3 * 0.0003  # 0.03% Rivers & Lakes
# Formula 3: Convert Ice-Melt Sea Rise (mm) -> Volume of Melted Glacier Ice (km3)
melted_ice_km3 = (ice_melt_mm / 1000000) * ocean_area_km2

new_glaciers_km3 = max(0.0, glaciers_km3 - melted_ice_km3)
new_saltwater_km3 = saltwater_km3 + melted_ice_km3
total_fresh_left_km3 = new_glaciers_km3 + groundwater_km3 + usable_fresh_km3

print("\n==========================================================")
print(f"RESULTS FOR +{user_temp} C TEMPERATURE INCREASE")
print("==========================================================")
print(
    f"1. Expected Water Level Rise:   {expected_wl_mm:.2f} mm"
    f" ({expected_wl_cm:.2f} cm)"
)
print(
    f"   - From Thermal Expansion:    {expansion_mm:.2f} mm (dH = H0 x B x dT)"
)
print(f"   - From Glacier Ice Melting:  {ice_melt_mm:.2f} mm")

print("\n2. Updated Earth Water Breakdown (Saltwater vs. Freshwater):")
print(
    f"   - Saltwater (Oceans):        {new_saltwater_km3:,.0f} km3"
    f" ({(new_saltwater_km3/total_earth_water_km3)*100:.4f}%)"
)
print(
    f"   - Total Freshwater Left:     {total_fresh_left_km3:,.0f} km3"
    f" ({(total_fresh_left_km3/total_earth_water_km3)*100:.4f}%)"
)
print(
    f"     * Glaciers & Ice Left:     {new_glaciers_km3:,.0f} km3"
    f" (-{melted_ice_km3:,.0f} km3 melted)"
)
print(f"     * Groundwater Left:        {groundwater_km3:,.0f} km3 (0.7500%)")
print(
    f"     * Usable Rivers & Lakes:   {usable_fresh_km3:,.0f} km3 (0.0300%)"
)
print("==========================================================")
