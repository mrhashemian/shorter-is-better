import simplejson as json


class QueryBuilder:
    def __init__(self, table_name, schema_name=None, **params):
        self.schema_name = schema_name
        self.table_name = table_name
        self.params = {k: v for k, v in params.items() if v is not None}

    def get_table_name(self):
        if self.schema_name is not None:
            return f'"{self.schema_name}"."{self.table_name}"'
        else:
            return f'"{self.table_name}"'

    def get_values(self):
        result = []
        for item in self.params.values():
            if isinstance(item, str):
                item = item.replace("'", "''")
                result.append(f"'{item}'")
            elif isinstance(item, dict) or isinstance(item, list):
                result.append(f"'{json.dumps(item)}'")
            else:
                result.append(str(item))
        return result

    def get_keys(self):
        return [f"\"{a}\"" for a in self.params.keys()]

    def get_insert_query(self, return_values=None):
        result = f'insert into {self.get_table_name()} ({",".join(self.get_keys())}) values ({",".join(self.get_values())})'
        if return_values is not None:
            result = result + f" RETURNING {return_values}"
        return result
