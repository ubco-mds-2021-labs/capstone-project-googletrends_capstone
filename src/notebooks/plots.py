import matplotlib.pyplot as plt
import seaborn as sns

class plots(object):
    def plot_df(y, title="", xlabel='Date', ylabel='Value', dpi=100, width = 16, height = 5):
        plt.figure(figsize=(width,height), dpi=dpi)
        plt.plot(y)
        plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
        #plt.close()
        return plt.show()
    
