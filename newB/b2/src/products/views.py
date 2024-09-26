from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Product
from .scraper import scrape_and_save_product
import json
from drf_spectacular.utils import extend_schema
from AuthModel.models import user_credential


@extend_schema(
    methods=['POST'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'product_url': {
                    'type': 'string',
                    'minLength': 10,
                    'maxLength': 500,
                    'example': 'https://www.example.com/product-url'
                }
            },
            'required': ['product_url']
        }
    },
    responses={
        200: {
            'description': 'Product already exists.',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Product already exists!',
                        'data': {
                            'name': 'Product Name',
                            'description': 'Product Description',
                            'price': '100.00',
                            'image_url': 'https://www.example.com/image.jpg',
                            'product_url': 'https://www.example.com/product-url'
                        }
                    }
                }
            }
        },
        202: {
            'description': 'Scraping started. Try again later.',
            'content': {
                'application/json': {
                    'example': {'message': 'Scraping started. Please try again in 5 minutes.'}
                }
            }
        },
        400: {
            'description': 'Invalid request',
            'content': {
                'application/json': {
                    'example': {'error': 'No URL provided.'}
                }
            }
        }
    },
    description="Submit a product URL to scrape and save the product data to the database.",
    summary="Scrape product data"
)
@extend_schema(
    methods=['GET'],
    responses={
        200: {
            'description': 'List of all products',
            'content': {
                'application/json': {
                    'example': {
                        'products': [
                            {
                                'name': 'Product 1',
                                'description': 'Description of product 1',
                                'price': '100.00',
                                'image_url': 'https://www.example.com/product1.jpg',
                                'product_url': 'https://www.example.com/product1'
                            },
                            {
                                'name': 'Product 2',
                                'description': 'Description of product 2',
                                'price': '200.00',
                                'image_url': 'https://www.example.com/product2.jpg',
                                'product_url': 'https://www.example.com/product2'
                            }
                        ]
                    }
                }
            }
        },
        200: {
            'description': 'No products found',
            'content': {
                'application/json': {
                    'example': {'message': 'No products found.'}
                }
            }
        }
    },
    description="Retrieve all scraped products from the database.",
    summary="Get all products"
)
@extend_schema(
    methods=['DELETE'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'product_url': {
                    'type': 'string',
                    'example': 'https://www.example.com/product-url'
                }
            }
        }
    },
    responses={
        200: {
            'description': 'Product(s) deleted successfully.',
            'content': {
                'application/json': {
                    'example': {'message': 'All products deleted successfully.'}
                }
            }
        },
        404: {
            'description': 'Product not found',
            'content': {
                'application/json': {
                    'example': {'error': 'Product not found.'}
                }
            }
        },
        400: {
            'description': 'Invalid request',
            'content': {
                'application/json': {
                    'example': {'error': 'Invalid request.'}
                }
            }
        }
    },
    description="Delete a specific product or all products from the database.",
    summary="Delete products"
)
@api_view(['POST', 'GET', 'DELETE'])
@user_credential
def scrape_product(request):
    if request.method == 'POST':
        product_url = request.data.get('product_url')
        
        if not product_url:
            return JsonResponse({'error': 'No URL provided.'}, status=400)

        # Check if the product already exists in the database
        product = Product.objects.filter(product_url=product_url).first()
        if product:
            product_data = json.loads(product.json_data)
            return JsonResponse({
                'message': 'Product already exists!',
                'data': product_data
            }, status=200)

        # If product doesn't exist, start scraping in the background
        scrape_and_save_product(product_url)
        
        return JsonResponse({
            'message': 'Scraping started. Please try again in 5 minutes.'
        }, status=202)

    elif request.method == 'GET':
        # Retrieve all products
        products = Product.objects.all()
        if products:
            product_list = [
                {
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'image_url': product.image_url,
                    'product_url': product.product_url
                } for product in products
            ]
            return JsonResponse({'products': product_list}, status=200)
        else:
            return JsonResponse({'message': 'No products found.'}, status=200)

    elif request.method == 'DELETE':
        product_url = request.data.get('product_url')
        
        if product_url:
            # Delete specific product
            product = Product.objects.filter(product_url=product_url).first()
            if product:
                product.delete()
                return JsonResponse({'message': f'Product {product_url} deleted successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Product not found.'}, status=404)
        else:
            # Delete all products
            Product.objects.all().delete()
            return JsonResponse({'message': 'All products deleted successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
