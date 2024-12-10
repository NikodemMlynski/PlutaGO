import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from controllers.ProductController import ProductController
from controllers.OrderPositionController import OrderPositionController
orderedProductsTab, ordersTab, categoriesTab, usersTab = st.tabs(['Products', 'Orders', 'Categories', 'Users']) 

with orderedProductsTab:
    orderPositionController = OrderPositionController(db_path='plutaGO.db')
    order_positions = orderPositionController.get_all()
    productController = ProductController(db_path='plutaGO.db')
    # products = productController.get_all()
    products_df = pd.DataFrame([{"id": order_position.id, "amount": order_position.amount, **productController.get_product_by_id(order_position.product_id).__dict__} for order_position in order_positions])
    products_df = products_df[['id', 'amount', 'name', 'price']]
    products_df
    st.bar_chart(data=products_df)