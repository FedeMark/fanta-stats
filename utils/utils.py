import streamlit as st


def add_sidebar_links():
    st.sidebar.markdown("##")
    st.sidebar.markdown("##")

    st.sidebar.markdown(
        '<a href="https://www.instagram.com/sigmaeffe"><img alt="Instagram" src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width=40>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<a href="https://www.twitch.tv/sigmaeffe"><img alt="Twirch" src="https://upload.wikimedia.org/wikipedia/commons/c/ce/Twitch_logo_2019.svg" width=80>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<a href="https://it.tipeee.com/sigmaeffe"><img alt="Tipeee" src="https://cdn.cdnlogo.com/logos/t/21/tipeee.svg" width=80>',
        unsafe_allow_html=True,
    )
