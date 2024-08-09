'''
POST /products: Add a new product
GET /products: List all products
GET /products/{id}: Get product details
PUT /products/{id}: Update product details
DELETE /products/{id}: Delete a product
'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/product_service_db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mySuperSecretKey')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from services.productService import ProductService

@app.route('/product/set_product', methods=['POST'])
def createProduct():
    data = request.get_json()
    result = ProductService.createProduct(data)
    return jsonify(result), result['status']

@app.route('/product/all_products', methods=['GET'])
def get_products():
    result = ProductService.getProducts()
    return jsonify(result), result['status']

@app.route('/product', methods=['GET'])
def test():
    return "This is a product test!"