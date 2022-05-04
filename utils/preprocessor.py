import os
import glob
import argparse
import pandas as pd

DEBUG = False

RAWDATAPATH = "./FW&BW_Rawdata/"
RAW_CONTROL = os.path.join(RAWDATAPATH, "Controls")
RAW_PD = os.path.join(RAWDATAPATH, "PD")

DATASETPATH = './dataset/'
DATA_CONTROL = os.path.join(DATASETPATH, 'Controls')
DATA_PD = os.path.join(DATASETPATH, 'PD')


def generatePrepData(rawdatapath):

    def prepData(target_path, target_file, ptype):

        if DEBUG:
            print("[ * ] prepData:", target_file)

        # 1. 2줄 제외하고 읽기

        dff = pd.read_csv(target_path, skiprows=2, encoding='utf-8')

        # 2. 전체 none인 컬럼 제외

        while dff[list(dff.columns)[-1]].isna().all():
            dff.drop(list(dff.columns)[-1], axis=1, inplace=True)

        # 3. 단위가 mm인 데이터만 추출

        target = [0, 1]
        target += list(filter(lambda x: list(dff.iloc[1] == 'mm')[x],
                              range(len(list(dff.iloc[1])))))
        dff = dff.iloc[:, target]
        dff.drop(dff.index[1], inplace=True)

        # 4. 컬럼 이름 변경하기

        pList = dff.columns
        colList = dff.iloc[0]

        NAME = None

        pNames = []
        for p in pList:
            if not p.startswith('Unnamed'):
                if NAME is None:
                    NAME = p.split(':')[0]
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

        if not os.path.exists(DATASETPATH + ptype):
            os.mkdir(DATASETPATH + ptype)

        dff.to_csv(os.path.join(os.path.join(DATASETPATH, ptype),
                                'PREP_' + target_file),
                   encoding='utf-8', index=False)

    if DEBUG:
        print("[ * ] runPrepData")

    for f in os.listdir(rawdatapath):
        if f.endswith('.csv'):
            prepData(os.path.join(rawdatapath, f),
                     f,
                     rawdatapath.split('/')[-1])


def generatePatientsInfoTable():

    def getPatientDataInfo(target_cate):

        if DEBUG:
            print("[ * ] getPatientDataInfo:", target_cate)

        dff = pd.DataFrame(columns=["Patient", "Category", "cntFW", "cntBW"])

        TARGET_DATA = DATA_CONTROL

        if target_cate == "PD":
            TARGET_DATA = DATA_PD

        files = glob.glob(os.path.join(TARGET_DATA, "*.csv"))
        fnames = list(set([f.split('/')[-1].split('_')[1] for f in files]))
        fnames.sort()

        for name in fnames:
            cnt_bw = len(glob.glob(os.path.join(TARGET_DATA,
                                                f"*{name}_BW*.csv")))
            cnt_fw = len(glob.glob(os.path.join(TARGET_DATA,
                                                f"*{name}_FW*.csv")))

            dff.loc[len(dff)] = [name, target_cate, cnt_fw, cnt_bw]

        return dff

    df = pd.DataFrame(columns=["Patient", "Category", "cntFW", "cntBW"])
    df = df.append(getPatientDataInfo("Controls"), ignore_index=True)
    df = df.append(getPatientDataInfo("PD"), ignore_index=True)

    df.to_csv(os.path.join(DATASETPATH, 'patients.csv'),
              encoding='utf-8', index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="debug mode")
    parser.add_argument("--rawdatapath", help="raw data path")
    parser.add_argument("--datasetpath", help="dataset path")
    args = parser.parse_args()

    if args.debug == "true":
        DEBUG = True

    if args.rawdatapath:
        RAWDATAPATH = args.rawdatapath

    if args.datasetpath:
        DATASETPATH = args.datasetpath

    if not os.path.exists(DATASETPATH):
        os.mkdir(DATASETPATH)

    generatePrepData(RAW_CONTROL)
    generatePrepData(RAW_PD)

    generatePatientsInfoTable()
