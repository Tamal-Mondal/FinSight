from quickfs import QuickFS
import os
import random
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv()

api_key = os.environ["QUICKFS_API_KEY"]
print("QUICKFS_API_KEY: "+ api_key)
client = QuickFS(api_key)

symbol = "TSLA"
metric = "fcf"
data = client.get_data_range(symbol=f'{symbol}:US', metric=metric, period='FY-9:FY')
data = {"metric": metric, "data": data}
print(data)

years = list(range(len(data["data"])))

# Generate a random color for all bars
bar_color = f'#{random.randint(0, 0xFFFFFF):06x}'

fig, ax = plt.subplots()
ax.bar(years, data["data"], color=bar_color)
ax.set_xlabel('Years')
ax.set_title(data["metric"])

# Save the figure to the current directory
metric = data["metric"]
file_path = f"./{metric.replace(' ', '_')}_chart.png"
fig.savefig(file_path, format='png')
plt.close(fig)