import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken    
from .models import Category,Product,Cart,Favourite
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,FavouriteSerializer,RegisterSerializer

# Create your views here.
@api_view(['GET'])
def home(request):
    all_urls={
        'trending':'/shopkart/frontPage',
    }
    return Response(all_urls)

@api_view(['GET'])
def frontPage(request):
    trending=Product.objects.filter(quantity__gt=0,quantity__lte=100)
    if trending:
        result=ProductSerializer(trending,many=True)
        return Response(result.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
        'username':str(request.user.username),
    }
    return Response(content)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        print(refresh_token)
        # token = RefreshToken(refresh_token)
        # token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
           
# from django.contrib.auth.models import User
# from .serializers import RegisterSerializer
# from rest_framework import generics


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    registerData=request.data
    if registerData:
        result=RegisterSerializer(data=registerData)
        if result.is_valid():
            result.save()
            return Response(result.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def collections(request):
    collections=Category.objects.all()
    if collections:
        serializer=CategorySerializer(collections,many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([AllowAny])    
def products(request):
    category_id=request.data['category_id']
    products=Product.objects.filter(category=category_id)
    if products:
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])    
def category(request,id):
    catergory_details=Category.objects.get(pk=id)
    if catergory_details:
        serializer=CategorySerializer(catergory_details,many=False)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])    
def product_details(request,id):
    product_details=Product.objects.get(pk=id)
    if product_details:
        serializer=ProductSerializer(product_details,many=False)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def cart(request,id):
    current_user=request.user
    current_date_time=now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    if Cart.objects.filter(product=id).exists():
        return Response(status=status.HTTP_409_CONFLICT)
    cart_details={
        'product':id,
        'user':current_user.id,
        'product_qnty':request.data["product_qnty"],
        'created_at':current_date_time
    }
    print(cart_details)
    serializer=CartSerializer(data=cart_details)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def favourite(request,id):
    item=Favourite.objects.filter(product=id)
    if item.exists():
        return Response(status=status.HTTP_409_CONFLICT)
    else: 
        current_user=request.user
        current_date_time=now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
        
        cart_details={
            'product':id,
            'user':current_user.id,
            'created_at':current_date_time
        }
        print(cart_details)
        serializer=FavouriteSerializer(data=cart_details)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cartDetails(request):
    # cardProducts=[]
    # total={}
    # amount=0
    # cartProducts=Cart.objects.filter(user=request.user.id)
    # cartSerializer=CartSerializer(cartProducts,many=True)
    # for i in cartSerializer.data:
    #     cardProducts.append(Product.objects.get(id=i["product"]))
    # cardProductSerializer=ProductSerializer(cardProducts,many=True)
    # result=[0]*len(cardProductSerializer.data)
    # print(cartSerializer.data[0])
    # for i in range(0,len(cardProductSerializer.data)):
    #     amount+=cartSerializer.data[i].product_qnty*cardProductSerializer.data[i].selling_price
    #     total={'amount':amount}
    #     result[i]={**cartSerializer.data[i],**cardProductSerializer.data[i],**total}
    result2=[]
    carts=Cart.objects.all()
    result=CartSerializer(carts,many=True).data
    for i in result:
        products=Product.objects.get(pk=i["product"])
        productSer=(ProductSerializer(products).data)
        order_qnty={"order_qnty":i["product_qnty"]}
        result2.append({**productSer,**order_qnty})
    return Response(result2)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favouriteDetails(request):
    productSer=[]
    favourites=Favourite.objects.all()
    result=FavouriteSerializer(favourites,many=True).data
    for i in result:
        products=Product.objects.get(pk=i["product"])
        productSer.append(ProductSerializer(products).data)
    return Response(productSer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProductFromCart(request,id):
    cartItems=Cart.objects.all().exclude(product=id)
    item=Cart.objects.get(product=id)
    item.delete()
    
    if cartItems:
        serializer=CartSerializer(cartItems,many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

api_view(['DELETE'])
def deleteAllFavourite(request):
    Favourite.objects.all().delete()
    return Response(status=status.HTTP_200_OK)  

api_view(['DELETE'])
def deleteAllCart(request):
    Cart.objects.all().delete()
    return Response(status=status.HTTP_200_OK)  
