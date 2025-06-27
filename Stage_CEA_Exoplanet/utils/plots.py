# Required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from IPython.display import display, HTML
import numpy as np



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

    # Scatter plot with color mapped to equilibrium temperature
    scatter = ax.scatter(
        df_filtered['pl_bmasse'], df_filtered['pl_rade'],
        c=df_filtered['pl_eqt'], cmap='plasma', s=25, zorder=1,
        label="Planets"
    )

    # Add colorbar indicating equilibrium temperature
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Equilibrium Temperature (K)")

    x = np.array([
    2.2233, 2.7682, 3.4297, 4.2296,
    5.1932, 6.3505, 7.7363, 9.3912, 11.3628, 13.7066, 16.4870, 19.7797,
    23.6585, 28.152, 33.3138, 39.2487, 46.0693, 53.8965, 62.8692, 73.1339,
    84.8337, 98.1197, 113.1545, 130.1162, 149.2054, 170.6534
    ])
    y = np.array([
        1.2485, 1.3245, 1.4019, 1.4806,
        1.5604, 1.6412, 1.7228, 1.8052, 1.8883, 1.9719, 2.0559, 2.1404, 2.2246,
        2.3063, 2.3848, 2.4602, 2.5325, 2.6019, 2.6683, 2.7319, 2.7924, 2.8497,
        2.9034, 2.9536, 3.0002, 3.0431
    ])

    xx = [
        0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 8.0,
        10.0, 12.0, 16.0, 20.0, 32.0, 64.0
    ]

        # Radii (in Earth radii)
    yy = [
        1.232, 1.302, 1.392, 1.512, 1.609, 1.762, 1.881, 1.981, 2.205,
        2.319, 2.415, 2.571, 2.696, 2.963, 3.34
    ]

    plt.plot(xx, yy, linestyle='-', color='blue', label='50%H2O')
    plt.legend()

        # Plot
    plt.plot(x, y, linestyle='-', color='green', label='earth like')
    plt.title('Linear Plot of Given Data')
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
def plot_density_vs_mass_Mtype(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot filtered stars on top in a distinct color
    ax.scatter(
        df_filtered['pl_bmasse'], df_filtered['pl_dens']/4.79,
        c="#3D2490", edgecolors="#363535", s=25, zorder=2,
        label="Filtered planets"
    )


    # Log scale for radius, reverse x-axis for HR-diagram convention
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    
    ax.set_xlabel("Mass ($M_{\\oplus}$)")
    ax.set_ylabel("($\\rho/\\rho_{\\oplus}$)")
    ax.legend()

    plt.tight_layout()
    plt.show()




# ------------------------------------------------------------------------------
# Plot histogram of planet density/earth density in the filtered dataset.
# ------------------------------------------------------------------------------
def plot_histogram_density_Mtype(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram of planetary radii
    ax.hist(
        df_filtered['pl_dens']/4.79, bins=20, color='steelblue', edgecolor='black'
    )

    ax.set_xlabel("($\\rho/\\rho_{\\oplus}$)")
    ax.set_ylabel("Number of Planets")
    ax.set_title("Distribution of Planet ($\\rho/\\rho_{\\oplus}$)")

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
