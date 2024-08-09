from flask import jsonify
from models.product import Product
from app import db

class ProductService:

    @staticmethod
    def createProduct(data):
        try:
            name = data.get('name')
            price = data.get('price')
            description = data.get('description')

            if not name or not price:
                return {'message': 'Name and Price are required', 'status': 400}
            
            newProduct = Product(name=name, price=price, description=description)

            db.session.add(newProduct)
            db.session.commit()

            return {'message': 'Product created successfully', 'status': 201}
        except Exception as e:
            return {'message': str(e), 'status': 500}
    
    @staticmethod
    def getProducts():
        try:
            products = Product.query.all()
            output = []
            for product in products:
                productData = {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description 
                }
                output.append(productData)
            return {'products': output, 'status':200}
        except Exception as e:
            return {'message': str(e), 'status':500}