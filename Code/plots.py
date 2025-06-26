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