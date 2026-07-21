import json

import pytest
from system.tools import get_all_requests


class TestRequestStructures:

    def test_user_request_structures(self):
        all_requests = get_all_requests(package_name="repositories")
        errors = []

        for module_name, all_module_requests in all_requests.items():
            for sql_request_name, sql_request in all_module_requests.items():
                request = sql_request.get("request")
                rule = sql_request.get("allowedRolesRequester")

                if request is None:
                    errors.append(f"{module_name}.{sql_request_name} : 'request' manquant")
                if rule is None:
                    errors.append(f"{module_name}.{sql_request_name} : 'allowedRolesRequester' manquant")

        if errors:
            pytest.fail("Requêtes invalides :\n" + "\n".join(errors))

    # def test_system_request_structures(self):
    #     all_requests = get_all_requests(package_name="system")
    #     for sql_request in all_requests:
    #         request = sql_request.get("request")
    #         rule = sql_request.get("allowedRolesRequester")
    #         assert request is not None
    #         assert rule is not None