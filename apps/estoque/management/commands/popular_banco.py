from django.core.management.base import BaseCommand
from apps.estoque.models import Categoria, Marca, Fornecedor, Produto, MovimentacaoEstoque


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **kwargs):
        categorias_nomes = ['Cimento e Argamassa', 'Ferramentas', 'Hidráulica', 'Elétrica', 'Madeiras e Painéis']
        categorias = {nome: Categoria.objects.get_or_create(nome=nome)[0] for nome in categorias_nomes}

        marcas_nomes = ['Votorantim', 'Tigre', 'Tramontina', 'Eucatex', 'Schneider']
        marcas = {nome: Marca.objects.get_or_create(nome=nome)[0] for nome in marcas_nomes}

        fornecedor, _ = Fornecedor.objects.get_or_create(
            cnpj_cpf='12.345.678/0001-90',
            defaults={
                'nome_fantasia': 'Distribuidora Central',
                'telefone': '(35) 99999-0000',
                'email': 'contato@distribuidoracentral.com.br',
            }
        )

        produtos = [
            {
                'nome': 'Cimento CP II 50kg',
                'categoria': categorias['Cimento e Argamassa'],
                'marca': marcas['Votorantim'],
                'preco_venda': 42.90,
                'estoque_minimo': 20,
                'quantidade': 100,
            },
            {
                'nome': 'Argamassa AC-II 20kg',
                'categoria': categorias['Cimento e Argamassa'],
                'marca': marcas['Votorantim'],
                'preco_venda': 28.50,
                'estoque_minimo': 15,
                'quantidade': 80,
            },
            {
                'nome': 'Tubo PVC 100mm x 6m',
                'categoria': categorias['Hidráulica'],
                'marca': marcas['Tigre'],
                'preco_venda': 89.90,
                'estoque_minimo': 10,
                'quantidade': 40,
            },
            {
                'nome': 'Joelho PVC 90° 100mm',
                'categoria': categorias['Hidráulica'],
                'marca': marcas['Tigre'],
                'preco_venda': 12.50,
                'estoque_minimo': 20,
                'quantidade': 60,
            },
            {
                'nome': 'Martelo Cabo Madeira 27mm',
                'categoria': categorias['Ferramentas'],
                'marca': marcas['Tramontina'],
                'preco_venda': 54.90,
                'estoque_minimo': 5,
                'quantidade': 25,
            },
            {
                'nome': 'Chave de Fenda 6" Cabo Bi-material',
                'categoria': categorias['Ferramentas'],
                'marca': marcas['Tramontina'],
                'preco_venda': 18.90,
                'estoque_minimo': 10,
                'quantidade': 50,
            },
            {
                'nome': 'Disjuntor Monofásico 20A',
                'categoria': categorias['Elétrica'],
                'marca': marcas['Schneider'],
                'preco_venda': 32.00,
                'estoque_minimo': 15,
                'quantidade': 70,
            },
            {
                'nome': 'Painel MDF 15mm 1830x2750mm',
                'categoria': categorias['Madeiras e Painéis'],
                'marca': marcas['Eucatex'],
                'preco_venda': 210.00,
                'estoque_minimo': 5,
                'quantidade': 20,
            },
        ]

        for dados in produtos:
            quantidade = dados.pop('quantidade')
            produto, criado = Produto.objects.get_or_create(
                nome=dados['nome'],
                defaults={**dados, 'imagem_principal': ''}
            )
            if criado:
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='ENTRADA',
                    quantidade=quantidade,
                    custo_unitario=produto.preco_venda,
                    fornecedor=fornecedor,
                )
                self.stdout.write(f'  Criado: {produto.nome}')
            else:
                self.stdout.write(f'  Já existe: {produto.nome}')

        self.stdout.write(self.style.SUCCESS('Banco populado com sucesso.'))
