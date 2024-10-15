from django.contrib import messages
from django.shortcuts import redirect, render
from grillmaster.forms import SignUpForm, ContactForm
from django.contrib.auth import authenticate, login
from grillmaster.models import Categoria, Detalles_orden, Orden, Productos, Registro_cliente, Contacto
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .shopping_cart import ShoppingCart
from .context_processor import *
from .forms import ProductosForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from django.contrib.auth.views import PasswordResetView

def index(request):
    return render(request, 'index.html')

def aboutUs(request):
    return render(request, 'aboutUs.html')

def photoGallery(request):
    return render(request, 'photoGallery.html')

def contact(request):
    data ={
        'form' : ContactForm()
    }
    print(data['form'].fields['reason'].choices)

    if request.method=="POST":
        form= ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Formulario de contacto enviado correctamente")
            return redirect('index')
        data["form"] = form
    return render(request, 'contact.html', data)

def cart(request):
    return render(request, 'cart/cart.html')

def freeEat(request):
    return render(request, 'freeEat.html')

def registrar(request):
    data ={
        'form' : SignUpForm()
    }
    if request.method=="POST":
        formulario= SignUpForm(data=request.POST)
        if formulario.is_valid():
            user=formulario.save()
            genero=formulario.cleaned_data.get('genero')
            fecha_nac=formulario.cleaned_data.get('fecha_nac')
            Registro_cliente.objects.create(user=user, id_genero=genero, fecha_nac=fecha_nac)
            user=authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect('index')
        data["form"] = formulario
    return render(request, 'registration/registrar.html',data)

@staff_member_required
def management(request):
    return render(request, 'adminaccess/management.html')

def products(request):
    products = Productos.objects.all()
    
    search_query = request.GET.get('search')
    category_filter = request.GET.get('category')
    
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    if category_filter:
        products = products.filter(categoria__nombreCategoria=category_filter)
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'cart/shop.html', context)

def products_manage(request):
    products = Productos.objects.all()
    ctx = {
        'products': products 
    }
    return render(request, 'cart/product_manage.html', ctx)

@staff_member_required
def product_add(request):
    if request.method == "POST":
        form = ProductosForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_manage')
    else:
        form = ProductosForm()
    return render(request, 'cart/product_add.html', {'form': form})

@staff_member_required
def product_edit(request, id):
    product = Productos.objects.get(id=id)
    ctx = {
        'form': ProductosForm(instance=product),
        'id': id,
    }
    if request.method == "POST":
        form = ProductosForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_manage')
    return render(request, 'cart/product_edit.html', ctx)

@staff_member_required
def product_delete(request, id):
    product = Productos.objects.get(id=id)
    product.delete()
    return redirect('product_manage')

@login_required
def shopping_cart_open(request):
    page = get_page_number(request)
    request.session['cart_open'] = True
    return redirect(reverse('products') + '?page=' + str(page))

@login_required
def shopping_cart_close(request):
    page = get_page_number(request)
    request.session['cart_open'] = False
    return redirect(reverse('products') + '?page=' + str(page))

@login_required
def shopping_cart_add(request, id):
    page = get_page_number(request)
    shopping_cart = ShoppingCart(request)
    product = Productos.objects.get(id=id)

    if product.stock - shopping_cart.get_amount(product) <= 0:
        return redirect(reverse('products') + '?page=' + str(page))

    shopping_cart.add(product)
    return redirect(reverse('products') + '?page=' + str(page))

@login_required
def shopping_cart_substract(request, id):
    page = get_page_number(request)
    shopping_cart = ShoppingCart(request)
    product = Productos.objects.get(id=id)
    shopping_cart.substract(product)
    return redirect(reverse('products') + '?page=' + str(page))

@login_required
def shopping_cart_delete(request, id):
    page = get_page_number(request)
    shopping_cart = ShoppingCart(request)
    product = Productos.objects.get(id=id)
    shopping_cart.delete(product)
    return redirect(reverse('products') + '?page=' + str(page))

@login_required
def shopping_cart_clear(request):
    page = get_page_number(request)
    shopping_cart = ShoppingCart(request)
    shopping_cart.clear()
    return redirect(reverse('products') + '?page=' + str(page))

@login_required
def create_order(request):
    total = 0
    for key, value in request.session['shopping_cart'].items():
        total = total + int(value['price']) * int(value['amount'])
    if total <= 0:
        return redirect('products')
    shipping = calculate_shipping(total)
    taxes = calculate_taxes(total)
    orden = Orden(user = request.user, total = (total + shipping + taxes), shipping = shipping, taxes = taxes)
    orden.save()
    products = []
    for key, value in request.session['shopping_cart'].items():
        product = Productos.objects.get(id=key)
        amount = value['amount']
        if product.stock - amount < 0:
            continue
        product.stock = product.stock - amount
        subtotal = amount * int(product.price)
        detail = Detalles_orden(order_id = orden, product_id = product, amount = amount, subtotal = subtotal)
        detail.save()
        product.save()
        products.append(detail)
    ctx = {
        'products': products,
        'date': orden.date,
        'total': orden.total,
        'shipping': shipping,
        'taxes': taxes,
    }
    shopping_cart = ShoppingCart(request)
    shopping_cart.clear()
    return render(request, 'cart/order_details.html', ctx)

@login_required
def orders(request):
    orders = Orden.objects.filter(user=request.user).prefetch_related('detalles_orden__product_id').order_by('-date')
    ctx = {
        'orders': orders,
    }
    return render(request, 'cart/orders.html', ctx)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            registro_cliente = Registro_cliente.objects.get(user=user)
            registro_cliente.fecha_nac = form.cleaned_data['fecha_nac']
            registro_cliente.id_genero = form.cleaned_data['genero']
            registro_cliente.save()
            return redirect('show_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user/profile.html', {'form': form})

@login_required
def show_profile(request):
    user = request.user
    return render(request, 'user/show_profile.html', {'user': user})

def list_orders(request):
    orders = Orden.objects.select_related('user').prefetch_related('detalles_orden__product_id').order_by('-date')
    ctx = {'orders': orders}
    return render(request, 'adminaccess/list_orders.html', ctx)

def test_view(request):
    return render(request, 'test_template.html')

class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context