import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import seaborn as sns

import os
import pandas as pd
import numpy as np

def plotPatientLRZDiff(patient, FWdata):
    """ patient's left heel & right heel Z-axis balance visualization """
    for idx, data in enumerate(FWdata):
        
        # PHASE 1 시작하는 지점 찾기 -- 이전 인덱스와 5 이상 차이나는 경우 선택
        start = [np.where(data["PHASE"] == 1)[0][0]] + [ x for idx, x in enumerate(np.where(data["PHASE"] == 1)[0][1:]) if x -np.where(data["PHASE"] == 1)[0][idx] > 5 ]

        fig, axes = plt.subplots(2, 2, figsize=(20,10), tight_layout=True)
        fig.suptitle(f"{patient} - FW{idx+1}", fontsize=15)

        sns.lineplot(ax=axes[0][0], data=data[["LHEE_Z", "RHEE_Z"]])
        axes[0][0].set_title("Left-Right HEE Z-aixs")

        sns.lineplot(ax=axes[0][1], data=data[["LHEE_Z_DIFF", "RHEE_Z_DIFF"]])
        axes[0][1].set_title("Left-Right HEE Diff")

        # phase 1 중 LHEE_Z_DIFF > RHEE_Z_DIFF 인 경우를 shift 기준으로 사용
        shift = start[1]
        if data.iloc[shift]["LHEE_Z_DIFF"] < data.iloc[shift]["RHEE_Z_DIFF"]: shift = start[2]

        sns.lineplot(ax=axes[1][0], data=pd.DataFrame({
                    "LHEE_Z" : data.iloc[0:-shift]["LHEE_Z"].values,
                    "RHEE_Z" : data.iloc[shift:]["RHEE_Z"].values})
                    )
        axes[1][0].set_title("Left-Right HEE Z-axis sync")

        sns.lineplot(ax=axes[1][1], data=pd.DataFrame({
                    "LHEE_Z_DIFF" : data.iloc[0:-shift]["LHEE_Z_DIFF"].values,
                    "RHEE_Z_DIFF" : data.iloc[shift:]["RHEE_Z_DIFF"].values})
                    )
        axes[1][1].set_title("Left-Right HEE Diff sync")
    plt.show()
    
    
if __name__=="__main__":
    STDPATH = "LHEE 기준 STD 완료한 데이터셋 위치" # 변경필요
    CONTROL_PATH = os.path.join(STDPATH, "Controls")
    PD_PATH = os.path.join(STDPATH, "PD")
    
    patient = "환자 이니셜" # 변경필요
    
    FWdata = [
        pd.read_csv(os.path.join(CONTROL_PATH, f"파일이름1")), #변경필요
        pd.read_csv(os.path.join(CONTROL_PATH, f"파일이름2")), #변경필요
        pd.read_csv(os.path.join(CONTROL_PATH, f"파일이름3"))  #변경필요
    ]
    
    plotPatientLRZDiff(patient, FWdata)
