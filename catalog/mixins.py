class OwnerRequiredMixin:
    """Только владелец может получить доступ к объекту."""

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnerOrModeratorRequiredMixin:
    """Владелец или пользователь с правом на удаление."""

    permission = 'catalog.delete_product'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Модератор с правом на удаление видит все объекты
        if user.has_perm(self.permission):
            return queryset

        # Остальные — только свои
        return queryset.filter(owner=user)