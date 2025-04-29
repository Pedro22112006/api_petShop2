from flask import Flask, request, jsonify
from flask_jwt_extended import (
)


app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta-aqui'
jwt = (app)


products_db = [
    {
        "id": 1,
        "product_name": "Coleira",
        "product_description": "Coleira para cachorro de pequeno porte",
        "product_price": 23.90,
        "product_photo": "https://example.com/coleira.jpg",
        "stock_quantity": 26
    },
    {
        "id": 2,
        "product_name": "Ração para Gatos",
        "product_description": "Ração premium para gatos adultos",
        "product_price": 89.90,
        "product_photo": "https://example.com/racao-gato.jpg",
        "stock_quantity": 15
    },
    {
        "id": 3,
        "product_name": "Brinquedo para Cães",
        "product_description": "Brinquedo de borracha para cães de médio porte",
        "product_price": 35.50,
        "product_photo": "https://example.com/brinquedo-cao.jpg",
        "stock_quantity": 10
    },
    {
        "id": 4,
        "product_name": "Areia Sanitária",
        "product_description": "Areia higiênica para gatos",
        "product_price": 45.00,
        "product_photo": "https://example.com/areia-gato.jpg",
        "stock_quantity": 20
    },
    {
        "id": 5,
        "product_name": "Shampoo para Cães",
        "product_description": "Shampoo para cães de todos os portes",
        "product_price": 32.75,
        "product_photo": "https://example.com/shampoo-cao.jpg",
        "stock_quantity": 8
    }
]



@app.route('/login', methods=['POST'])
def login():

    access_token = create_access_token(identity='usuario_petshop')
    return jsonify({'access_token': access_token}), 200



@app.route('/products', methods=['GET'])
@jwt_required()
def list_products():
    try:

        preco_asc = request.args.get('preco_asc', '').lower() == 'true'
        preco_desc = request.args.get('preco_desc', '').lower() == 'true'
        description_part = request.args.get('description_part', '').lower()


        result_products = products_db.copy()


        if description_part:
            result_products = [p for p in result_products
                               if description_part in p['product_description'].lower()]


        if preco_asc:
            result_products.sort(key=lambda x: x['product_price'])
        elif preco_desc:
            result_products.sort(key=lambda x: x['product_price'], reverse=True)

        return jsonify(result_products), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/products/<int:product_id>', methods=['GET'])()
def get_product(product_id):
    try:
        product = next((p for p in products_db if p['id'] == product_id), None)
        if product:
            return jsonify(product), 200
        return jsonify({'error': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True)