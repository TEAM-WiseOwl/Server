import random
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import F, Sum

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_view(request, facility_id):
    # Facility 조회
    facility = get_object_or_404(Facility, pk=facility_id)
    
    # 모든 상품 가져오기
    products = Product.objects.filter(facility=facility)

    # 랜덤으로 5개 추천 상품 선택
    recommended_products = random.sample(list(products), min(5, len(products)))

    # 카테고리별로 상품을 그룹화
    categories = ProductCategory.objects.filter(facility=facility)
    products_by_category = []

    for category in categories:
        category_products = products.filter(product_category=category)
        product_list = ProductSerializer(category_products, many=True).data
        products_by_category.append({
            "product_category": category.product_category_name if category.product_category_name != 'ALL' else None,
            "product_list": product_list
        })

    # 모든 상품을 "all" 카테고리로 추가
    all_products = ProductSerializer(products, many=True).data
    products_by_category.insert(0, {
        "product_category": "ALL",
        "product_list": all_products
    })

    # 랜덤으로 선택된 추천 상품 직렬화
    recommended_products_data = ProductSerializer(recommended_products, many=True).data

    response_data = {
        "facility_num": facility.facility_id,
        "facility_name": facility.facility_name,
        "facility_loc": facility.facility_loc,
        "builidng_name": facility.building.building_name,  # Assuming Facility has a ForeignKey to Building
        "products_recommended": recommended_products_data,
        "products": products_by_category
    }
    print(products_by_category)
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def products_cart_view(request, product_id):
    print("products_cart_view 호출됨")

    user = request.user
    product = get_object_or_404(Product, pk=product_id)

    # 장바구니 생성 또는 가져오기
    cart, created = Cart.objects.get_or_create(user=user, defaults={"cart_price": 0})

    # CartProducts에 상품 추가 또는 수량 증가
    cart_product, created = CartProducts.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"product_cnt": 1}
    )

    if not created:
        # 이미 장바구니에 존재하는 경우 수량 증가
        cart_product.product_cnt = F('product_cnt') + 1
        cart_product.save()
        cart_product.refresh_from_db()

    # 장바구니 총 금액 업데이트
    cart.cart_price = CartProducts.objects.filter(cart=cart).aggregate(
        total_price=Sum(F('product__product_price') * F('product_cnt'))
    )['total_price'] or 0
    cart.save()

    # 성공 메시지 반환
    return Response({"message": "장바구니에 상품이 담겼습니다!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        return Response({"message": "장바구니가 비어있습니다.", "cart": [], "cart_price": 0})

    cart_products = CartProducts.objects.filter(cart=cart).select_related('product')
    cart_price = cart_products.aggregate(
        total_price=Sum(F('product__product_price') * F('product_cnt'))
    )['total_price'] or 0

    serialized_cart_products = ProductCartSerializer(
        [cart_product.product for cart_product in cart_products], many=True
    ).data

    # 장바구니에 담긴 각 제품의 수량 추가
    for serialized_product, cart_product in zip(serialized_cart_products, cart_products):
        serialized_product['product_cnt'] = cart_product.product_cnt

    response_data = {
        "facility_id": cart_products.first().product.facility.facility_id if cart_products else None,
        "facility_name": cart_products.first().product.facility.facility_name if cart_products else None,
        "cart": serialized_cart_products,
        "cart_price": cart_price
    }
    return Response(response_data)