import streamlit as st
from backend.database import *
from backend.queries import *

if __name__ == "__main__":
    st.title("Gestion des Films")
    db_mongo, mongo = init_mongo_connection()
    load_data(mongo)
    st.write(f"{query1(mongo)}")
