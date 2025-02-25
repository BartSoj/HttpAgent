from typing import Dict, List, Tuple, Optional
import jsonref


class OpenapiManager:
    def __init__(self, list_operations_function_name, get_operation_function_name, list_operations_function_schema,
                 get_operation_function_schema, openapi_files: Dict[str, str]):
        self.list_operations_function_name = list_operations_function_name
        self.get_operation_function_name = get_operation_function_name
        self.list_operations_function_schema = list_operations_function_schema
        self.get_operation_function_schema = get_operation_function_schema

        self.openapi_files = openapi_files

    def list_operation_ids_and_summaries(self, api_name: str) -> List[Dict[str, str]]:
        """
        Retrieves a list of dictionaries containing 'operationId' and 'summary'.
        """
        file_path = self.openapi_files.get(api_name.lower())

        if not file_path:
            return []

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
                        operation_list.append({"operationId": operation_id, "summary": summary})
                    else:
                        raise ValueError(f'OperationId not found for {path} {method}')

        return operation_list

    def get_operation_by_id(self, api_name: str, operation_id: str) -> Optional[Dict]:
        """
        Retrieves details of a path method, given an operationId.
        """
        file_path = self.openapi_files.get(api_name.lower())

        if not file_path:
            return None

        with open(file_path, 'r') as f:
            api_json = jsonref.load(f)

        valid_methods = {"get", "options", "head", "post", "put", "patch", "delete"}
        servers = api_json.get('servers', [])
        server_url = servers[0]['url'] if servers else "http://localhost"

        paths = api_json.get('paths', {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in valid_methods and details.get('operationId') == operation_id:
                    full_path = f"{server_url}{path}"

                    filtered_details = {
                        key: details[key]
                        for key in ["operationId", "parameters", "requestBody"]
                        if key in details
                    }

                    return {
                        "path": full_path,
                        "method": method.upper(),
                        "details": filtered_details
                    }

        return None
