import json
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Cucumbers', 'category': 'vegetable', 'quantity': 40},
    {'id': 2, 'name': 'Chicken thigh', 'category': 'poutry', 'quantity': 20},
    {'id': 3, 'name': 'Coffee beans', 'category': 'beverage', 'quantity': 0}
]

required_keys = {"id", "category", "name", "quantity"}

nextProductId = 4

@app.route('/')
def home():
    return render_template("home.html", data=products)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


@app.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({'error': 'Product does not exist'}), 404
    return jsonify(product)


def get_product(id):
    return next((e for e in products if e['id'] == id), None)


def product_is_valid(product):
    # Checks if the payload has all the required fields
    if not set(product.keys()).issubset(required_keys):
        return False
    return True


@app.route('/products', methods=['POST'])
def create_product():
    global nextProductId
    product = json.loads(request.data)
    if not product_is_valid(product) or any(product["name"] == p["name"] for p in products):
        return jsonify({'error': 'Invalid product properties.'}), 400

    product['id'] = nextProductId
    nextProductId += 1
    products.append(product)

    return jsonify(product), 201


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id: int):
    product = get_product(id)
    if product is None:
        return jsonify({'error': 'product does not exist.'}), 404

    updated_product = json.loads(request.data)
    if not product_is_valid(updated_product):
        return jsonify({'error': 'Invalid product properties.'}), 400

    product.update(updated_product)

    return jsonify(product)


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id: int):
    global products
    product = get_product(id)
    if product is None:
        return jsonify({'error': 'product does not exist.'}), 404

    products = [e for e in products if e['id'] != id]
    return jsonify(product), 200

if __name__ == '__main__':
    app.run(port=5000)