##################################################################################
#   Francesco Carli
#
#   Title: Binomial Stock Price & Forward Price Simulation
#
#   Description: Simulates a multi-year daily stock price path using a binomial 
#             random walk and compares it against the theoretical forward 
#             price curve using the cost-of-carry model (F = S * e^(r*t)).
#
##################################################################################


import numpy as np
import matplotlib.pyplot as plt
import random as rd

# ----------------------------------------
# Definition
# ----------------------------------------
def Fprices(spot_price, annual_rate, time_to_maturity):
    #  F = S * e^(r * t)
    return spot_price * np.exp(annual_rate * time_to_maturity)

# -----------------------------------------
# CONSTANTS
# -----------------------------------------
r_step = 0.01       # Daily step volatility (+/- 1% per day)
R_annual = 0.05     # Annual risk-free interest rate (5% per year)

num_years = 3       # Total number of years to simulate
n = 365 * num_years # Total number of daily steps (e.g., 365 * 3 = 1095 days)
prob = 0.5          # Probability of an "up" day
S0 = 100            # Initial stock price
T_maturity = num_years # Forward contract maturity matches the total years
# -----------------------------------------

# -----------------------------------------
# Main
# -----------------------------------------


prices = [S0]
current_price = S0
forward_prices = [Fprices(S0, R_annual, T_maturity)] 

for i in range(1, n + 1):
    toss = rd.random()
    if toss < prob:
        current_price *= (1 + r_step)
    else:
        current_price *= (1 - r_step)

    prices.append(current_price)
    
    time_years = i / 365 
    
    # Time remaining until the contract matures
    time_to_maturity = T_maturity - time_years
    
    f_price = Fprices(current_price, R_annual, time_to_maturity)
    forward_prices.append(f_price)

# -----------------------------------------
# PLOT
# -----------------------------------------
plt.figure(figsize=(12, 6))
plt.xlabel('Days')
plt.ylabel('Stock Price ($S_t$)')
plt.title(f'Stock Price & Forward Price Simulation ({num_years} Years)')
plt.axhline(y=S0, color='r', linestyle='--', label='Initial Price (S_0)')


for year in range(1, num_years + 1):
    plt.axvline(x=year * 365, color='gray', linestyle='--', alpha=0.5)
    plt.text(year * 365, plt.ylim()[1] * 0.95, f'Year {year}', rotation=90, verticalalignment='top')

plt.plot(prices, label='Simulated Spot Price', color='blue', alpha=0.8)
plt.plot(forward_prices, label=f'Forward Price (to {num_years}-year maturity)', color='orange')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()