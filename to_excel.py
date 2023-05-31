import json
import pandas as pd
from IPython.display import display

with open("results.json") as f:
    results = f.read()

tso = []
strækning = []
data = json.loads(results)
for k, v in data.items():
    for (
        nk,
        nv,
    ) in v.items():
        output.append([k, nv])

print(output)
df = pd.DataFrame(output)

df.to_excel("output.xlsx", index=False)

# print(df)
