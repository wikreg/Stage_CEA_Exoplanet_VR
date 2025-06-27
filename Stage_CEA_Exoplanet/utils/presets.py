import pandas as pd 
from utils.filters import apply_filters

df = pd.read_csv(
    r"C:\Users\vireg\Stage_CEA_Exoplanet_VR\Dataset\Confirmed_Data.csv", 
    comment='#'
    )
df.columns = df.columns.str.strip()




# ------------------------ STELLAR TYPE PRESETS ------------------------

def O_type():
    return apply_filters(df, st_type="O")

def B_type():
    return apply_filters(df, st_type="B")

def A_type():
    return apply_filters(df, st_type="A")

def F_type():
    return apply_filters(df, st_type="F")

def G_type():
    return apply_filters(df, st_type="G")

def K_type():
    return apply_filters(df, st_type="K")

def M_type():
    return apply_filters(df, st_type="M")

def L_type():
    return apply_filters(df, st_type="L")

def T_type():
    return apply_filters(df, st_type="T")

STELLAR_TYPE_PRESETS = {
    "O": O_type,
    "B": B_type,
    "A": A_type,
    "F": F_type,
    "G": G_type,
    "K": K_type,
    "M": M_type,
    "L": L_type,
    "T": T_type,
}




# ------------------------ MISSION PRESETS ------------------------

def filter_kepler():
    return apply_filters(df, mission="Kepler")

def filter_k2():
    return apply_filters(df, mission="K2")

def filter_tess():
    return apply_filters(df, mission="Transiting Exoplanet Survey Satellite (TESS)")

def filter_corot():
    return apply_filters(df, mission="CoRoT")

def filter_cheops():
    return apply_filters(df, mission="CHaracterising ExOPlanets Satellite (CHEOPS)")

def filter_jwst():
    return apply_filters(df, mission="James Webb Space Telescope (JWST)")

def filter_spitzer():
    return apply_filters(df, mission="Spitzer Space Telescope")

def filter_hubble():
    return apply_filters(df, mission="Hubble Space Telescope")

def filter_gaia():
    return apply_filters(df, mission="European Space Agency (ESA) Gaia Satellite")

def filter_wise():
    return apply_filters(df, mission="Wide-field Infrared Survey Explorer (WISE) Sat")

MISSION_PRESETS = {
    "Kepler": filter_kepler,
    "K2": filter_k2,
    "TESS": filter_tess,
    "CoRoT": filter_corot,
    "CHEOPS": filter_cheops,
    "JWST": filter_jwst,
    "Spitzer": filter_spitzer,
    "Hubble": filter_hubble,
    "Gaia": filter_gaia,
    "WISE": filter_wise,
}




# ------------------------ PAPER PRESETS ------------------------

def Fulton_2017():
    return apply_filters(df,
                         mission='Kepler', date_max=2017, kp=14.2,
                         Teff_min=4700, Teff_max=6500, Fulton_2017=True,
                         b=0.7
                         )

def Luque_Paille_2022():
    return apply_filters(df,
                         date_max=2022,
                         st_type='M',
                         rade_max=4, rade_err=0.08, mass_max=20,mass_err=0.25)

PAPER_PRESETS = {
    "Fulton_2017"      : Fulton_2017,
    "Luque_Paille_2022": Luque_Paille_2022
}