def plot_co2_data(fig_ax=None):
    if not fig_ax:
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    else:
        fig, ax = fig_ax
    ax.plot(co2_by_month_training_data, label="training data")
    ax.plot(co2_by_month_testing_data, color="C4", label="testing data")
    ax.legend()
    ax.set(
        ylabel="Atmospheric CO2 concentration (ppm)",
        xlabel="Year"
    )
    ax.text(0.99, .02,
              """Source: National Oceanic & Atmospheric Administraion 
                         Trends in Atmospheric Carbon Dioxide
              https://gml.noaa.gov/ccgg/trends/data.html""",
              transform=ax.transAxes,
              horizontalalignment="right",
              alpha=0.5)
    fig.autofmt_xdate()
    return fig, ax