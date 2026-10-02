@@ matplotlib-basics
topics: figure and axes, `plt.subplots`, `ax.plot`, titles and labels, legends, `figsize`, styling, `savefig`
terms:
- **matplotlib:** Python's main charting library; `pyplot` (imported as `plt`) is its main interface.
- **Figure:** the whole image, which can hold one or more charts.
- **Axes:** one chart area inside a figure, with its own x and y axes. You draw on it with `ax.` methods.
- **plt.subplots:** creates a figure and its axes in one call.
- **Line chart:** points joined by lines, best for change over time.
- **Legend:** the key that says which line or colour is which.
- **figsize:** the figure's (width, height) in inches.
- **savefig:** writes a figure to an image file.
mistakes:
- Leaving the default title and labels empty. Every chart needs a title and axis labels with units.
- Calling `ax.legend()` without giving lines a `label=`, which shows an empty legend.
- Mixing up `plt.title()` and `ax.set_title()`. With `fig, ax`, use the `ax.set_...` methods.

@@ chart-types
topics: bar and horizontal bar charts, `bar_label`, histograms, scatter plots, box plots, why to avoid pie charts
terms:
- **Bar chart:** bars whose lengths compare values across categories.
- **Histogram:** bars counting how many values fall in each range (bin), showing a distribution's shape.
- **Distribution:** how the values of a variable are spread out.
- **Scatter plot:** one dot per row, placed by two numbers, to show whether they're related.
- **Box plot:** a summary of a distribution: median, quartiles, typical range and outliers.
- **Correlation:** two variables tending to rise or fall together.
- **Causation:** one thing actually causing another. Correlation alone doesn't show it.
mistakes:
- Starting a bar chart's axis above zero, which exaggerates differences.
- Using a line chart for categories that have no order (like products). Lines imply a sequence; use bars.
- Reading a scatter plot as proof of cause and effect.

@@ pandas-plotting
topics: `Series.plot`, `kind=` and `.plot.bar()`-style shortcuts, plotting DataFrames, `plt.subplots(rows, cols)`, `ax=`, `sharey`, chart design habits
terms:
- **df.plot:** pandas' built-in charting, which draws with matplotlib.
- **Grouped bar chart:** bars for several series side by side, one group per category.
- **Stacked bar chart:** series stacked on top of each other in one bar.
- **Subplots:** several charts arranged in a grid in one figure.
- **sharey:** makes every subplot use the same y-axis scale.
- **tight_layout:** adjusts spacing so labels don't overlap.
- **Chart clutter:** anything on a chart that doesn't help the reader, like heavy grids or 3-D effects.
mistakes:
- Comparing subplots with different y scales. Use `sharey=True` when the charts measure the same thing.
- Letting pandas pick an unsorted category order. Sort the values (or use a meaningful order) before plotting.
- Using colour for decoration. Highlight the one thing that matters and keep the rest grey.

@@ final-project
topics: turning a brief into questions, joining and checking data, headline numbers, profit analysis, a dashboard, writing up findings, saving results
terms:
- **Brief:** the request that starts an analysis, often vague.
- **Revenue:** money from sales: units × price.
- **Profit:** revenue minus cost.
- **Margin:** profit as a percentage of revenue.
- **Seasonality:** a pattern that repeats at the same time each year.
- **Dashboard:** a few related charts shown together to answer a set of questions.
- **Write-up:** a short plain-language summary of findings and recommendations.
mistakes:
- Answering only the easy question (revenue) when the real one is about profit or customers.
- Sharing numbers you haven't re-checked against the output. One wrong figure costs a lot of trust.
- Burying the answer at the end of a long report. Put the finding first.
