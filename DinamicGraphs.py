from bokeh.layouts import column,gridplot
from bokeh.models import ColumnDataSource,CustomJS,Range1d,LinearAxis,HoverTool,NumeralTickFormatter,Slider,RangeTool
from bokeh.models.widgets import DataTable,TableColumn,Select
from bokeh.plotting import save, output_file,show,figure
import pandas as pd
import numpy as np


def DinamicSeriesTime(DataFrame,column_values,width=500,height=500):
    """ This function return a dinamic graph from timeseries,this is dinamic
    becouse you can get one filter for your graph"""

    #Define the sources
    sources=ColumnDataSource(DataFrame)
    original_sources=ColumnDataSource(DataFrame)

    #Define the figure(target object)
    figure1=figure(x_axis_type="datetime",title="Death for month for year",
            width=width,height=height,
            tools='reset,box_zoom',toolbar_location='below'
            )
    #Set the axis from the graphs
    figure1.xgrid.grid_line_color = None
    figure1.xaxis.major_label_orientation = 1
    #figure1.y_range.start=0
        
    #Create the Main Graph
    figure1.line(
        x='date',y=column_values,width=1,line_color="#a442f5",source=sources
        )
    
    #Define the part for select the graph
    select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=int(height/4),width=width, y_range=figure1.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

    #Create the secondary graph
    select.line(x='date',y=column_values, source=sources)
    #Set the axis
    select.ygrid.grid_line_color = None
    

    # Define the selector from the date    
    range_tool = RangeTool(x_range=figure1.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2
    
    #Add the tool from select
    select.add_tools(range_tool)
    
    #**Define the selectors
    Name_list=["ALL"]+DataFrame["name"].unique().tolist()
    Name_select=Select(title="State",value=Name_list[0],options=Name_list)

    #Define the callback from java script
    callback_changes_js="""
    var data=sources.data; //Get data
    var original_data=original_sources.data;
    var name_value=Name_select.value;
    console.log("Name"+name_value);
    for(var key in original_data){
        data[key]=[];
        for(var i=0; i < original_data['date'].length;++i){
            if(name_value === "ALL"||original_data['name'][i]===name_value){
                data[key].push(original_data[key][i]);
            }
        }
    }
    sources.change.emit();
    target_obj.change.emit();
    """
    #Create the generic_callback
    generic_callback=CustomJS(
    args=dict(sources=sources,
              original_sources=original_sources,
              Name_select=Name_select,
              target_obj=figure1),
    code=callback_changes_js        
    )

    
    
    #Define the action from the selectors
    Name_select.js_on_change('value',generic_callback)
    GraphTime=column(Name_select,figure1, select)
    return GraphTime

def ParetoDinamic(DATA_FRAME,column_index,column_values,color="#9B59B6",width=500,height=500,initial=5):
    """ This graph return a dinamic Pareto, you can choise the number of things than you want show
    in your graph"""
    #Do pareto table.
    TOTAL=DATA_FRAME[column_values].sum()
    DATA_FRAME=DATA_FRAME.sort_values(by=column_values,ascending=False)
    DATA_FRAME['Porcentaje']=100*(DATA_FRAME[column_values]/TOTAL)
    DATA_FRAME['Porcentaje_acumulado']=DATA_FRAME['Porcentaje'].cumsum()
    
    #Set pareto table how the source of next graphs.
    DataSourse=ColumnDataSource(DATA_FRAME)
    
    #Create the figure called figure 1
    figure1=figure(
        x_range=DataSourse.data[f"{column_index}"][:initial],title=column_values,
        width=width,height=height,
        tools='reset,box_zoom',toolbar_location='below'
        )
    
    #General sets, how label´s name, color´s grid etc.
    figure1.xgrid.grid_line_color=None
    figure1.xaxis.axis_label=column_index
    figure1.xaxis.major_label_text_font_size='15px'
    figure1.yaxis.axis_label=column_values
    figure1.xgrid.grid_line_color=None
    figure1.ygrid.grid_line_alpha=0.7
    figure1.toolbar.autohide=True
    figure1.y_range.start = 0
    figure1.x_range.range_padding = 0.1
    figure1.xaxis.major_label_orientation = 1
    figure1.xgrid.grid_line_color = None
    figure1.yaxis.formatter = NumeralTickFormatter(format="0,0")  # format y-axis ticks
    
    # Create the seconde y axis for the % acumulate
    figure1.extra_y_ranges = {"y2": Range1d(start = 0, end = 110)}
    figure1.add_layout(LinearAxis(y_range_name = "y2"), 'right')
    
    #Create the Graphs
    GRAPHBAR=figure1.vbar(
        x=column_index,top=column_values,
        width=0.9,fill_color=color,
        line_color="#2E4053",source=DataSourse
        )
    GRAPHLINE=figure1.line(
        x=column_index,y='Porcentaje_acumulado',
        y_range_name='y2',source=DataSourse
        )
    GRAPHSCATTER=figure1.scatter(
        x=column_index,y='Porcentaje_acumulado',
        y_range_name='y2',source=DataSourse)
    
    #Create the hover for can show the values of graph
    hover=HoverTool(
        tooltips=[
            (column_index,'@'+column_values),
            ('% profit acumulete','@Porcentaje_acumulado'), 
            ('% profit','@Porcentaje')]
            )
    figure1.add_tools(hover)
    
    number_slider = Slider(
        start=1,
        end=len(DataSourse.data[f"{column_index}"]),
        value=len(figure1.x_range.factors),
        title="Number of states",
    )

    custom_js = CustomJS(
        args={  # the args parameter is a dictionary of the variables that will be accessible in the JavaScript code
            "figure1": figure1, 
            "DataSourse": DataSourse.data[f"{column_index}"],
        },
        code="""
        figure1.title.text = "Top " + this.value + " states from USA";  
        figure1.x_range.factors = DataSourse.slice(0,this.value);
        """,
        )
    number_slider.js_on_change("value", custom_js)
    dinamicGraph = column([number_slider, figure1], sizing_mode="stretch_width")
    
    return dinamicGraph