import pandas as pd

def load_data(type_of_data="normalized"):
    # From IPTG.csv and OC6.csv
    # Load IPTG data
    IPTG_data = pd.read_csv("Dat_for_Ayush/IPTG.csv")
    # Create exteded data
    mean_row = pd.DataFrame([IPTG_data.mean()], columns=IPTG_data.columns)
    std_row = pd.DataFrame([IPTG_data.std()], columns=IPTG_data.columns)
    IPTG_data_extended = pd.concat([IPTG_data, mean_row, std_row], ignore_index=True)
    IPTG_data_extended.index = ["replicate 1", "replicate 2", "replicate 3", "replicate 4", 
                        "replicate 5", "replicate 6", "mean", "std"]
    # Normalize each row by its last value
    IPTG_data_normalized = IPTG_data.div(IPTG_data.iloc[:, 0], axis=0)

    # Now, compute the mean and std rows for the normalized data
    mean_row = pd.DataFrame([IPTG_data_normalized.mean()], columns=IPTG_data_normalized.columns)
    std_row = pd.DataFrame([IPTG_data_normalized.std()], columns=IPTG_data_normalized.columns)

    # Concatenate the original DataFrame with the mean and std rows
    IPTG_data_normalized_extended = pd.concat([IPTG_data_normalized, mean_row, std_row], ignore_index=True)

    # rename rows
    IPTG_data_normalized_extended.index = ["replicate 1", "replicate 2", "replicate 3", "replicate 4", 
                        "replicate 5", "replicate 6", "mean", "std"]

    # Load IPTG 08_29 data (updated)
    IPTG_updated_df = pd.read_csv("IPTG_08_29.csv", delimiter=",", engine="python")
    # Create exteded data
    mean_row = pd.DataFrame([IPTG_updated_df.mean()], columns=IPTG_updated_df.columns)
    std_row = pd.DataFrame([IPTG_updated_df.std()], columns=IPTG_updated_df.columns)
    IPTG_updated_df_extended = pd.concat([IPTG_updated_df, mean_row, std_row], ignore_index=True)
    IPTG_updated_df_extended.index = ["replicate 1", "replicate 2", "replicate 3", "replicate 4", 
                        "replicate 5", "replicate 6", "mean", "std"]
    # Normalize each row by its last value
    IPTG_updated_df_normalized = IPTG_updated_df.div(IPTG_updated_df.iloc[:, -1], axis=0)

    # Now, compute the mean and std rows for the normalized data
    mean_row = pd.DataFrame([IPTG_updated_df_normalized.mean()], columns=IPTG_updated_df_normalized.columns)
    std_row = pd.DataFrame([IPTG_updated_df_normalized.std()], columns=IPTG_updated_df_normalized.columns)

    # Concatenate the original DataFrame with the mean and std rows
    IPTG_updated_df_normalized_extended = pd.concat([IPTG_updated_df_normalized, mean_row, std_row], ignore_index=True)

    # rename rows
    IPTG_updated_df_normalized_extended.index = ["replicate 1", "replicate 2", "replicate 3", "replicate 4",
                                                 "replicate 5", "replicate 6", "mean", "std"]
    # Load OC6 data
    OC6_data = pd.read_csv("Dat_for_Ayush/OC6.csv")
    # Create exteded data
    mean_row = pd.DataFrame([OC6_data.mean()], columns=OC6_data.columns)
    std_row = pd.DataFrame([OC6_data.std()], columns=OC6_data.columns)
    OC6_data_extended = pd.concat([OC6_data, mean_row, std_row], ignore_index=True)
    OC6_data_extended.index = ["replicate 1", "replicate 2", "replicate 3", "replicate 4", 
                        "replicate 5", "replicate 6", "mean", "std"]
    # Normalize each row by its last value
    OC6_data_normalized = OC6_data.div(OC6_data.iloc[:, 0], axis=0)

    # Now, compute the mean and std rows for the normalized data
    mean_row = pd.DataFrame([OC6_data_normalized.mean()], columns=OC6_data_normalized.columns)
    std_row = pd.DataFrame([OC6_data_normalized.std()], columns=OC6_data_normalized.columns)

    # Concatenate the original DataFrame with the mean and std rows
    OC6_data_normalized_extended = pd.concat([OC6_data_normalized, mean_row, std_row], ignore_index=True)
    # rename rows
    OC6_data_normalized_extended.index = ["replicate 1", "replicate 2", "replicate 3", "replicate 4", 
                            "replicate 5", "replicate 6", "mean", "std"]
    # Load data from csv
    Sal_data = pd.read_csv('Dat_for_Ayush/Sal.csv')

    # Compute mean of last five columns
    mean_1000uM = Sal_data[Sal_data.columns[-5:]].mean(axis=1)

    # Drop the original last five columns
    Sal_data = Sal_data.drop(Sal_data.columns[-5:], axis=1)

    # Add the mean column
    Sal_data['1000uM'] = mean_1000uM

    # Create Sal_data_extended with mean and std appended
    mean_row = pd.DataFrame([Sal_data.mean()], columns=Sal_data.columns)
    std_row = pd.DataFrame([Sal_data.std()], columns=Sal_data.columns)
    Sal_data_extended = pd.concat([Sal_data, mean_row, std_row], ignore_index=True)
    Sal_data_extended.index = ["replicate 1", "replicate 2", "replicate 3", "mean", "std"]

    # Normalize each row by its last value
    Sal_data_normalized = Sal_data.div(Sal_data.iloc[:, -1], axis=0)

    # Now, compute the mean and std rows for the normalized data
    mean_row = pd.DataFrame([Sal_data_normalized.mean()], columns=Sal_data_normalized.columns)
    std_row = pd.DataFrame([Sal_data_normalized.std()], columns=Sal_data_normalized.columns)

    # Concatenate the original DataFrame with the mean and std rows
    Sal_data_normalized_extended = pd.concat([Sal_data_normalized, mean_row, std_row], ignore_index=True)

    # Rename rows
    Sal_data_normalized_extended.index = ["replicate 1", "replicate 2", "replicate 3", "mean", "std"]


    ### Load OHC14 data
    # Load data from csv
    OHC14_data = pd.read_csv('Dat_for_Ayush/OHC14.csv')

    # Compute mean of last five columns
    mean_2uM = OHC14_data[OHC14_data.columns[-5:]].mean(axis=1)

    # Drop the original last five columns
    OHC14_data = OHC14_data.drop(OHC14_data.columns[-5:], axis=1)

    # Add the mean column
    OHC14_data['2uM'] = mean_2uM

    # Create OHC14_data_extended with mean and std appended
    mean_row = pd.DataFrame([OHC14_data.mean()], columns=OHC14_data.columns)
    std_row = pd.DataFrame([OHC14_data.std()], columns=OHC14_data.columns)
    OHC14_data_extended = pd.concat([OHC14_data, mean_row, std_row], ignore_index=True)
    OHC14_data_extended.index = ["replicate 1", "replicate 2", "replicate 3", "mean", "std"]

    # Normalize each row by its last value
    OHC14_data_normalized = OHC14_data.div(OHC14_data.iloc[:, -1], axis=0)

    # Now, compute the mean and std rows for the normalized data
    mean_row = pd.DataFrame([OHC14_data_normalized.mean()], columns=OHC14_data_normalized.columns)
    std_row = pd.DataFrame([OHC14_data_normalized.std()], columns=OHC14_data_normalized.columns)

    # Concatenate the original DataFrame with the mean and std rows
    OHC14_data_normalized_extended = pd.concat([OHC14_data_normalized, mean_row, std_row], ignore_index=True)

    # Rename rows
    OHC14_data_normalized_extended.index = ["replicate 1", "replicate 2", "replicate 3", "mean", "std"]
    if type_of_data == "normalized":
        all_normalized_data = {}
        all_normalized_data["Sal"] = Sal_data_normalized_extended
        all_normalized_data["OHC14"] = OHC14_data_normalized_extended
        all_normalized_data["OC6"] = OC6_data_normalized_extended
        all_normalized_data["IPTG"] = IPTG_data_normalized_extended
        all_normalized_data["IPTG*"] = IPTG_updated_df_normalized_extended
        return all_normalized_data
    if type_of_data == "absolute":
        absolute_data = {}
        absolute_data["Sal"] = Sal_data_extended
        absolute_data["OHC14"] = OHC14_data_extended
        absolute_data["OC6"] = OC6_data_extended
        absolute_data["IPTG"] = IPTG_data_extended
        absolute_data["IPTG*"] = IPTG_updated_df_extended
        return absolute_data
