from typing import Dict, List, Tuple, Optional
import jsonref


class OpenapiManager:
    def __init__(self,
                 list_operations_function_schema: dict,
                 get_operation_function_schema: dict,
                 openapi_files: Dict[str, str]):
        self.list_operations_function_schema = list_operations_function_schema
        self.get_operation_function_schema = get_operation_function_schema
        self.list_operations_function_name = list_operations_function_schema["function"]["name"]
        self.get_operation_function_name = get_operation_function_schema["function"]["name"]

        self.openapi_files = openapi_files

    def list_operation_ids_and_summaries(self, api_name: str) -> List[Dict[str, str]]:
        """
        Retrieves a list of dictionaries containing 'operationId' and 'summary'.
        """
        file_path = self.openapi_files.get(api_name.replace(" ", "").lower())

        if not file_path:
            raise ValueError(f'API {api_name} not found')

        with open(file_path, 'r') as f:
            api_json = jsonref.load(f)

        valid_methods = {"get", "options", "head", "post", "put", "patch", "delete"}
        operation_list = []
        paths = api_json.get('paths', {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in valid_methods:
                    operation_id = details.get('operationId')
                    summary = details.get('summary', '').rstrip('\n')
                    if not summary:
                        summary = details.get('description', '')

                    if operation_id:
                        operation_list.append({operation_id: summary})
                    else:
                        raise ValueError(f'OperationId not found for {path} {method}')

        return operation_list

    def list_operation_ids(self, api_name: str) -> List[str]:
        """
        Retrieves a list of operation IDs.
        """
        file_path = self.openapi_files.get(api_name.replace(" ", "").lower())

        if not file_path:
            raise ValueError(f'API {api_name} not found')

        with open(file_path, 'r') as f:
            api_json = jsonref.load(f)

        valid_methods = {"get", "options", "head", "post", "put", "patch", "delete"}
        operation_ids = []
        paths = api_json.get('paths', {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in valid_methods:
                    operation_id = details.get('operationId')
                    if operation_id:
                        operation_ids.append(operation_id)
                    else:
                        raise ValueError(f'OperationId not found for {path} {method}')

        return operation_ids

    def get_operation_by_id(self, api_name: str, operation_id: str) -> Optional[Dict]:
        """
        Retrieves details of a path method, given an operationId.
        """
        file_path = self.openapi_files.get(api_name.replace(" ", "").lower())

        if not file_path:
            raise ValueError(f'API {api_name} not found')

        with open(file_path, 'r') as f:
            api_json = jsonref.load(f)

        valid_methods = {"get", "options", "head", "post", "put", "patch", "delete"}
        servers = api_json.get('servers', [])
        server_url = servers[0]['url'] if servers else "http://localhost"

        paths = api_json.get('paths', {})

        for path, methods in paths.items():
            path_parameters = methods.get("parameters", [])

            for method, details in methods.items():
                if method.lower() in valid_methods and details.get('operationId') == operation_id:
                    full_path = f"{server_url}{path}"

                    method_parameters = details.get("parameters", [])
                    parameters = list({p["name"]: p for p in path_parameters + method_parameters}.values())

                    request_body = details.get('requestBody', None)
                    if request_body:
                        content = request_body.get('content', {})
                        if 'application/json' in content:
                            request_body = {"content": {"application/json": content['application/json']}}
                        else:
                            request_body = None

                    operation_details = {
                        "path": full_path,
                        "method": method,
                        "operationId": operation_id,
                        "parameters": parameters,
                        "requestBody": request_body
                    }

                    return {k: v for k, v in operation_details.items() if v is not None}

        raise ValueError(f'OperationId not found for {api_name} {operation_id}')
