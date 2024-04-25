# In this library you can find 2 files.

The first file is the file is about the graphs.
# Graphs.
## Pareto graph.
The graphs than you cand find is the follow.

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/4cff954e-05ca-43c7-b4d4-fa079f88357d)

For make this kind of graph you need to following the next steps:
1. You need to define a DataFrame with the next structure. Note:"The data only are for this example, you cant get any data
  
```python
    
   >>>
   import pandas as pd
   data_frame=pd.DataFrame({
    'Products':['Orange','Orange','Orange','Aple','Aple','Banana','Banana','Banana','Banana','Aple'],
    'Profit':[100,200,300,800,300,100,200,300,400,300]})
   dataframe_pareto=data_frame.groupby(['Products'])['Profit'].sum().reset_index()
   dataframe_pareto
```
And when you data Frame take the follow structure, you can use the next function.

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/b5373544-c2b1-4407-bb9c-7e7607ed8a7d)


The functión is called "Pareto", and this function is in "Graphs.py",now we start explain how work this function.
```python
>>>
def Pareto(DATA_FRAME,column_index,column_values,color="#9B59B6")
"""
```
1. Functionality:Return a object type bokeh.plotting.figure.Figure, 
with this object you can show in the html page, or extract the sources, and components(
script,div,js_components,css_components) for render in a web page.
Arguments: For this function works,you need the following
2. dataframe,this data frame need to content a column with strings and a column with values.
3. column_index: this is a column than have strings, only strings
4. column_values: this is a column than have values, for make calcules
5. color: it need a color for the bars in the pareto, this color is in HEXADECIMAL format.

so, the way for use the function is the follow.
```python
>>>
  from Graphs import Pareto
  from bokeh.plotting import show
  
  pareto=Pareto(dataframe_pareto,'Products','Profit',color="#9B59B6")
  show(pareto)
```
## Stack graph
The follow graph is the Stack Graphs, and this look as the below graph.

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/88114eb3-deea-48e0-825b-6268ca9705a1)

Or this kind of graph

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/4ba182b4-e4fe-4051-bcb9-955516d6f9eb)

for can draw that kind of Graphs, you need to have a DataFrame with the follow structure
```python
>>>
import pandas as pd
data_frame=pd.DataFrame({
    'Products':['Orange','Orange','Orange','Aple','Aple','Banana','Banana','Banana','Banana','Aple'],
    'Profit':[100,200,300,800,300,100,200,300,400,300],
    'Seller':['Fernando','Saul','Fernando','Saul','Fernando','Saul','Fernando','Saul','Fernando','Saul']
})
```

And when you data Frame take the follow structure, you can use the next function.

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/d5090497-f110-4594-ae2b-762be5190578)

you can use the follow lines for draw the stack graphs.
```python
>>>
from Graphs import Pareto,barra_stackeada
from bokeh.plotting import show
stackbarr=barra_stackeada(dataframe_pareto,'Seller','Products','Profit',color_list=[
            '#922B21','#196F3D','#117864'])
```
The documentation for the function is the follow.

```python
>>>
2.-def barra_stackeada(DATA_FRAME,column_index,column_columns,column_values,color_list=[
            '#922B21','#B03A2E','#76448A','#6C3483',
            '#1F618D','#2874A6','#117864','#0B5345',
            '#196F3D','#7D6608','#6E2C00','#F5CBA7',
            '#85C1E9'
            ]):
```
1. Functionality:Return a object type bokeh.plotting.figure.Figure,
with this object you can show in the html page, or extract the sources, and components(
script,div,js_components,css_components) for render in a web page.
Arguments: For this function works, you need the following:

2. dataframe,this dataframe need to content 3 columns, a main column with strings, a second column
    with strings, and a third column with values.
3. column_index: this is a main column than have strings, only strings
4. column_columns: this is  second column than have strings, only strings
5. column_values: this is a column than have values, for make calcules
6. color_list: it need a color list for the stackbars, you concidere the same number of 
    colors than have the numer of unique elements of column_columns,this color is in HEXADECIMAL format,
    if you column_columns have 13 unique elements, you can use default list, but if is diferent,
    you need to define your own list.

## BoxPlot
![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/d45fa44c-6c8c-4193-8ce7-b692fc870966)

or this kind of graph

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/ced8440a-a65e-40f5-855a-03986a824cde)

for do this kind of graph you need a datafreme with a similar structure for StackBar, bur in this case you don´t need to do the Groupby
For example

```python
>>>
import pandas as pd
data_frame=pd.DataFrame({
    'Products':['Orange','Orange','Orange','Aple','Aple','Banana','Banana','Banana','Banana','Aple'],
    'Profit':[100,200,300,800,300,100,200,300,400,300],
    'Seller':['Fernando','Saul','Fernando','Saul','Fernando','Saul','Fernando','Saul','Fernando','Saul']
})

```
And you have your table with this structure, you can import the Box_Plot function

![image](https://github.com/ferchangodjango/Statistic-Library/assets/68520215/b551d593-c0a9-4065-92e1-aca4d7bd4e30)

```python
>>>
from Graphs import Pareto,barra_stackeada,Box_Plot
from bokeh.plotting import show
boxplot=Box_Plot(data_frame,'Seller','Profit')
show(boxplot)

```
The documentation for this function is the follow

```python
>>>
def Box_Plot(DATA_FRAME,column_index,column_values,type=1,color_list=Dark2[7])
```
1. Functionality:Return a object type bokeh.plotting.figure.Figure,
with this object you can show in the html page, or extract the sources, and components(
script,div,js_components,css_components) for render in a web page.
Arguments: For this function works, you need the following:

2. dataframe,this dataframe need to content 2 columns or 1 column, a main column with strings, a second column
    with values.
3. column_index: this is a main column than have strings, only strings
4. column_values: this is a column than have values, for make calcules
5. color_list: it need a color list for the stackbars, you concidere the same number of 
    colors than have the numer of unique elements of column_columns,this color is in HEXADECIMAL format,
    if you column_columns have 13 unique elements, you can use default list, but if is diferent,

