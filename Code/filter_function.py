import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import ScalarFormatter
from IPython.display import display, HTML


import pandas as pd

def apply_filters(
    df,
    mission=None,
    date_min=None, date_max=None,
    kp=None,
    st_type=None,
    Teff_min=None, Teff_max=None,
    rade_min=None, rade_max=None,
    rade_err=None,
    mass_min=None, mass_max=None,
    mass_err=None,
    density_min=None, density_max=None,
    P=None,
    b=None
):
    df_filtered = df.copy()

    # -------------------- DISCOVERY FILTERS --------------------
    if mission is not None:
        df_filtered = df_filtered[
            df_filtered['disc_facility'].notna() &
            (df_filtered['disc_facility'] == mission)
        ]

    if date_min is not None:
        df_filtered = df_filtered[
            df_filtered['disc_year'].notna() &
            (df_filtered['disc_year'] > date_min)
        ]

    if date_max is not None:
        df_filtered = df_filtered[
            df_filtered['disc_year'].notna() &
            (df_filtered['disc_year'] < date_max)
        ]

    if kp is not None:
        df_filtered = df_filtered[
            df_filtered['sy_kepmag'].notna() &
            (df_filtered['sy_kepmag'] < kp)
        ]

    # -------------------- STELLAR FILTERS --------------------
    if st_type is not None:
        df_filtered = df_filtered[
            df_filtered['st_spectype'].fillna('').str.startswith(st_type)
        ]

    if Teff_min is not None:
        df_filtered = df_filtered[
            df_filtered['st_teff'].notna() &
            (df_filtered['st_teff'] > Teff_min)
        ]

    if Teff_max is not None:
        df_filtered = df_filtered[
            df_filtered['st_teff'].notna() &
            (df_filtered['st_teff'] < Teff_max)
        ]

    # -------------------- PLANETARY FILTERS --------------------
    if rade_min is not None:
        df_filtered = df_filtered[
            df_filtered['pl_rade'].notna() &
            (df_filtered['pl_rade'] > rade_min)
        ]

    if rade_max is not None:
        df_filtered = df_filtered[
            df_filtered['pl_rade'].notna() &
            (df_filtered['pl_rade'] < rade_max)
        ]

    if rade_err is not None:
        mask = (
            df_filtered['pl_rade'].notna() &
            df_filtered['pl_radeerr1'].notna() &
            df_filtered['pl_radeerr2'].notna()
        )
        rade_error = df_filtered[['pl_radeerr1', 'pl_radeerr2']].max(axis=1)
        snr = rade_error / df_filtered['pl_rade']
        df_filtered = df_filtered[mask & (snr < rade_err)]

    if mass_min is not None:
        df_filtered = df_filtered[
            df_filtered['pl_bmasse'].notna() &
            (df_filtered['pl_bmasse'] > mass_min)
        ]

    if mass_max is not None:
        df_filtered = df_filtered[
            df_filtered['pl_bmasse'].notna() &
            (df_filtered['pl_bmasse'] < mass_max)
        ]

    if mass_err is not None:
        mask = (
            df_filtered['pl_bmasse'].notna() &
            df_filtered['pl_bmasseerr1'].notna() &
            df_filtered['pl_bmasseerr2'].notna()
        )
        mass_error = df_filtered[['pl_bmasseerr1', 'pl_bmasseerr2']].max(axis=1)
        snr = mass_error / df_filtered['pl_bmasse'] 
        df_filtered = df_filtered[mask & (snr < mass_err)]

    if density_min is not None:
        df_filtered = df_filtered[
            df_filtered['pl_dens'].notna() &
            (df_filtered['pl_dens'] > density_min)
        ]

    if density_max is not None:
        df_filtered = df_filtered[
            df_filtered['pl_dens'].notna() &
            (df_filtered['pl_dens'] < density_max)
        ]

    if P is not None:
        df_filtered = df_filtered[
            df_filtered['pl_orbper'].notna() &
            (df_filtered['pl_orbper'] < P)
        ]

    if b is not None:
        df_filtered = df_filtered[
            df_filtered['pl_imppar'].notna() &
            (df_filtered['pl_imppar'] < b)
        ]

    return df_filtered


#     if giant is not None:
#         threshold = temperature_dependent_stellar_filter(df_filtered)

#         ratio = df_filtered['st_rad'] / df_filtered['pl_rade']
#         if giant == True:
#             df_filtered = df_filtered[ratio <= threshold]
#         elif giant == False:
#             df_filtered = df_filtered[ratio > threshold]

# def temperature_dependent_stellar_filter(df, p=0.00025, C=0.20):
#     Teff = df['st_teff']
#     K    = df['pl_eqt']
#     return 10**( p * ( Teff / (1 - 5500) ) + C )



def display_table(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    display(HTML(
        "<div style='height: 300px; overflow: auto; width: fit-content;'>"
        + df.to_html()
        + "</div>"
    ))





def plot_sample_stellar_radi_vs_teff(df, df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        df['st_teff'], df['st_rad'],
        color="#CECECE", alpha=0.6, s=25, zorder=1,
        label="All Stars"
    )

    ax.scatter(
        df_filtered['st_teff'], df_filtered['st_rad'],
        c="#3D2490", edgecolors="#363535", s=25, zorder=2,
        label="Filtered Stars"
    )

    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.invert_xaxis()

    ax.set_xlabel("Stellar Effective Temperature (K)")
    ax.set_ylabel("Stellar Radius ($R_{\\odot}$)")
    ax.legend()

    plt.tight_layout()
    plt.show()




def plot_radii_vs_mass_Mtype(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        df_filtered['pl_bmasse'], df_filtered['pl_rade'],
        c=df_filtered['pl_eqt'], cmap='plasma', s=25, zorder=1,
        label="Planets"
    )

    cbar = plt.colorbar(scatter, ax=ax)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel("Planet Mass ($M_{\\oplus}$)")
    ax.set_ylabel("Planet Radius ($R_{\\oplus}$)")
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_histogram(df_filtered):
    fig, ax = plt.subplots(figsize=(10,6))

    ax.hist(
        df_filtered['pl_rade'], bins=200
    )

    ax.set_xlabel("Planet Radius ($R_{\\oplus}$)")
    ax.set_ylabel("Number of Planets")
    ax.legend()

    plt.tight_layout()
    plt.show()


