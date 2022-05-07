import numpy as np
import pandas as pd
import os
import re


class DataTools:
    """

    PREPROCESSED DATASET EXTRACTOR TOOLS

    ---------------------------------------------------------------
    Example 1:
    t = DataTools()

    DATASETPATH = t.get_datasetpath()
    print("dataset path:", DATASETPATH)

    patients = t.get_patients_table()
    CONTROL = patients[patients["Category"] == "Controls"]
    PD = patients[patients["Category"] == "PD"]

    idx = 0

    category = CONTROL["Category"][idx]
    patient = CONTROL["Patient"][idx]
    print("category:", category)
    print(" patient:", patient)

    fw, bw = t.get_patient_datapath(category, patient)
    fw_data, bw_data = t.get_patient_fwdw_data(category, patient)
    ---------------------------------------------------------------
    
    ---------------------------------------------------------------
    Example 2 - custom dataset path: 
    t = DataTools()
    t.set_datasetpath(~~CUSTOM DATASET PATH~~)

    DATASETPATH = t.get_datasetpath()
    print("dataset path:", DATASETPATH)

    patients = t.get_patients_table()
    CONTROL = patients[patients["Category"] == "Controls"]
    PD = patients[patients["Category"] == "PD"]

    idx = 0

    category = CONTROL["Category"][idx]
    patient = CONTROL["Patient"][idx]
    print("category:", category)
    print(" patient:", patient)

    fw, bw = t.get_patient_datapath(category, patient)
    fw_data, bw_data = t.get_patient_fwdw_data(category, patient)
    ---------------------------------------------------------------
    """

    def __init__(self):

        # Processed data path

        self.DATASETPATH = "./dataset/"
        self.DATA_CONTROL = os.path.join(self.DATASETPATH, "Controls")
        self.DATA_PD = os.path.join(self.DATASETPATH, "PD")
        self.INFO_FILE = "patients.csv"

    def set_datasetpath(self, datasetpath: str):
        """
        set custom dataset path

        - datasetpath: dataset path
        """

        self.DATASETPATH = datasetpath
        self.DATA_CONTROL = os.path.join(self.DATASETPATH, "Controls")
        self.DATA_PD = os.path.join(self.DATASETPATH, "PD")

    def get_datasetpath(self) -> str:
        return self.DATASETPATH

    def get_patients_table(self) -> pd.DataFrame:
        """
        get patients FW & BW data count info table
        """

        patients = pd.read_csv(os.path.join(self.DATASETPATH, self.INFO_FILE),
                               encoding="utf-8")

        return patients

    def get_patient_datapath(self, target_cate: str, target_patient: str, mode="PREP") -> list:
        """
        get patients FW & BW data path

        - target_cate: target patient category, "Controls" or "PD"
        - target_patient: target patient's name, initial
        - mode: default "PREP"
        """

        fw = []
        bw = []

        target_folder = self.DATA_CONTROL

        if target_cate == "PD":
            target_folder = self.DATA_PD

        files = os.listdir(target_folder)

        p = re.compile(target_patient)
        idxs = list(filter(lambda x: p.search(files[x]) != None
                           and files[x].startswith(mode),
                           range(len(files))))

        for idx in idxs:
            f = files[idx]

            if f.split('/')[-1].split('_')[2].startswith("FW"):
                fw.append(os.path.join(target_folder, f))
            else:
                bw.append(os.path.join(target_folder, f))

        fw.sort()
        bw.sort()

        return fw, bw

    def get_patient_fwdw_data(self, target_cate: str, target_patient: str, mode="PREP") -> pd.DataFrame:
        """
        get patients FW & BW data

        - target_cate: target patient category, "Controls" or "PD"
        - target_patient: target patient's name, initial
        - mode: default "PREP"
        """

        fw, bw = self.get_patient_datapath(target_cate, target_patient, mode)

        fw_data = []
        bw_data = []

        for f in fw:
            df_f = pd.read_csv(f, encoding="utf-8")
            fw_data.append(df_f)

        for b in bw:
            df_b = pd.read_csv(b, encoding="utf-8")
            bw_data.append(df_b)

        return fw_data, bw_data


if __name__ == "__main__":

    t = DataTools()

    DATASETPATH = t.get_datasetpath()
    print("[ * ] dataset path:", DATASETPATH)

    patients = t.get_patients_table()
    CONTROL = patients[patients["Category"] == "Controls"]
    PD = patients[patients["Category"] == "PD"]

    idx = 0

    category = CONTROL["Category"][idx]
    patient = CONTROL["Patient"][idx]
    print("[ * ] category:", category)
    print("[ * ] patient:", patient)

    fw, bw = t.get_patient_datapath(category, patient)
    fw_data, bw_data = t.get_patient_fwdw_data(category, patient)
    print("[ * ] DONE")
