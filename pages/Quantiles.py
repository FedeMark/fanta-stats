import streamlit as st
import altair as alt
import pandas as pd
from utils.const import DATA_PATH, PRIMARY_COLOR, GRAPHIC_PATH
from PIL import Image
from utils.utils import add_sidebar_links


def main():
    icon = Image.open(GRAPHIC_PATH / "logo-sfondo.png")
    st.set_page_config(page_icon=icon, layout="wide")

    st.header("Coming soon....")

    add_sidebar_links()


if __name__ == "__main__":
    main()
