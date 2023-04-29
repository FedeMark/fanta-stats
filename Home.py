from pathlib import Path

import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
from utils.utils import add_sidebar_links
from utils.const import (
    BACKGROUND_COLOR,
    SECONDARY_COLOR,
    PRIMARY_COLOR,
    GRAPHIC_PATH,
    RC,
)

page_bg = f"""
<style>
.stApp{{
background: rgb(2,0,36);
background: linear-gradient(165deg, rgba(2,0,36,1) 0%, rgba(35,0,148,1) 54%, rgba(12,250,202,1) 100%);
background-attachment: fixed;
backgroun-size: cover
}}
</style>
"""


def main():
    plt.rcParams.update(RC)

    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    high_icon = Image.open(GRAPHIC_PATH / "nome_logo_orizzontale.png")

    st.set_page_config(page_icon=icon, page_title="Fanta Stats")

    st.markdown(page_bg, unsafe_allow_html=True)

    cols = st.columns((0.1, 0.8, 0.1))
    cols[1].image(high_icon, use_column_width=False)

    # bottom_image = Image.open(GRAPHIC_PATH / "nome_logo_slogan_streamlit.png")

    st.header(
        "Do you want to learn simple statistic concepts with Fantacalcio (italian fantasty football)"
        + " data?"
    )
    st.subheader("You're in the right place!")
    st.write(
        "Have fun exploring the mini 'courses' with the navigation bar on the left."
    )

    add_sidebar_links()


if __name__ == "__main__":
    main()
