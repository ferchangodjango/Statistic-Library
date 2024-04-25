import pandas as pd
from bokeh.plotting import figure
from bokeh.models import Range1d,LinearAxis,ColumnDataSource,HoverTool
from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Dark2
import math
from scipy import stats
import numpy as np

def Pareto(DATA_FRAME,column_index,column_values,color="#9B59B6"):
    
    #Do pareto table.
    TOTAL=DATA_FRAME[column_values].sum()
    DATA_FRAME['Porcentaje']=100*(DATA_FRAME[column_values]/TOTAL)
    DATA_FRAME['Porcentaje_acumulado']=DATA_FRAME['Porcentaje'].cumsum()
    
    #Set pareto table how the source of next graphs.
    DataSourse=ColumnDataSource(DATA_FRAME)
    
    #Create the figure called figure 1
    figure1=figure(
        x_range=DATA_FRAME[column_index],title=column_values,
        plot_width=600,plot_height=450,
        tools='reset,box_zoom',toolbar_location='below'
        )
    
    #General sets, how label´s name, color´s grid etc.
    figure1.xgrid.grid_line_color=None
    figure1.xaxis.axis_label=column_index
    figure1.xaxis.major_label_text_font_size='15px'
    figure1.yaxis.axis_label="$"+column_values
    figure1.xgrid.grid_line_color=None
    figure1.ygrid.grid_line_alpha=0.7
    figure1.toolbar.autohide=True
    figure1.y_range.start = 0
    figure1.x_range.range_padding = 0.1
    figure1.xaxis.major_label_orientation = 1
    figure1.xgrid.grid_line_color = None
    
    # Create the seconde y axis for the % acumulate
    figure1.extra_y_ranges = {"y2": Range1d(start = 0, end = 110)}
    figure1.add_layout(LinearAxis(y_range_name = "y2"), 'right')
    
    #Create the Graphs
    figure1.vbar(
        x=column_index,top=column_values,
        width=0.9,fill_color=color,
        line_color="#2E4053",source=DataSourse
        )
    figure1.line(
        x=column_index,y='Porcentaje_acumulado',
        y_range_name='y2',source=DataSourse
        )
    figure1.scatter(
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
    return figure1


def barra_stackeada(DATA_FRAME,column_index,column_columns,column_values,color_list=[
            '#922B21','#B03A2E','#76448A','#6C3483',
            '#1F618D','#2874A6','#117864','#0B5345',
            '#196F3D','#7D6608','#6E2C00','#F5CBA7',
            '#85C1E9'
            ]):
    PRODUCTS=DATA_FRAME.groupby([column_index,column_columns])[column_values].sum()
    PRODUCTS_U=PRODUCTS.unstack(level=1,fill_value=0)
    PRODUCTS_U=PRODUCTS_U.reset_index()
    PRODUCTS_TOTAL=DATA_FRAME.groupby([column_index])[column_values].sum().reset_index()
    # UNION DE TABLAS
    TABLA_TOTAL=pd.merge(PRODUCTS_U,PRODUCTS_TOTAL)
    TABLA_TOTAL_SORT=TABLA_TOTAL.sort_values(by=column_values,ascending=False)
    sellers=list(TABLA_TOTAL_SORT[column_index])
    columns=list(TABLA_TOTAL_SORT.columns)
    figure1=figure(
        x_range=sellers,height=250,title=column_values,
        plot_width=1200,plot_height=800,
        tools='reset,box_zoom',toolbar_location='below',
        tooltips="$name @"+column_index+":@$name"
        )
    figure1.xgrid.grid_line_color=None

    figure1.xaxis.axis_label=column_index
    figure1.yaxis.axis_label='$'+column_values
    figure1.xaxis.major_label_text_font_size='15px'
    figure1.xgrid.grid_line_color=None
    figure1.ygrid.grid_line_alpha=0.7
    figure1.yaxis.major_label_text_font_size='15px'

    figure1.toolbar.autohide=True
    figure1.y_range.start = 0
    figure1.x_range.range_padding = 0.1
    figure1.xaxis.major_label_orientation = 1
    figure1.xgrid.grid_line_color = None
    figure1.vbar_stack(
        columns[1:-1],x=column_index, width=0.9,
        color=color_list,
        line_color="#17202A", 
        source=TABLA_TOTAL_SORT,legend_label=columns[1:-1])
    return figure1

#type=1
#type=0
def Box_Plot(DATA_FRAME,column_index,column_values,color_list=Dark2[7]):
    try:
        # Rename the columns
        df = DATA_FRAME[[column_index,column_values]].rename(columns={column_index: "kind"})
        #get a list of uniques kind
        kinds = df.kind.unique()
        # compute quantiles
        qs = df.groupby("kind")[column_values].quantile([0.25, 0.5, 0.75])
        qs = qs.unstack().reset_index()
        qs.columns = ["kind", "q1", "q2", "q3"]
        df = pd.merge(df, qs, on="kind", how="left")

        # compute IQR outlier bounds
        iqr = df.q3 - df.q1
        df["upper"] = df.q3 + 1.5*iqr
        df["lower"] = df.q1 - 1.5*iqr

        source = ColumnDataSource(df)

        p = figure(x_range=kinds, toolbar_location="below",
                title="BOX PLOT",
                background_fill_color="#eaefef", y_axis_label="MPG")
        # outlier range
        whisker = Whisker(base="kind", upper="upper", lower="lower", source=source)
        whisker.upper_head.size = whisker.lower_head.size = 20
        p.add_layout(whisker)
        cmap = factor_cmap("kind", color_list, kinds)
        p.vbar("kind", 0.7, "q2", "q3", source=source, color=cmap, line_color="black")
        p.vbar("kind", 0.7, "q1", "q2", source=source, color=cmap, line_color="black")

        # outliers
        outliers = df[~df[column_values].between(df.lower, df.upper)]
        p.scatter("kind",column_values, source=outliers, size=6, color="black", alpha=0.3)

        p.xgrid.grid_line_color = None
        p.axis.major_label_text_font_size="14px"
        p.axis.axis_label_text_font_size="12px"

        return p



    except:
        # Rename the columns
        df=DATA_FRAME
        df.loc[:,(column_index)]=column_index
        df =df[[column_index,column_values]].rename(columns={column_index: "kind"})
        #get a list of uniques kind
        kinds = df.kind.unique()
        # compute quantiles
        qs = df.groupby("kind")[column_values].quantile([0.25, 0.5, 0.75])
        qs = qs.unstack().reset_index()
        qs.columns = ["kind", "q1", "q2", "q3"]
        df = pd.merge(df, qs, on="kind", how="left")

        # compute IQR outlier bounds
        iqr = df.q3 - df.q1
        df["upper"] = df.q3 + 1.5*iqr
        df["lower"] = df.q1 - 1.5*iqr

        source = ColumnDataSource(df)

        p = figure(x_range=kinds, toolbar_location="below",
                title="BOX PLOT",
                background_fill_color="#eaefef", y_axis_label="MPG")
        # outlier range
        whisker = Whisker(base="kind", upper="upper", lower="lower", source=source)
        whisker.upper_head.size = whisker.lower_head.size = 20
        p.add_layout(whisker)
        cmap = factor_cmap("kind", color_list, kinds)
        p.vbar("kind", 0.7, "q2", "q3", source=source, color=cmap, line_color="black")
        p.vbar("kind", 0.7, "q1", "q2", source=source, color=cmap, line_color="black")

        # outliers
        outliers = df[~df[column_values].between(df.lower, df.upper)]
        p.scatter("kind", column_values, source=outliers, size=6, color="black", alpha=0.3)

        p.xgrid.grid_line_color = None
        p.axis.major_label_text_font_size="14px"
        p.axis.axis_label_text_font_size="12px"

        return p

def Q_Q_Graphs(Data,column,name,distribution,s=0.9,n=500,p=0.1,ancho=400,alto=400):
    figure_Q_Q=figure(title=name,plot_width=ancho,plot_height=alto)
    figure_Q_Q.xgrid.grid_line_color=None
    figure_Q_Q.ygrid.grid_line_alpha=0.7
    figure_Q_Q.xaxis.axis_label='Size'
    figure_Q_Q.yaxis.axis_label='Probability desity'
    figure_Q_Q.toolbar.autohide=True
    
    if distribution=='normal':
        
        Datos_Q_Q=Data[[column]].sort_values(by=column)
        Datos_Q_Q=Datos_Q_Q.reset_index(drop=True)
        Datos_Q_Q=Datos_Q_Q.reset_index()
        Datos_Q_Q['i']=Datos_Q_Q['index']+1
        Datos_Q_Q['j']=(Datos_Q_Q['i']-(1/2))/Datos_Q_Q['index'].count()
        Datos_Q_Q['Z']=stats.norm().ppf(Datos_Q_Q['j'])
        figure_Q_Q.y_range.start = Datos_Q_Q[column].min()
        figure_Q_Q.x_range.start = Datos_Q_Q['Z'].min()
        figure_Q_Q.scatter(Datos_Q_Q.Z,Datos_Q_Q[column])
        return figure_Q_Q

    elif distribution=='lognormal':
        Datos_Q_Q=Data[[column]].sort_values(by=column)
        Datos_Q_Q=Datos_Q_Q.reset_index(drop=True)
        Datos_Q_Q=Datos_Q_Q.reset_index()
        Datos_Q_Q['i']=Datos_Q_Q['index']+1
        Datos_Q_Q['j']=(Datos_Q_Q['i']-(1/2))/Datos_Q_Q['index'].count()
        Datos_Q_Q['Z']=stats.lognorm.ppf(Datos_Q_Q['j'],s)
        
        figure_Q_Q.y_range.start = Datos_Q_Q[column].min()
        figure_Q_Q.x_range.start = Datos_Q_Q['Z'].min()
        figure_Q_Q.scatter(Datos_Q_Q.Z,Datos_Q_Q[column])
        return figure_Q_Q
    
    elif distribution=='binomial':
        Datos_Q_Q=Data[[column]].sort_values(by=column)
        Datos_Q_Q=Datos_Q_Q.reset_index(drop=True)
        Datos_Q_Q=Datos_Q_Q.reset_index()
        Datos_Q_Q['i']=Datos_Q_Q['index']+1
        Datos_Q_Q['j']=(Datos_Q_Q['i']-(1/2))/Datos_Q_Q['index'].count()
        Datos_Q_Q['Z']=stats.binom.ppf(Datos_Q_Q['j'],n,p)
        figure_Q_Q.y_range.start = Datos_Q_Q[column].min()
        figure_Q_Q.x_range.start = Datos_Q_Q['Z'].min()
        figure_Q_Q.scatter(Datos_Q_Q.Z,Datos_Q_Q[column])
        return figure_Q_Q
        
#histogram_plot(Data,column,distribution,m=0,std=1)
#You need to pass the Data, column
#You can change the kind of distribution ['normal','lognormal','binomial']
#Scale for distribution lognormal
#n y p for distribution binomial



def histogram_plot(Data,column,name,distribution,m=0,std=1,s=0.9,n=500,p=0.1,ancho=400,alto=400):
    N=Data[column].count()
    figure_h=figure(title=name,plot_width=ancho,plot_height=alto,
               toolbar_location="below")
    figure_h.xgrid.grid_line_color=None
    figure_h.ygrid.grid_line_alpha=0.7
    figure_h.xaxis.axis_label=str(column)
    figure_h.yaxis.axis_label='Probability'
    figure_h.toolbar.autohide=True
    Number_intervals=int(round(1+3.322*math.log10(N),0))
    
    if distribution=='normal':
        hist,edges=np.histogram(Data[column],density=True,bins=Number_intervals)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.norm.pdf(x,m,std)
        # Histograma distribución normal
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Normal_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h 
        
    elif distribution=='lognormal':
        hist,edges=np.histogram(Data[column],density=True,bins=100)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.lognorm.pdf(x,s)
        #Histograma distribucion logonormal
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Logormal_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h
        
    elif distribution=='binomial':
        hist,edges=np.histogram(Data[column],density=True,bins=Number_intervals)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.binom.pmf(x,n,p)
        #Histograma distribucion binomial
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Binomial_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h
    
