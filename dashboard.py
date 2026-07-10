import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd 
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent


def load_dataset(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    return pd.read_csv(uploaded_file, encoding="ISO-8859-1")


# Check if matplotlib is available for Styler.background_gradient
try:
    import matplotlib  # noqa: F401
    _HAS_MATPLOTLIB = True
except Exception:
    _HAS_MATPLOTLIB = False

st.set_page_config(page_title="Superstores!!!", page_icon=":BAR_CHART", layout="wide")

st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload your  file", type=["csv", "xlsx", "xls", "txt"])
if fl is not None:
    st.write(fl.name)
    df = load_dataset(fl)

else:
    df = pd.read_csv(BASE_DIR / "Superstore.csv", encoding= "ISO-8859-1")

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])


#Getting the min and max date

start_date = pd.to_datetime(df["Order Date"]).min()
end_date = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", start_date))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", end_date))

#Getting the data between the selected dates
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

#Create for Region
st.sidebar.header("Choose the filter: ")
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()

else:
    df2 = df[df["Region"].isin(region)]
                            
#Create for State
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()

else:
    df3 = df2[df2["State"].isin(state)]

#Create for City
city = st.sidebar.multiselect("Pick the City", df3["City"].unique())

#Filter the data based on Region, State and City
if not region and not state and not city:
    filtered_df = df

elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]

elif not region and not city:
    filtered_df = df[df["State"].isin(state)]

elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
    df4 = df3.copy()

elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]

elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]

elif city:
    filtered_df = df3[df3["City"].isin(city)]

else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()

with col1: 
    st.subheader("Category wise Sales")
    fig = px.bar(
        category_df,
        x="Category",
        y="Sales",
        text=[f"${x:,.2f}" for x in category_df["Sales"]],
        template="seaborn",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Region wise Sales")
    region = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
    fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig, use_container_width = True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category_ViewData"):
        if _HAS_MATPLOTLIB:
            st.write(category_df.style.background_gradient(cmap="Blues"))
        else:
            st.write(category_df)
        csv = category_df.to_csv(index = False).encode('utf-8') 
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
        
with cl2:
    with st.expander("Region_ViewData"):
        if _HAS_MATPLOTLIB:
            st.write(region.style.background_gradient(cmap="Oranges"))
        else:
            st.write(region)
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data in CSV file')

filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y = "Sales", labels = {"Sales": "Amount"}, height = 500, width=1000, template = "gridon")
st.plotly_chart(fig2, use_container_width = True)

with st.expander("View Data of TimeSeries"):
    if _HAS_MATPLOTLIB:
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
    else:
        st.write(linechart.T)
    csv = linechart.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime = "text/csv")


#Create a tream based on Region, category, sub-category 

st.subheader("Hieracal view of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Region", "Category", "Sub-Category"], values = "Sales", hover_data = ["Sales"],
                    color = "Sub-Category")

fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width = True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values="Sales", names = "Category", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig, use_container_width = True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df, values="Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig, use_container_width = True)

st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region", "State", "City", "Category", "Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width = True)

    st.markdown("Month wise sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"], 
                                       columns = "month")
    if _HAS_MATPLOTLIB:
        st.write(sub_category_Year.style.background_gradient(cmap="Blues"))
    else:
        st.write(sub_category_Year)

#Create a scatter plot
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1.update_layout(
    title=dict(
        text="Relationship between Sales and Profits using Scatter Plot.",
        font=dict(size=20),
    ),
    xaxis=dict(title=dict(text="Sales", font=dict(size=20))),
    yaxis=dict(title=dict(text="Profit", font=dict(size=20))),
)
st.plotly_chart(data1, use_container_width = True)

with st.expander("View Data"):
    if _HAS_MATPLOTLIB:
        st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Blues"))
    else:
        st.write(filtered_df.iloc[:500,1:20:2])

# Download at the end of the page
st.markdown("---")
st.subheader("Download Filtered Dataset")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data",
    data=csv,
    file_name="Superstore_filtered.csv",
    mime="text/csv",
    key="download_superstore_csv_bottom",
)
