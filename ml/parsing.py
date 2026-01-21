import pandas as pd
import numpy as np

batch_size = 41
df = pd.read_csv('optim.csv')
dfs11 = df["dB(St(port1_T1,port1_T1)) []"].tolist()
f = df["Freq [GHz]"].tolist()
dimensions = ["d []","dw [mm]","h [mm]","h_s [mm]","l [mm]","l_inset [mm]","l_s [mm]","ls [mm]","w [mm]","w_inset [mm]","w_s [mm]"]
dval = df[dimensions].values
d = {}
batchess11 = np.array_split(dfs11, len(df)//batch_size)
freqs = np.array_split(f, len(df)//batch_size)
arg = []
operatingfreq  = []
s11 = []
s11neg = []
s11pos = []
for b in batchess11:
    arg.append(int(np.argmin(b)))
    s11.append(min(b))
count = 0
for i in range(len(df)//batch_size):
    operatingfreq.append(freqs[i][arg[count]])
    s11neg.append(batchess11[i][arg[count]-2])
    s11pos.append(batchess11[i][arg[count]+2])
    count+=1

for i in range(len(df)//batch_size):
    key = dval[i*batch_size].tolist()
    d[tuple(list(key))]= arg[i]

data = {
    "dims": list(d.keys()),
    "Operating Frequency": operatingfreq,
    "s11 left" : s11neg,
    "s11" : s11,
    "s11 right" : s11pos
}
for da in data:
    print(len(data[da]))

parsed = pd.DataFrame(data)
parsed.to_csv('goodata.csv')
parsed.to_excel("output.xlsx", sheet_name="Sheet1", index=False)