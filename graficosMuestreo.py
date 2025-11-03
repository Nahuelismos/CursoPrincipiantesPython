import pandas as pd
import matplotlib.pyplot as plt

# crear DataFrame
data = {"Mes": ["Enero", "Febrero", "Marzo", "Abril"],
        "Ventas": [150, 200, 180, 220]}
df = pd.DataFrame(data)

print(df.describe())

# crear gráfico
plt.bar(df["Mes"], df["Ventas"])
plt.title("Ventas por Mes")
plt.show()
