# Required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from IPython.display import display, HTML
import numpy as np
from scipy.interpolate import CubicSpline
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.stats import norm
import matplotlib.colors as mcolors


# ------------------------------------------------------------------------------
# Utility function to display a DataFrame in a scrollable table format.
# Useful for inspecting large tables in Jupyter notebooks or IPython environments.
# ------------------------------------------------------------------------------
def display_table(df):
    # Set display options to show all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Display the DataFrame in a scrollable box
    display(HTML(
        "<div style='height: 300px; overflow: auto; width: fit-content;'>"
        + df.to_html()
        + "</div>"
    ))




# ------------------------------------------------------------------------------
# Plot a Hertzsprung–Russell-like diagram: Stellar Radius vs Effective Temperature
# for all stars in the dataset and a filtered subset.
# ------------------------------------------------------------------------------
def plot_sample_stellar_radi_vs_teff(df, df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all stars in light gray
    ax.scatter(
        df['st_teff'], df['st_rad'],
        color="#CECECE", alpha=0.6, s=25, zorder=1,
        label="All Stars"
    )

    # Plot filtered stars on top in a distinct color
    ax.scatter(
        df_filtered['st_teff'], df_filtered['st_rad'],
        c="#3D2490", edgecolors="#363535", s=25, zorder=2,
        label="Filtered Stars"
    )

    # Log scale for radius, reverse x-axis for HR-diagram convention
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.invert_xaxis()

    ax.set_xlabel("Stellar Effective Temperature (K)")
    ax.set_ylabel("Stellar Radius ($R_{\\odot}$)")
    ax.legend()

    plt.tight_layout()
    plt.show()




# ------------------------------------------------------------------------------
# Plot Planetary Radius vs Mass for M-type stars, colored by equilibrium temperature.
# ------------------------------------------------------------------------------
def plot_radii_vs_mass_Mtype(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot with color mapped to equilibrium temperature
    scatter = ax.scatter(
        df_filtered['pl_bmasse'], df_filtered['pl_rade'],
        c=df_filtered['pl_eqt'], cmap='plasma', s=25, zorder=1,
        label="Planets"
    )

    # Add colorbar indicating equilibrium temperature
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Equilibrium Temperature (K)")

    

    # Log-log scaling for both axes
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter())

    ax.set_xlabel("Planet Mass ($M_{\\oplus}$)")
    ax.set_ylabel("Planet Radius ($R_{\\oplus}$)")
    ax.legend()

    plt.tight_layout()
    plt.show()




# ------------------------------------------------------------------------------
# Plot Planetary Radius vs Mass for M-type stars, colored by equilibrium temperature with comparaison.
# ------------------------------------------------------------------------------
def plot_radii_vs_mass_Mtype_comparaison(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    brown_to_yellow = LinearSegmentedColormap.from_list(
    'BrownYellow', ['saddlebrown', 'khaki'], N=256
    )

    # Scatter plot with color mapped to equilibrium temperature
    scatter = ax.scatter(
        df_filtered['pl_bmasse'], df_filtered['pl_rade'],edgecolors='black',linewidths=0.6,
        c=df_filtered['pl_eqt'], cmap=brown_to_yellow, s=25, zorder=2,
        label="Planets"
    )

    # Add colorbar indicating equilibrium temperature
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Equilibrium Temperature (K)")

    x = np.array([
        2.2233, 2.7682, 3.4297, 4.2296,
        5.1932, 6.3505, 7.7363, 9.3912, 11.3628, 13.7066, 16.4870
    ])
    y = np.array([
        1.2485, 1.3245, 1.4019, 1.4806,
        1.5604, 1.6412, 1.7228, 1.8052, 1.8883, 1.9719, 2.0559
    ])

    cs = CubicSpline(x, y, extrapolate=True)
    x_extended = np.logspace(np.log10(0.6), np.log10(16), 200)
    y_extended = cs(x_extended)

    xx = [
        0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 8.0,
        10.0, 12.0, 16.0
    ]

        # Radii (in Earth radii)
    yy = [
        1.232, 1.302, 1.392, 1.512, 1.609, 1.762, 1.881, 1.981, 2.205,
        2.319, 2.415, 2.571
    ]

    spline = CubicSpline(xx, yy, extrapolate=True)

    # Create new x range from 0 to 16
    xx_extended = np.logspace(np.log10(0.6), np.log10(16), 200)
    yy_extended = spline(xx_extended)

    plt.plot(xx_extended, yy_extended, linestyle='-', color='blue', label='50%H2O', zorder=1)
    plt.legend()

        # Plot
    plt.plot(x_extended, y_extended, linestyle='-', color='green', label='earth like', zorder=1)
    plt.legend()

    # Log-log scaling for both axes
    ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter())

    ax.set_xlabel("Planet Mass ($M_{\\oplus}$)")
    ax.set_ylabel("Planet Radius ($R_{\\oplus}$)")
    ax.legend()

    plt.tight_layout()
    plt.show()




# ------------------------------------------------------------------------------
# Plot Planetary density/earth density vs Mass for M-type stars.
# ------------------------------------------------------------------------------
def classify_planet(mass, density_ratio):
    earth_like = 1
    water_like = 2.11 / 4.79  # ~0.44
    mid_density = (earth_like + water_like) / 2  # ~0.72

    if density_ratio >= mid_density:
        return 'saddlebrown'      # Rocky (Earth-like)
    elif mass <= 6:
        return 'lightskyblue'     # Water world
    else:
        return 'darkblue'         # Sub-Neptune

def plot_density_vs_mass_Mtype(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    df_filtered['density_ratio'] = df_filtered['pl_dens'] / 4.79

    df_filtered['color'] = df_filtered.apply(
        lambda row: classify_planet(row['pl_bmasse'], row['density_ratio']),
        axis=1
    )

    scatter = ax.scatter(
        df_filtered['pl_bmasse'], df_filtered['density_ratio'],
        c=df_filtered['color'], edgecolors='black', s=25, zorder=2,
        label="Filtered planets"
    )

    # Add reference lines
    ax.axhline(y=1, color='green', linestyle='-', label='Earth-like', zorder=1, linewidth=1)
    ax.axhline(y=2.11/4.79, color='blue', linestyle='-', label='50% H₂O', zorder=1, linewidth=1)

    plt.axvline(x=2, color='lightskyblue', linestyle='--', linewidth=1)
    plt.axvline(x=6, color='lightskyblue', linestyle='--', linewidth=1)

    # Set log scale and labels
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel("Mass ($M_{\\oplus}$)")
    ax.set_ylabel("Density ($\\rho / \\rho_\\oplus$)")

    # Custom legend
    legend_elements = [
        Patch(facecolor='saddlebrown', edgecolor='black', label='Earth-like'),
        Patch(facecolor='lightskyblue', edgecolor='black', label='Water World'),
        Patch(facecolor='darkblue', edgecolor='black', label='Sub-Neptune'),
        Line2D([0], [0], color='green', lw=1, label='Earth density'),
        Line2D([0], [0], color='blue', lw=1, label='50% H₂O density')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()




# ------------------------------------------------------------------------------
# Plot histogram of planet density/earth density in the filtered dataset.
# ------------------------------------------------------------------------------
# Classification function based on mass and normalized density
def classify_planet(mass, density_ratio):
    mid_density = (1 + 2.11 / 4.79) / 2  # ~0.72

    if density_ratio >= mid_density:
        return 'saddlebrown'      # Earth-like
    elif mass <= 6:
        return 'lightskyblue'     # Water world
    else:
        return 'darkblue'         # Sub-Neptune

# Darken color helper
def darken_color(color, amount=0.6):
    """
    Darken a given matplotlib color by scaling RGB components.
    amount < 1 makes color darker.
    """
    c = np.array(mcolors.to_rgb(color))
    return c * amount

# Function to plot histogram bars with small gaps
def plot_histogram_with_gaps(data, bins, color='steelblue', ax=None, label=None):
    if ax is None:
        ax = plt.gca()

    counts, _ = np.histogram(data, bins=bins)
    bin_width = bins[1] - bins[0]
    bar_width = bin_width * 0.9  # 90% width to create gaps
    bin_centers = bins[:-1] + bin_width / 2

    ax.bar(bin_centers, counts, width=bar_width, color=color, edgecolor='black', label=label, align='center')

# Main plotting function with Gaussian fits and darker lines
def plot_histogram_density_Mtype_with_gauss(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calculate normalized density ratio
    df_filtered['density_ratio'] = df_filtered['pl_dens'] / 4.79

    # Classify planets
    df_filtered['category'] = df_filtered.apply(
        lambda row: classify_planet(row['pl_bmasse'], row['density_ratio']),
        axis=1
    )

    # Define bins once over entire dataset density_ratio range
    all_density = df_filtered['density_ratio']
    bins = np.linspace(all_density.min(), all_density.max(), 21)  # 20 bins

    # Colors and labels for categories
    categories = ['saddlebrown', 'lightskyblue', 'darkblue']
    labels = ['Earth-like', 'Water World', 'Sub-Neptune']

    # Plot histograms and Gaussian fits
    for color, label in zip(categories, labels):
        data = df_filtered[df_filtered['category'] == color]['density_ratio']
        if len(data) == 0:
            continue  

        plot_histogram_with_gaps(data, bins=bins, color=color, ax=ax, label=label)

        # Fit Gaussian
        mu, std = norm.fit(data)
        x = np.linspace(bins[0], bins[-1], 500)
        bin_width = bins[1] - bins[0]
        pdf = norm.pdf(x, mu, std) * len(data) * bin_width

        # Plot Gaussian PDF with darker color line
        dark_color = darken_color(color, amount=0.6)
        ax.plot(x, pdf, color=dark_color, linewidth=3, linestyle='-')

    ax.set_xlabel("Density ($\\rho / \\rho_\\oplus$)")
    ax.set_ylabel("Number of Planets")

    ax.legend()
    plt.tight_layout()
    plt.show()




# ------------------------------------------------------------------------------
# Plot histogram of planet radii in the filtered dataset.
# ------------------------------------------------------------------------------
def plot_histogram(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram of planetary radii
    ax.hist(
        df_filtered['pl_rade'], bins=200, color='steelblue', edgecolor='black'
    )

    ax.set_xlabel("Planet Radius ($R_{\\oplus}$)")
    ax.set_ylabel("Number of Planets")
    ax.set_title("Distribution of Planet Radii")

    plt.tight_layout()
    plt.show()
