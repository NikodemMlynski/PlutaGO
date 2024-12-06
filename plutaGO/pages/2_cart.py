import streamlit as st
st.title('Cart')
st.write('Here replace this static content and write all products that are in cart state.')
st.write('In format like this [name, price, quantity]')
st.write('if you will have your work finished, delete this guidelines')
if "cart" not in st.session_state:
    pass
else:
    with st.container(border=True):
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Laptop')
        with col2:
            st.write(3000)
        with col3:
            st.write(3)

