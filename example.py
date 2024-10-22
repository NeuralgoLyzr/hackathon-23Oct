from main import DataAnalysis

da = DataAnalysis(filepath="world-data-2023.csv")
result = da.ask("Your question here")


# View the analysis output
print(result["analysis_output"])

# View the plot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread(result["plot_path"])
imgplot = plt.imshow(img)
plt.axis("off")
plt.show()

# View the insights
print(result["insights"])
