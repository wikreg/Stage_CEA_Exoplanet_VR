# Required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from IPython.display import display, HTML




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
