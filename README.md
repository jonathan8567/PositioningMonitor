# PositioningMonitor
The package used for positioning monitoring at Amundi

## Requirements
You may need to install a few packages first. 
* conda install -c conda-forge -c plotly jupyter-dash
* conda install -c conda-forge dash-bootstrap-components
* conda install plotly 
* conda install dash 



## How to start
Go to the Interactive folder and run PositioningMonitor Jupyter notebook and enter the fund code. 
```python
import os
os.getcwd()
os.chdir("Place where you save the package")
import Interactive.PositioningMonitor as PM

fund = input("Type FUND CODE then press Enter:  ")
PM.PositionReporting(fund).run_dash()    
```
After clicking the link that pops out, you will see below page:
![image](https://github.com/jonathan8567/PositioningMonitor/assets/139473310/70b36f3c-454f-4bcc-9607-a137332650da)

## How to use
It is very simple to use. You only needs to select what you are interested in. You can also select multiple line in a chart.

### Date
![image](https://github.com/jonathan8567/PositioningMonitor/assets/139473310/d34fc31a-b5c4-4d02-8e70-9b080c7b8088)
### Rates exposure (MD) + Maturity segments
![image](https://github.com/jonathan8567/PositioningMonitor/assets/139473310/5a17fc65-82fb-4aff-b7dd-25f6d6a32c96)
### Euro country exposure (MD) + Maturity segments
![image](https://github.com/jonathan8567/PositioningMonitor/assets/139473310/2832fec6-9fed-452b-b336-80d1d22f701f)
### FX exposure (%)
![image](https://github.com/jonathan8567/PositioningMonitor/assets/139473310/01cf607c-d3c8-438a-9a78-658ffc4ece4a)

### The charts are also interactive, which you are able to zoom in/out, change scales, and show hover window when you pointing to data point.
