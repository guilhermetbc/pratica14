from django.shortcuts import render, redirect
from django.views import View
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from . import models, forms
from django.contrib import messages


class ListaTesourosView(View):
    def get(self, request):
        lista_tesouros = models.Tesouro.objects.annotate(
            total=ExpressionWrapper(
                F('preco') * F('quantidade'),
                output_field=DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    blank=True
                )
            )
        ).all()
        return render(
            request,
            template_name='lista_tesouros.html',
            context=dict(
                lista_tesouros=lista_tesouros,
                total_geral=lista_tesouros.aggregate(Sum('total'))['total__sum']
            )
        )


class SalvarTesouroView(View):
    def get(self, request, pk=None):
        form = forms.TesouroForm()
        if pk:
            form = forms.TesouroForm(
                instance=models.Tesouro.objects.get(pk=pk)
            )
        return render(
            request,
            template_name='salvar_tesouro.html',
            context=dict(
                form=form,
                action=f'/edit/{pk}' if pk else 'new'
            )
        )

    def post(self, request, pk=None):
        form = forms.TesouroForm(
            request.POST,
            request.FILES,
            instance=models.Tesouro.objects.get(pk=pk) if pk else None
        )
        if form.is_valid():
            messages.add_message(
                request,
                messages.SUCCESS,
                'Tesouro atualizado com sucesso!' if pk else 'Tesouro criado com sucesso!'
            )
            form.save()
            return redirect('list')
        messages.add_message(
            request,
            messages.ERROR,
            'Erro ao criar o tesouro!' if pk else 'Erro ao editar o tesouro!'
        )
        return render(
            request,
            template_name='salvar_tesouro.html',
            context=dict(
                form=form,
                action=f'/edit/{pk}' if pk else 'new'
            )
        )


class DeletarTesouroView(View):
    def get(self, request, pk=None):
        models.Tesouro.objects.get(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Tesouro removido com sucesso!')
        return redirect('list')