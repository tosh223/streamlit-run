from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

row_size = 10000
graph_width = 750
bins = 20

def create_df():
    return pd.DataFrame(np.random.rand(row_size, 5), columns=['a', 'b', 'c', 'd', 'e'])

def show(df):
    # initialize
    header = 'Sample DataFrame'
    dt_now = datetime.now()
    dt_str = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    date_str = dt_now.strftime('%Y-%m-%d')
    time_str = dt_now.strftime('%H:%M:%S')
    selected_items = list(df.columns.values)
    histogram_mode = 'relative'
    details_window_length = 250
    multi_num = (0, row_size)

    # sidebar
    st.sidebar.button('Reload')
    is_checked = st.sidebar.checkbox('Select parameters', value=False)

    if is_checked:
        multi_num = st.sidebar.slider("Pick row range", 0, row_size, multi_num)
        selected_items = st.sidebar.multiselect('Select columns', list(df.columns.values), selected_items)
        histogram_mode = st.sidebar.selectbox('Select a histogram mode', ['relative', 'overlay'], index=0)

        with st.sidebar.beta_expander('Show others'):
            date_str = st.date_input("Pick a date")
            time_str = st.time_input("Pick a time")
            header = st.text_input("Write a header text", value=header)


    st.title('Hello, World!')

    col1, col2 = st.beta_columns(2)
    with col1:
        st.write(f'Now: {dt_str}')
    with col2:
        st.write(f'Selected: {date_str} {time_str}')

    st.header(header)
    df_filtered = df.loc[multi_num[0]:multi_num[1], selected_items]

    with st.beta_expander('Show describe'):
        st.dataframe(df_filtered.describe(), width=750, height=250)

    with st.beta_expander('Show details'):
        details_window_length = st.slider("Set window size", 0, 500, details_window_length)
        st.dataframe(df_filtered, width=750, height=details_window_length)

    st.header('Graphs')

    line_chart = px.line(df_filtered, width=graph_width, title='Line chart')
    st.write(line_chart)

    box_plot = px.box(df_filtered, y=list(df_filtered.columns), width=graph_width, title='Box plot')
    st.write(box_plot)

    histogram = px.histogram(df_filtered, nbins=bins, width=graph_width, opacity=0.5, barmode=histogram_mode, title=f'Histogram: {histogram_mode}')
    histogram.update_layout(bargap=0.1)
    st.write(histogram)

    scatter = px.scatter(df_filtered, width=graph_width, opacity=0.5, title='Scatter plot')
    st.write(scatter)

if __name__ == '__main__':
    show(create_df())
