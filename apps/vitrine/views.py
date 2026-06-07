from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from apps.estoque.models import Produto, Categoria
from apps.vitrine.models import Reserva, ItemReserva
from .forms import CadastroClienteForm
from django.contrib.auth.decorators import login_required

def catalogo(request):
    q = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')

    produtos = Produto.objects.all()

    if q:
        produtos = produtos.filter(nome__icontains=q)
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    for p in produtos:
        p.disponivel = p.quantidade_fisica - p.quantidade_reservada

    return render(request, 'vitrine/catalogo.html', {
        'produtos': produtos,
        'categorias': Categoria.objects.all(),
        'q': q,
        'categoria_selecionada': int(categoria_id) if categoria_id else None,
    })


def carrinho(request):

    carrinho = request.session.get('carrinho', {})

    produtos = []

    for produto_id, quantidade in carrinho.items():

        try:

            produto = Produto.objects.get(id=produto_id)

            produtos.append({
                'produto': produto,
                'quantidade': quantidade
            })

        except Produto.DoesNotExist:
            pass

    return render(
        request,
        'vitrine/carrinho.html',
        {'produtos': produtos}
    )


@login_required
def adicionar_carrinho(request, produto_id):

    produto = Produto.objects.get(id=produto_id)

    quantidade = int(request.POST.get('quantidade', 1))

    disponivel = produto.quantidade_fisica - produto.quantidade_reservada

    carrinho = request.session.get('carrinho', {})

    produto_id = str(produto_id)

    atual = carrinho.get(produto_id, 0)

    novo_total = atual + quantidade

    if novo_total > disponivel:
        novo_total = disponivel

    carrinho[produto_id] = novo_total

    request.session['carrinho'] = carrinho

    return redirect('catalogo')

@login_required
def remover_carrinho(request, produto_id):

    carrinho = request.session.get('carrinho', {})

    produto_id = str(produto_id)

    if produto_id in carrinho:
        del carrinho[produto_id]

    request.session['carrinho'] = carrinho

    return redirect('carrinho')


def checkout(request):

    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        return redirect('carrinho')

    reserva = Reserva.objects.create(
        cliente=request.user
    )

    for produto_id, quantidade in carrinho.items():

        try:

            produto = Produto.objects.get(id=produto_id)

            ItemReserva.objects.create(
                reserva=reserva,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco_venda
            )

        except Produto.DoesNotExist:
            pass

    request.session['carrinho'] = {}

    return render(
        request,
        'vitrine/checkout.html',
        {'reserva': reserva}
    )


def login_cliente(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(request, usuario)

            return redirect('catalogo')

    return render(request, 'vitrine/login.html')


def cadastro_cliente(request):

    if request.method == 'POST':

        form = CadastroClienteForm(request.POST)

        if form.is_valid():

            usuario = form.save(commit=False)

            usuario.role = 'CLIENTE'

            usuario.save()

            return redirect('login')

    else:

        form = CadastroClienteForm()

    return render(
        request,
        'vitrine/cadastro.html',
        {'form': form}
    )