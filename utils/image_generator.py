import pandas as pd
import numpy as np

DATAPATH = "/Users/sujinlee/Desktop/nims/pd/dataset"
CONTROL = os.path.join(DATAPATH, "Controls")
PD = os.path.join(DATAPATH, "PD")

df_patients = pd.read_csv(os.path.join(DATAPATH, "patients.csv"))
df_null_info = pd.read_csv(os.path.join(DATAPATH, "NULL_info.csv"))

print("PD count:", np.sum(df_patients[df_patients["Category"] == "PD"]["cntFW"].values) + np.sum(df_patients[df_patients["Category"] == "PD"]["cntBW"].values))
print("Controls count:", np.sum(df_patients[df_patients["Category"] == "Controls"]["cntFW"].values) + np.sum(df_patients[df_patients["Category"] == "Controls"]["cntBW"].values))

DATAPATH_IMG = DATAPATH + "_img"
DATAPATH_NP = DATAPATH + "_np"

if os.path.exists(DATAPATH_IMG) == False: 
    os.os.mkdir(DATAPATH_IMG)
    os.mkdir(os.path.join(DATAPATH_IMG, "Controls"))
    os.mkdir(os.path.join(DATAPATH_IMG, "PD"))
    
if os.path.exists(DATAPATH_NP) == False:
    os.mkdir(DATAPATH_NP)
    os.mkdir(os.path.join(DATAPATH_NP, "Controls"))
    os.mkdir(os.path.join(DATAPATH_NP, "PD"))
    
print(len(os.listdir(os.path.join(DATAPATH_IMG, "Controls"))))
print(len(os.listdir(os.path.join(DATAPATH_IMG, "PD"))))

print(len(os.listdir(os.path.join(DATAPATH_NP, "Controls"))))
print(len(os.listdir(os.path.join(DATAPATH_NP, "PD"))))

# 전체 데이터 x,y,z
for cate, name, nFW, nBW in zip(df_patients["Category"].values, df_patients["Patient"].values, df_patients["cntFW"].values, df_patients["cntBW"].values):    
    for idx in range(1, nFW+1):
        
        if not (name == "KMS" and idx == 3) and not (name == "BGH" and idx == 1):
            
            df = pd.read_csv(os.path.join(os.path.join(DATAPATH, cate), f"PREP_{name}_FW{idx}.csv"))
            df_sample = df.copy()

            # x, y, z 추출
            df_x = df_sample.filter(regex='X')
            df_y = df_sample.filter(regex='Y')
            df_z = df_sample.filter(regex='Z')

            # MARKERS 컬럼들인지 확인 
            print("LEN X:", len(df_x.columns))
            print("LEN Y:", len(df_y.columns))
            print("LEN Z:", len(df_z.columns))

            assert len(df_x.columns) == 39 and len(set([x.split('_')[0] for x in df_x]) - set(MARKERS)) == 0
            assert len(df_y.columns) == 39 and len(set([x.split('_')[0] for x in df_y]) - set(MARKERS)) == 0
            assert len(df_z.columns) == 39 and len(set([x.split('_')[0] for x in df_z]) - set(MARKERS)) == 0

            # 컬럼 순서 재 확인
            df_x = df_x[[m + "_X" for m in MARKERS]]
            df_y = df_y[[m + "_Y" for m in MARKERS]]
            df_z = df_z[[m + "_Z" for m in MARKERS]]

            # 3차원 벡터 생성
            df_img = np.stack([df_x, df_y, df_z], -1)
            
            # save numpy 
            np.save(os.path.join(os.path.join(DATAPATH_NP, cate), f"NP_{name}_FW{idx}.npy"), df_img)

            # save img
            from PIL import Image
            df_img_jpg = Image.fromarray(df_img.astype(np.uint8))
            df_img_jpg.save(os.path.join(os.path.join(DATAPATH_IMG, cate), f"IMG_{name}_FW{idx}.jpg"))

            print(name, f"FW{idx}")
            print(len(df))

    for idx in range(1, nBW+1):
        
        if not (name == "BGH" and idx == 1):
        
            df = pd.read_csv(os.path.join(os.path.join(DATAPATH, cate), f"PREP_{name}_BW{idx}.csv"))
            df_sample = df.copy()

            # x, y, z 추출
            df_x = df_sample.filter(regex='X')
            df_y = df_sample.filter(regex='Y')
            df_z = df_sample.filter(regex='Z')

            # MARKERS 컬럼들인지 확인 
            print("LEN X:", len(df_x.columns))
            print("LEN Y:", len(df_y.columns))
            print("LEN Z:", len(df_z.columns))

            assert len(df_x.columns) == 39 and len(set([x.split('_')[0] for x in df_x]) - set(MARKERS)) == 0
            assert len(df_y.columns) == 39 and len(set([x.split('_')[0] for x in df_y]) - set(MARKERS)) == 0
            assert len(df_z.columns) == 39 and len(set([x.split('_')[0] for x in df_z]) - set(MARKERS)) == 0

            # 컬럼 순서 재 확인
            df_x = df_x[[m + "_X" for m in MARKERS]]
            df_y = df_y[[m + "_Y" for m in MARKERS]]
            df_z = df_z[[m + "_Z" for m in MARKERS]]

            # 3차원 벡터 생성
            df_img = np.stack([df_x, df_y, df_z], -1)
            
            # save numpy 
            np.save(os.path.join(os.path.join(DATAPATH_NP, cate), f"NP_{name}_BW{idx}.npy"), df_img)

            # save img
            from PIL import Image
            df_img_jpg = Image.fromarray(df_img.astype(np.uint8))
            df_img_jpg.save(os.path.join(os.path.join(DATAPATH_IMG, cate), f"IMG_{name}_BW{idx}.jpg"))

            print(name, f"BW{idx}")
            
# x, y, z 추출
df_x = df.filter(regex='X')
df_y = df.filter(regex='Y')
df_z = df.filter(regex='Z')

# MARKERS 컬럼들인지 확인 
print("LEN X:", len(df_x.columns))
print("LEN Y:", len(df_y.columns))
print("LEN Z:", len(df_z.columns))

assert len(df_x.columns) == 39 and len(set([x.split('_')[0] for x in df_x]) - set(MARKERS)) == 0
assert len(df_y.columns) == 39 and len(set([x.split('_')[0] for x in df_y]) - set(MARKERS)) == 0
assert len(df_z.columns) == 39 and len(set([x.split('_')[0] for x in df_z]) - set(MARKERS)) == 0

# 컬럼 순서 재 확인
df_x = df_x[[m + "_X" for m in MARKERS]]
df_y = df_y[[m + "_Y" for m in MARKERS]]
df_z = df_z[[m + "_Z" for m in MARKERS]]

# 3차원 벡터 생성
df_img = np.stack([df_x, df_y, df_z], -1)

# save img
from PIL import Image
df_img_jpg = Image.fromarray(df_img.astype(np.uint8))
df_img_jpg.save(os.path.join(DATAPATH, "your_file.jpg"))

# save numpy
np.save(os.path.join(DATAPATH, "sample.npy"), df_img)