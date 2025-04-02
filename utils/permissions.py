from rest_framework.permissions import DjangoModelPermissions


class CRUDModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class CRUDdDocumentPermissions(CRUDModelPermissions):
    def has_permission(self, request, view):
        if getattr(view, '_ignore_model_permissions', False):
            return True
        queryset = self._queryset(view)
        print('~~~' * 49)
        print(queryset.__dict__)
        print('~~~' * 49)
        perms = self.get_required_permissions(request.method, queryset._document)

        return request.user.has_perms(perms)

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.get('app_label'),
            'model_name': model_cls._meta.get('model_name')
        }

        if method not in self.perms_map:
            from rest_framework import exceptions
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

