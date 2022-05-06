import os
import glob
import argparse
import pandas as pd

DEBUG = False


class Preprocessor:
    """

    DAMC PD FW & BW DATASET PREPROCESSOR

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

        # RAW data path

        self.RAWDATAPATH = "./FW&BW_Rawdata/"
        self.RAW_CONTROL = os.path.join(self.RAWDATAPATH, "Controls")
        self.RAW_PD = os.path.join(self.RAWDATAPATH, "PD")

        # Processed data path

        self.DATASETPATH = "./dataset/"
        self.DATA_CONTROL = os.path.join(self.DATASETPATH, "Controls")
        self.DATA_PD = os.path.join(self.DATASETPATH, "PD")
        self.PREFIX = "PREP_"

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
        self.PREFIX = "PREP_"

        if not os.path.exists(self.DATASETPATH):
            os.mkdir(self.DATASETPATH)

        if not os.path.exists(self.DATA_CONTROL):
            os.mkdir(self.DATA_CONTROL)

        if not os.path.exists(self.DATA_PD):
            os.mkdir(self.DATA_PD)

    def get_rawdatapath(self) -> str:
        return self.RAWDATAPATH

    def get_datasetpath(self) -> str:
        return self.DATASETPATH

    def prep_data(self, target_path: str, target_file: str, target_cate: str):
        """
        preprocess raw data file

        - target_path: target file path
        - target_file: target file name
        - target_cate: target patient category, "Controls" or "PD"

        1. Skip 2 rows from raw data file
        2. Remove un-recorded columns
        3. Select positional info columns (unit=mm)
        4. Rename columns as {MARKER NAME}_X, {MARKER_NAME}_Y, {MAREKR_NAME}_Z
        5. Save processed file to DATASETPATH
        """

        if DEBUG:
            print("[ * ] prep_data:", target_file)

        # 1. Skip 2 rows from raw data file

        dff = pd.read_csv(target_path, skiprows=2, encoding="utf-8")

        # 2. Remove un-recorded columns

        while dff[list(dff.columns)[-1]].isna().all():
            dff.drop(list(dff.columns)[-1], axis=1, inplace=True)

        # 3. Select positional info columns (unit=mm)

        target = [0, 1]
        target += list(filter(lambda x: list(dff.iloc[1] == "mm")[x],
                              range(len(list(dff.iloc[1])))))
        dff = dff.iloc[:, target]
        dff.drop(dff.index[1], inplace=True)

        #  4. Rename columns as {MARKER NAME}_X, {MARKER_NAME}_Y, {MAREKR_NAME}_Z

        pList = dff.columns
        colList = dff.iloc[0]

        name = None

        pNames = []
        for p in pList:
            if not p.startswith("Unnamed"):
                if name is None:
                    name = p.split(':')[0]
                pNames.append(p.split(':')[1])

        columns = []
        columns.append(colList[0])
        columns.append(colList[1])
        for idx, col in enumerate(colList[2:]):
            i = int(idx / 3)
            eachColName = pNames[i] + '_' + col
            columns.append(eachColName)

        assert len(columns) == len(list(dff.columns))

        dff.drop(dff.index[0], inplace=True)
        dff.reset_index(drop=True, inplace=True)
        dff.columns = columns

        if not os.path.exists(os.path.join(self.DATASETPATH, target_cate)):
            os.mkdir(os.path.join(self.DATASETPATH + target_cate))

        # 5. Save processed file to DATASETPATH

        dff.to_csv(os.path.join(os.path.join(self.DATASETPATH, target_cate),
                                self.PREFIX + target_file),
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


if __name__ == "__main__":

    p = Preprocessor()

    # Options

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="debug mode, use true or t")
    parser.add_argument("--rawdatapath", help="raw data path")
    parser.add_argument("--datasetpath", help="dataset path")
    args = parser.parse_args()

    if args.debug == "true" or args.debug == "t":
        DEBUG = True

    if args.rawdatapath:
        p.set_rawdatapath(args.rawdatapath)

    if args.datasetpath:
        p.set_datasetpath(args.datasetpath)

    if not os.path.exists(p.DATASETPATH):
        os.mkdir(p.DATASETPATH)

    # Processor

    p.generate_prep_data(p.RAW_CONTROL)
    p.generate_prep_data(p.RAW_PD)

    p.generate_patients_fwbw_info_table()
