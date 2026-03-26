from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank = True, null= True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default= 0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)  # gera o pk primeiro

        if not self.slug:
            self.slug = f'{slugify(self.nome)}-{self.pk}'
            
        # Se for produto simples e não tiver variação, cria uma automática
        if self.tipo == 'S' and not self.variacao_set.exists():
            from produto.models import Variacao 
            Variacao.objects.create(
                produto=self,
                nome="",
                preco=self.preco_marketing,
                preco_promocional=self.preco_marketing_promocional
            )

        super().save(*args, **kwargs)

        if self.imagem:
            self.resize_image(self.imagem, 800)

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)

        original_width, original_height = img_pil.size

        if original_width <= new_width:
            print('largura original < largura nova')
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

        print('img redimensionada')

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank= True, null= True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default = 0)
    estoque = models.PositiveIntegerField(default = 1)  

    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta: # correção plural no admin
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'