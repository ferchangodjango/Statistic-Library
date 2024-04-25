# In this library you can find 2 files.
The first file is the file is about the graphs.
The graphs than you cand find is the follow.

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/4cff954e-05ca-43c7-b4d4-fa079f88357d)

For make this kind of graph you need to following the next steps:
1. You need to define a DataFrame with the next structure. Note:"The data only are for this example, you cant get any data
  
   python
    ```
   >>>
   import pandas as pd
   data_frame=pd.DataFrame({
    'Products':['Orange','Orange','Orange','Aple','Aple','Banana','Banana','Banana','Banana','Aple'],
    'Profit':[100,200,300,800,300,100,200,300,400,300]})
   dataframe_pareto=data_frame.groupby(['Products'])['Profit'].sum().reset_index()
   dataframe_pareto
  ```

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/b5373544-c2b1-4407-bb9c-7e7607ed8a7d)
