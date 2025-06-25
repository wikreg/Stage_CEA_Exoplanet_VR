def apply_filters(df, rade_max=None, date=None, ks=None, b=None, P=None, st_type=None, Teff_min=None, Teff_max=None, giant=None,):
    df_filtered = df.copy()

    if rade_max is not None:
        df_filtered = df_filtered[df_filtered['pl_rade'] < rade_max]

    if date is not None:
        df_filtered = df_filtered[df_filtered['disc_year'] < date]

    if ks is not None:
        df_filtered = df_filtered[df_filtered['sy_kmag'] < ks]

    if b is not None:
        df_filtered = df_filtered[df_filtered['pl_orbeccen'] < b]

    if P is not None:
        df_filtered = df_filtered[df_filtered['pl_orbper'] < P]

    if st_type is not None:
        df_filtered = df_filtered[df_filtered['st_spectype'].fillna('').str.startswith(st_type)]

    if Teff_min is not None:
        df_filtered = df_filtered[df_filtered['st_teff'] > Teff_min]

    if Teff_max is not None:
        df_filtered = df_filtered[df_filtered['st_teff'] < Teff_max]
        
    if giant is not None:
        threshold = temperature_dependent_stellar_filter(df_filtered)

        ratio = df_filtered['st_rad'] / df_filtered['pl_rade']
        if giant == True:
            df_filtered = df_filtered[ratio <= threshold]
        elif giant == False:
            df_filtered = df_filtered[ratio > threshold]

    return df_filtered

def temperature_dependent_stellar_filter(df, p=0.00025, C=0.20):
    Teff = df['st_teff']
    K    = df['pl_eqt']
    return 10**( p * ( Teff / (1 - 5500) ) + C )