import streamlit as st
import altair as alt
import pandas as pd
from utils.const import DATA_PATH, PRIMARY_COLOR


def get_distribution_chart(data):
    data_dist = (
        alt.Chart(data=data).mark_bar().encode(x=alt.X("FV", bin=False), y="count()")
    )

    return data_dist


def plot_mean(data):
    data_dist = get_distribution_chart(data)
    mean_line = (
        alt.Chart(pd.DataFrame({"x": [data.FV.mean()]}))
        .mark_rule(color=PRIMARY_COLOR, strokeDash=[15, 15], strokeWidth=4)
        .encode(x="x")
        .properties(width=600)
    )
    st.altair_chart(data_dist + mean_line)


def plot_median(data):
    data_dist = get_distribution_chart(data)
    mean_line = (
        alt.Chart(pd.DataFrame({"x": [data.FV.median()]}))
        .mark_rule(color=PRIMARY_COLOR, strokeWidth=4)
        .encode(x="x")
        .properties(width=600)
    )
    st.altair_chart(data_dist + mean_line)


def plot_mode(data):
    data_dist = get_distribution_chart(data)
    mean_line = (
        alt.Chart(pd.DataFrame({"x": [data.FV.astype(float).mode().to_numpy()[0]]}))
        .mark_rule(color=PRIMARY_COLOR, strokeWidth=4)
        .encode(x="x")
        .properties(width=600)
    )
    st.altair_chart(data_dist + mean_line)


def plot_trimmed_mean(data):
    percentage = (
        st.slider(
            label="Discarded percentage for each side",
            min_value=0,
            max_value=50,
            value=4,
        )
        / 100
    )
    p1 = data.FV.quantile(percentage)
    p2 = data.FV.quantile(1.0 - percentage)
    data["out"] = (data.FV < p1) | (data.FV > p2)
    data["opacity"] = data.FV.apply(lambda x: 1 if (x >= p1) and (x <= p2) else 0.2)

    data_dist = (
        alt.Chart(data=data)
        .mark_bar()
        .encode(
            x=alt.X("FV", bin=False),
            y="count()",
            opacity=alt.Opacity("opacity:N", legend=None),
        )
        .properties(width=600)
    )
    mean_line = (
        alt.Chart(pd.DataFrame({"x": [data[~data.out].FV.mean()]}))
        .mark_rule(color=PRIMARY_COLOR, strokeDash=[15, 15], strokeWidth=4)
        .encode(x="x")
    )
    st.altair_chart(data_dist + mean_line)


def main():
    st.write("Let's use Victor Oshimen Fantacalcio scores (FV) as our very variable.")
    oshimen_fv_df = pd.read_csv(DATA_PATH / "oshimen_fv.csv", index_col=0)

    st.sidebar.markdown("# Central tendency")
    measure_type = st.sidebar.selectbox(
        "Choose a central tendency measure:", ["Mean", "Median", "Mode", "Trimmed mean"]
    )

    st.header(measure_type)

    if measure_type == "Mean":
        plot_mean(oshimen_fv_df)
    elif measure_type == "Median":
        plot_median(oshimen_fv_df)
    elif measure_type == "Mode":
        plot_mode(oshimen_fv_df)
    elif measure_type == "Trimmed mean":
        plot_trimmed_mean(oshimen_fv_df)
    else:
        raise ValueError()
    st.sidebar.write(
        "Data from: [fantacalcio.it](https://www.fantacalcio.it/)",
    )


if __name__ == "__main__":
    main()
