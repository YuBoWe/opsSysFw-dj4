import operator
from functools import reduce
from rest_framework import filters
from rest_framework.settings import api_settings
from mongoengine import Q
LOOKUP_SEP = '__'


class MongoSearchFilter(filters.BaseFilterBackend):
    mongo_search_param = 'search' # api_settings.SEARCH_PARAM
    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'mongo_search_fields', None)
        # search_fields指定查询字段们，假设为["label","name"]
        search_terms = request.query_params.get(self.mongo_search_param, '')
        # search_terms提取查询字符串中提交的查询参数，认为只有一个参数，不能用空格切分
        if not search_fields or not search_terms:
            return queryset
        # 从字段列表里面提取每一个字段名
        # 我们简单一点，不支持特殊字符，直接拼接icontains
        orm_lookups = [
            "{}{}{}".format(search_field, LOOKUP_SEP, "icontains")
            for search_field in search_fields
       ]
        # orm_lookups=["label_icontains", "name_icontains"]
        # base = queryset
        # conditions = []
        # 用Q封装后，用Or连接
        queries = [
            Q(**{orm_lookup: search_terms})
            for orm_lookup in orm_lookups
        ]
        print(queries, '@@@@@@@@@@@@@@@@@')
        # queries=[Q(label_icontains="adm"), Q(label_icontains="adm")]
        x = reduce(operator.or_, queries)  # 用|连接成一个 Q | Q
        print(x, '~~~~~~~~~~~~~~~~')
        queryset = queryset.filter(reduce(operator.or_, queries))
        print(queryset)  # mongoengine.queryset.queryset.QuerySet
        return queryset