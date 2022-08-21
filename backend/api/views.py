import io

from django.db.models import Sum
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .mixins import ListRetrieveViewSet
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            Shopping, Tag)
from .serializers import (IngredientSerializer, RecipeFollowSerializer,
                          RecipeGetSerializer, RecipeSerializer, TagSerializer)
from .utils import delete, post


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Рецепт успешно удален',
                        status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action != 'create':
            return (IsAuthorOrReadOnly(),)
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'],)
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return post(request, pk, Favorite, RecipeFollowSerializer)
        return delete(request, pk, Favorite)

    @action(detail=True, methods=['POST', 'DELETE'],)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return post(request, pk, Shopping, RecipeFollowSerializer)
        return delete(request, pk, Shopping)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = RecipeIngredient.objects.filter(
            recipe__cart__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            amount_total=Sum('amount')
        ).order_by()
        font = 'Tantular'
        pdfmetrics.registerFont(
            TTFont('Tantular', 'Tantular.ttf', 'UTF-8')
        )
        buffer = io.BytesIO()
        pdf_file = canvas.Canvas(buffer)
        pdf_file.setFont(font, 24)
        pdf_file.drawString(
            150,
            800,
            'Список покупок:'
        )
        pdf_file.setFont(font, 14)
        from_bottom = 750
        for number, ingredient in enumerate(shopping_list, start=1):
            pdf_file.drawString(
                50,
                from_bottom,
                (f'{number}.  {ingredient["ingredient__name"]} - '
                 f'{ingredient["amount_total"]} '
                 f'{ingredient["ingredient__measurement_unit"]}')
            )
            from_bottom -= 20
            if from_bottom <= 50:
                from_bottom = 800
                pdf_file.showPage()
                pdf_file.setFont(font, 14)
        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping_list.pdf'
        )
