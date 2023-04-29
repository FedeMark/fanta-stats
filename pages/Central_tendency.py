import streamlit as st
import altair as alt
import pandas as pd
from utils.const import DATA_PATH, PRIMARY_COLOR, GRAPHIC_PATH
from PIL import Image
from utils.utils import add_sidebar_links


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

    st.write("The (arithmetic) mean is the most common measure of central tendency.")
    st.latex(
        r"""
    \bar{x} = \frac{(x_1 + x_2 + x_3 + \cdots + x_{n-1} + x_n)}{n} = \sum_{i=1}^{n} x_i
    """
    )
    st.write(
        "This measure has the problem to be very sensible to outliers. For example, "
        + "even for Oshimen, a hat-trick is an exceptionality; so we should not consider the 17.5 "
        + "the striker scored against Sassuolo on October 29."
    )

    data["outlier"] = data.FV > 16

    data_dist_out = (
        alt.Chart(data=data)
        .mark_bar()
        .encode(
            x=alt.X("FV", bin=False),
            y="count()",
            color=alt.Color(
                "outlier",
            ),
        )
        .properties(width=600)
    )

    cols = st.columns([0.1, 0.8, 0.1])
    cols[1].altair_chart(data_dist_out)


def plot_median(data):
    data_dist = get_distribution_chart(data)
    mean_line = (
        alt.Chart(pd.DataFrame({"x": [data.FV.median()]}))
        .mark_rule(color=PRIMARY_COLOR, strokeWidth=4)
        .encode(x="x")
        .properties(width=600)
    )
    cols = st.columns([0.1, 0.8, 0.1])
    cols[1].altair_chart(data_dist + mean_line)

    st.write(
        """
    The process to extract the median is very simple:
    1. order the scores of Victor Oshimen (samples of the distribution), getting a sequence
    2. the ***median*** is the central value of the sequence (if the number of samples is even, it's the mean between the two central values)
    """
    )
    st.write("By definition, the median is more robust to outliers than the mean.")


def plot_mode(data):
    data_dist = get_distribution_chart(data)
    mean_line = (
        alt.Chart(pd.DataFrame({"x": [data.FV.astype(float).mode().to_numpy()[0]]}))
        .mark_rule(color=PRIMARY_COLOR, strokeWidth=4)
        .encode(x="x")
        .properties(width=600)
    )
    cols = st.columns([0.1, 0.8, 0.1])
    cols[1].altair_chart(data_dist + mean_line)

    st.markdown(
        "The mode is typically less used and simply consists in the value that is more present among the samples."
    )


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
    cols = st.columns([0.1, 0.8, 0.1])
    cols[1].altair_chart(data_dist + mean_line)

    st.markdown(
        "This is an attempt to make the mean more robust to outliers. The idea is to "
        + "remove the more extreme values and compute the mean on the left ones."
    )


def main():
    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    st.set_page_config(page_icon=icon)

    st.header("Central tendency")
    st.write(
        "Let's use Victor Oshimen Fantacalcio scores (FV) as our distribution."
        + " This season (Seriea 2022-2023) his performances are amazing and surely worth a closer look."
    )
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

    add_sidebar_links()


if __name__ == "__main__":
    main()
