# PositioningMonitor
The package used for positioning monitoring at Amundi

## Requirements
You may need to install a few packages first. 
* conda install -c conda-forge -c plotly jupyter-dash
* conda install -c conda-forge dash-bootstrap-components
* conda install plotly 
* conda install dash 



## How to use
Go to the Interactive folder and run PositioningMonitor Jupyter notebook and enter the fund code.
```python
import os
os.getcwd()
os.chdir("Place where you save the package")
import Interactive.PositioningMonitor as PM

fund = input("Type FUND CODE then press Enter:  ")
PM.PositionReporting(fund).run_dash()    
```
