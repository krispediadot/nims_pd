import os
import glob
import argparse
import pandas as pd

if __name__ == "__main__":
    from datatools import DataTools
else:
    from utils.datatools import DataTools

DEBUG = False


class Preprocessor:
    """

    DAMC PD FW & BW DATASET PREPROCESSOR

    1) preprocessing
    2) phase

    ---------------------------------------
    Example 1:
    p = Preprocessor()

    p.generate_prep_data(p.RAW_CONTROL)
    p.generate_prep_data(p.RAW_PD)

    p.generate_patients_fwbw_info_table()

    ---------------------------------------

    ---------------------------------------
    Example 2:
    p = Preprocessor()

    p.set_datasepath(~~CUSTOM PATH~~)
    p.generate_prep_data(p.RAW_CONTROL)
    p.generate_prep_data(p.RAW_PD)

    p.generate_patients_fwbw_info_table()

    ---------------------------------------
    """

    def __init__(self):

        self.t = DataTools()

        # RAW data path

        self.RAWDATAPATH = "./FW&BW_Rawdata/"
        self.RAW_CONTROL = os.path.join(self.RAWDATAPATH, "Controls")
        self.RAW_PD = os.path.join(self.RAWDATAPATH, "PD")

        # Processed data path

        self.DATASETPATH = "./dataset/"
        self.DATA_CONTROL = os.path.join(self.DATASETPATH, "Controls")
        self.DATA_PD = os.path.join(self.DATASETPATH, "PD")
        self.DATASET_PREFIX = "PREP_"

        if not os.path.exists(self.DATASETPATH):
            os.mkdir(self.DATASETPATH)
        if not os.path.exists(self.DATA_CONTROL):
            os.mkdir(self.DATA_CONTROL)
        if not os.path.exists(self.DATA_PD):
            os.mkdir(self.DATA_PD)

        # Phase data path

        self.PHASEPATH = "./dataset_LHEE_RHEE_Z_PHASE/"
        self.CONTROL_PATH = os.path.join(self.PHASEPATH, "Controls")
        self.PD_PATH = os.path.join(self.PHASEPATH, "PD")

        if not os.path.exists(self.PHASEPATH):
            os.mkdir(self.PHASEPATH)
        if not os.path.exists(self.CONTROL_PATH):
            os.mkdir(self.CONTROL_PATH)
        if not os.path.exists(self.PD_PATH):
            os.mkdir(self.PD_PATH)

        self.PHASE_ERROR_FILENAME = "error.csv"
        
        

    def set_rawdatapath(self, rawdatapath: str):
        """
        set custom raw data path
        """

        self.RAWDATAPATH = rawdatapath
        self.RAW_CONTROL = os.path.join(self.RAWDATAPATH, "Controls")
        self.RAW_PD = os.path.join(self.RAWDATAPATH, "PD")

    def set_datasetpath(self, datasetpath: str):
        """
        set custom preprocessed data save path
        """

        self.DATASETPATH = datasetpath
        self.DATA_CONTROL = os.path.join(self.DATASETPATH, "Controls")
        self.DATA_PD = os.path.join(self.DATASETPATH, "PD")
        self.DATASET_PREFIX = "PREP_"

        if not os.path.exists(self.DATASETPATH):
            os.mkdir(self.DATASETPATH)
        if not os.path.exists(self.DATA_CONTROL):
            os.mkdir(self.DATA_CONTROL)
        if not os.path.exists(self.DATA_PD):
            os.mkdir(self.DATA_PD)

    def set_phasepath(self, phasepath: str):
        """
        set custom phase path
        """

        self.PHASEPATH = phasepath
        self.CONTROL_PATH = os.path.join(self.PHASEPATH, "Controls")
        self.PD_PATH = os.path.join(self.PHASEPATH, "PD")

        if os.path.exists(self.PHASEPATH) is False:
            os.mkdir(self.PHASEPATH)
        if os.path.exists(self.CONTROL_PATH) is False:
            os.mkdir(self.CONTROL_PATH)
        if os.path.exists(self.PD_PATH) is False:
            os.mkdir(self.PD_PATH)

    def get_rawdatapath(self) -> str:
        return self.RAWDATAPATH

    def get_datasetpath(self) -> str:
        return self.DATASETPATH

    def get_phasepath(self) -> str:
        return self.PHASEPATH

    def prep_data(self, target_path: str, target_file: str, target_cate: str):
        """
        preprocess raw data file

        - target_path: target file path
        - target_file: target file name
        - target_cate: target patient category, "Controls" or "PD"

        1. Skip 2 rows from raw data file
        2. Select positional info columns (unit=mm)
        4. Rename columns as {MARKER NAME}_X, {MARKER_NAME}_Y, {MAREKR_NAME}_Z
        5. Save processed file to DATASETPATH
        """

        if DEBUG:
            print("[ * ] prep_data:", target_file)

        # 1. Skip 2 rows from raw data file

        dff = pd.read_csv(target_path, skiprows=2, encoding="utf-8")

        # 2. Select positional info columns (unit=mm)

        target = [0] + list(filter(lambda x: dff.iloc[1].values[x] == "mm", 
                                   range(len(dff.columns))))
        
        dff = dff.iloc[:, target]
        dff.drop(dff.index[1], inplace=True)

        #  4. Rename columns as
        #     {MARKER NAME}_X, {MARKER_NAME}_Y, {MAREKR_NAME}_Z

        mark_list = dff.columns.values
        axis_list = dff.iloc[0].values

        mark_names = [ (idx, mark.split(':')[1]) for idx, mark in enumerate(mark_list)
                      if (not mark.startswith("Unnamed"))
                      and (not mark.split(':')[1].startswith("Centre"))]
        
        columns = [axis_list[0]]  # add Frame column
        
        for idx, mark in mark_names:
            columns.append(mark + '_' + axis_list[idx])
            columns.append(mark + '_' + axis_list[idx+1])
            columns.append(mark + '_' + axis_list[idx+2])

        assert len(columns) == 1+39*3

        dff.drop(dff.index[0], inplace=True)
        dff.reset_index(drop=True, inplace=True)
        dff.columns = columns

        if not os.path.exists(os.path.join(self.DATASETPATH, target_cate)):
            os.mkdir(os.path.join(self.DATASETPATH + target_cate))

        # 5. Save processed file to DATASETPATH

        dff.to_csv(os.path.join(os.path.join(self.DATASETPATH, target_cate),
                                self.DATASET_PREFIX + target_file),
                   encoding="utf-8", index=False)

    def generate_prep_data(self, rawdatapath: str):
        """
        apply def prepData to whole raw data files

        - rawdatapath: raw dataset path
        """

        if DEBUG:
            print("[ * ] run prep_data")

        for f in os.listdir(rawdatapath):
            if f.endswith(".csv"):
                self.prep_data(os.path.join(rawdatapath, f), f,
                               rawdatapath.split('/')[-1])

    def get_patients_fwbw_info(self, target_cate: str) -> pd.DataFrame:
        """
        create pandas dataframe of FW & BW counts information

        - target_cate: "Controls" or "PD"
        """

        if DEBUG:
            print("[ * ] get_patients_fwbw_info:", target_cate)

        dff = pd.DataFrame(columns=["Patient", "Category", "cntFW", "cntBW"])

        target_data = self.DATA_CONTROL

        if target_cate == "PD":
            target_data = self.DATA_PD

        files = glob.glob(os.path.join(target_data, "*.csv"))
        fnames = list(set([f.split('/')[-1].split('_')[1] for f in files]))
        fnames.sort()

        for name in fnames:
            cnt_bw = len(glob.glob(os.path.join(target_data,
                                                f"*{name}_BW*.csv")))
            cnt_fw = len(glob.glob(os.path.join(target_data,
                                                f"*{name}_FW*.csv")))

            dff.loc[len(dff)] = [name, target_cate, cnt_fw, cnt_bw]

        return dff

    def generate_patients_fwbw_info_table(self):
        """
        create and save patients FW & BW count information table

        save path = DATASETPATH/patients.csv
        """

        df = pd.DataFrame(columns=["Patient", "Category", "cntFW", "cntBW"])
        df = df.append(self.get_patients_fwbw_info("Controls"), ignore_index=True)
        df = df.append(self.get_patients_fwbw_info("PD"), ignore_index=True)

        df.to_csv(os.path.join(self.DATASETPATH, "patients.csv"),
                  encoding="utf-8", index=False)


    def generate_phase_info(self, df_data_list: list, target_cate_path: str, filename_prefix: str):
        """
        Add and save phase column in a data file

        - df_data_list: target pd.DataFrame list
        - target_cate_path: target category path
        - filename_prefix: generated filename with patient name & FW/BW info
                            ex) PHASE_AAA_BW1.csv

        1. Calculate diff of HEE
        2. Categorize phase 1/2/3/4
        """

        for idx, data in enumerate(df_data_list):

            df = data.copy()

            # 1. Calculate diff of HEE

            LHEE_Z_diff = [df.iloc[idx+1]["LHEE_Z"] - df.iloc[idx]["LHEE_Z"]
                           for idx in range(len(df)-1)]

            RHEE_Z_diff = [df.iloc[idx+1]["RHEE_Z"] - df.iloc[idx]["RHEE_Z"]
                           for idx in range(len(df)-1)]

            df["LHEE_Z_DIFF"] = [None] + LHEE_Z_diff
            df["RHEE_Z_DIFF"] = [None] + RHEE_Z_diff

            # 2. Categorize phase 1/2/3/4

            phase = [None]

            for l_diff, r_diff in zip(df["LHEE_Z_DIFF"][1:], df["RHEE_Z_DIFF"][1:]):

                # criteria: l_diff & r_diff

                if l_diff is not None and r_diff is not None:
                    if l_diff >= 0 and r_diff >= 0: phase.append(1)
                    if l_diff >= 0 and r_diff < 0: phase.append(2)
                    if l_diff < 0 and r_diff >= 0: phase.append(3)
                    if l_diff < 0 and r_diff < 0: phase.append(4)
                else:
                    phase.append(None)

            df["PHASE"] = phase
            df.to_csv(os.path.join(target_cate_path,
                                   f"{filename_prefix}{idx+1}.csv"), index=False)

    def generate_phase_dataset(self, patients_df: pd.DataFrame, target_cate: str, target_cate_path: str):
        """
        Create and Save phase dataset

        - patients_df: target patients info from patients.csv
        - target_cate: "Controls" or "PD"
        - target_cate_path: target category path
        """

        # 1. Create pd.DataFrame for error csv

        dt = pd.DataFrame(columns=["Patient", "Category", "FW_BW"])

        if os.path.exists(os.path.join(self.PHASEPATH, self.PHASE_ERROR_FILENAME)):
            dt = pd.read_csv(os.path.join(self.PHASEPATH, self.PHASE_ERROR_FILENAME))

        for patient_initial in patients_df["Patient"]:

            # 2. Get each patients FW & BW data list

            fw_data, bw_data = self.t.get_patient_fwbw_data(target_cate, patient_initial)

            # 3. Generate phase

            # FW

            try:
                self.generate_phase_info(fw_data, target_cate_path,
                                         f"PHASE_{patient_initial}_FW")
            except:
                print(patient_initial+"_FW")
                dt.loc[len(dt)] = [patient_initial, target_cate, "FW"]

            # BW

            try:
                self.generate_phase_info(bw_data, target_cate_path,
                                         f"PHASE_{patient_initial}_BW")
            except:
                print(patient_initial+"_BW")
                dt.loc[len(dt)] = [patient_initial, target_cate, "BW"]

        # 4. Save error result as csv

        dt.to_csv(os.path.join(self.PHASEPATH, self.PHASE_ERROR_FILENAME),
                  index=False)


if __name__ == "__main__":

    p = Preprocessor()

    # == Options ==

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="debug mode, use true or t")
    parser.add_argument("--rawdatapath", help="raw data path")
    parser.add_argument("--datasetpath", help="dataset path")
    parser.add_argument("--phasepath", help="phase path")
    args = parser.parse_args()

    if args.debug == "true" or args.debug == "t":
        DEBUG = True

    if args.rawdatapath:
        p.set_rawdatapath(args.rawdatapath)

    if args.datasetpath:
        p.set_datasetpath(args.datasetpath)

    if args.phasepath:
        p.set_phasepath(args.phasepath)

    if not os.path.exists(p.DATASETPATH):
        os.mkdir(p.DATASETPATH)

    # == Processor ==

    p.generate_prep_data(p.RAW_CONTROL)
    p.generate_prep_data(p.RAW_PD)

    p.generate_patients_fwbw_info_table()

#     # == PHASE ==

#     p = Preprocessor()
#     p.set_phasepath("./dataset_LHEE_RHEE_Z_PHASE_/")

#     PHASEPATH = p.get_phasepath()
#     CONTROL_PATH = os.path.join(PHASEPATH, "Controls")
#     PD_PATH = os.path.join(PHASEPATH, "PD")

#     t = DataTools()
#     patients = t.get_patients_table()

#     CONTROL = patients[patients["Category"] == "Controls"]
#     PD = patients[patients["Category"] == "PD"]

#     print("Controls count:", len(CONTROL))
#     print("PD count:", len(PD))

#     p.generate_phase_dataset(CONTROL, "Controls", CONTROL_PATH)
#     p.generate_phase_dataset(PD, "PD", PD_PATH)

#     # == SHIFT ==
    
#     p = Preprocessor()
#     p.set_shiftpath("./dataset_PHEE_RHEE_Z_PHASE_SHIFT")
    
    
    
    