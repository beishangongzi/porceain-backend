import sys

from drf_yasg import openapi

class LoginSchemas:
    phone = openapi.Parameter("phone", required=True, in_=openapi.IN_BODY,
                              description="user phone", type=openapi.TYPE_STRING)
    code = openapi.Parameter("code", required=True, in_=openapi.IN_BODY,
                             description="code", type=openapi.TYPE_STRING)
    def get_schemas(self):
        schemas = []
        co = self.__dir__()
        for var in co:
            if not var.startswith("__"):
                schemas.append(getattr(self, var))
        f_name = sys._getframe().f_code.co_name
        schemas.remove(getattr(self, f_name))
        return schemas


if __name__ == '__main__':
    a = LoginSchemas()
    print(a.get_schemas())
