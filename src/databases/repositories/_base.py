from typing import Type
from sqlalchemy.orm import Session
# from upatra.common.errors import UConflict, UNotFound, UUnprocessableEntity
from ..models.base import Base
from sqlalchemy import exc, and_, or_


class CRUD:
    session: Type[Session] = None
    model: Type[Base] = None

    def find_by_id(self, model_id):
        q = self.session.query(self.model).filter(self.model.id == model_id)
        return q.first()

    def find(self, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.all()

    def find_paging(self, limit=None, offset=None, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        if limit is not None and offset is not None:
            return query.count(), query.limit(limit).offset(offset).all()
        else:
            records = query.all()
            return len(records), records

    def first(self, **conditions):
        query = self.session.query(self.model)
        for key, value in conditions.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.model, key).in_(value))
                continue
            query = query.filter(getattr(self.model, key) == value)

        return query.first()

    def create(self, flush=True, mapping=None, **data):
        try:
            obj = self.model()
            for key in data:
                p = key
                if mapping and key in mapping:
                    p = mapping.get(key)

                if hasattr(obj, key):
                    setattr(obj, key, data[p])

            self.session.add(obj)
            if flush:
                self.session.flush()
            return obj
        except exc.IntegrityError as e:
            raise e
            # raise {
            #     '23503': UUnprocessableEntity,
            #     '23505': UConflict
            # }[e.orig.pgcode] or exc.IntegrityError

    def update(self, obj, flush=True, only=None, **data):
        if obj:
            for k in data:
                if hasattr(obj, k) and (only is None or k in only):
                    setattr(obj, k, data.get(k))
        if flush:
            self.session.flush()
        return obj

    def bulk_update(self, records):
        return self.session.bulk_update_mappings(self.model, records)

    def delete(self, obj, flush=True):
        try:
            self.session.delete(obj)
            if flush:
                self.session.flush()
            return True
        except exc.IntegrityError as e:
            raise e

    def list(self, request=None, **options):
        """
        :param request
        :param options:
                filters: [],

                matching(model, sa): a function return list in filter(*[])

                sort(model, sa): a function return list
                for order_by(*[user.name.desc()])

                sort_text: first_name:asc

                join(model, sa):

                search: function return list field to search

                search_text: search string

                pagination: True
        :return:
        """

        # for key, obj in options:
        #     options[key] = obj(self.model, sa) \
        #         if isinstance(obj, types.FunctionType) else obj

        data = self.session.query(self.model)

        if 'outerjoin' in options and options['outerjoin']:
            for j in options['outerjoin']:
                data = data.outerjoin(*j)

        if 'join' in options and options['join']:
            for j in options['join']:
                data = data.join(*j)

        filters = []

        has_search = ('search_text' in options
                      and 'search' in options
                      and options['search'])
        if has_search:
            search = []
            text = options['search_text'].split(
            ) if options['search_text'] is not None else []

            for field in options['search']:
                for i in [field.ilike('%' + t + '%') for t in text]:
                    search.append(i)
            if len(search) > 0:
                filters.append(or_(*search))

        # use key, value in dict as options to match extractly between key and
        # attr in model
        for key, value in options.items():
            if hasattr(self.model, key):
                filters.append(and_(getattr(self.model, key) == value))

        # add filters use lambda
        if 'matching' in options and len(options['matching']):
            filters.extend(options['matching'])

        # add filter use list
        if 'filters' in options and len(options['filters']):
            filters.extend(options['filters'])

        if len(filters) > 0:
            data = data.filter(*filters)

        has_sort = ('sort' in options
                    and 'sort_text' in options
                    and options['sort_text'])
        if has_sort:
            text = options['sort_text'].split('+')
            orders = []
            for t in text:
                key, by = t.split(':')
                key = options['sort'].get(key)
                if not key:
                    continue
                orders.append(getattr(key, by)())

            if len(orders):
                data = data.order_by(*orders)

        elif ('order' in options
              and options['order']
              and len(options['order']) > 0):
            data = data.order_by(*options['order'])

        # if request is not None or ('pagination' in options
        #  and options['pagination']):
        #     query_params = request.GET.mixed()

        #     page = 1
        #     if 'page' in query_params:
        #         page = query_params['page']

        #     def url_maker(next_page):
        #         # replace page param with values generated by paginator
        #         query_params['page'] = next_page

        #         return request.current_route_url(_query=query_params)

        #     return SqlalchemyOrmPage(
        #         data, page=page, items_per_page=10, url_maker=url_maker)

        return data
