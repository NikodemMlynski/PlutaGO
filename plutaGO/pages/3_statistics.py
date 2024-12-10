import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_palette('colorblind')
from controllers.ProductController import ProductController
from controllers.OrderPositionController import OrderPositionController
orderedProductsTab, ordersTab, categoriesTab, usersTab = st.tabs(['Products', 'Orders', 'Categories', 'Users']) 

def calculate_profit(products_df):
        """Calculates profit for each product in the DataFrame.

        Args:
            products_df (pandas.DataFrame): The DataFrame containing product data.

        Returns:
            pandas.DataFrame: A DataFrame with an additional 'profit' column.
        """

        products_df['amount'] = pd.to_numeric(products_df['amount'], errors='coerce')
        products_df['price'] = pd.to_numeric(products_df['price'], errors='coerce')
        products_df['profit'] = products_df['amount'] * products_df['price']
        return products_df

with orderedProductsTab:
    orderPositionController = OrderPositionController(db_path='plutaGO.db')
    order_positions = orderPositionController.get_all()
    productController = ProductController(db_path='plutaGO.db')
    products_df = pd.DataFrame([{"id": order_position.id, "amount": order_position.amount, **productController.get_product_by_id(order_position.product_id).__dict__} for order_position in order_positions])
    products_df = products_df[['id', 'amount', 'name', 'price']]
    products_df
    grouped_data = products_df.groupby('name')['amount'].sum()

    with st.container(border=True):
        grouped_data = products_df.groupby('name')['amount'].sum()
        st.subheader('Najczęściej kupowane produkty')

        # Create a bar chart using Streamlit's built-in chart
        st.bar_chart(grouped_data)
    
    with st.container(border=True):
        products_df = calculate_profit(products_df.copy())  

        grouped_profit = products_df.groupby('name')['profit'].sum()

        sorted_profit = grouped_profit.sort_values(ascending=False)

        top_n_profit = sorted_profit.head(3)
        bottom_n_profit = sorted_profit.tail(3)

        # Display headers
        st.subheader('Produkty o najwyższym zysku')
        st.bar_chart(top_n_profit)

        st.subheader('Produkty o najniższym zysku')
        st.bar_chart(bottom_n_profit)