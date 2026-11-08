"""Optional test-local newline JSON-RPC/MCP adapter; no credentials or network."""
import argparse
import json
import sys
from save_tool import SaveTool, SaveError

TOOL = {'name': 'save_record',
        'description': 'Save a complete Markdown record at an instance-authorized path and return the save result.',
        'inputSchema': {'type': 'object', 'properties': {'path': {'type': 'string'}, 'content': {'type': 'string'}},
                        'required': ['path', 'content'], 'additionalProperties': False}}


def dispatch(request, tool):
    method, params = request.get('method'), request.get('params', {})
    if not isinstance(params, dict):
        raise TypeError('params must be an object')
    if method == 'initialize':
        requested = params.get('protocolVersion', '2024-11-05')
        version = requested if requested in ('2024-11-05', '2025-03-26', '2025-06-18') else '2024-11-05'
        return {'protocolVersion': version, 'capabilities': {'tools': {}},
                'serverInfo': {'name': 'research-save-probe', 'version': '0.0.0-test'}}
    if method == 'ping':
        return {}
    if method == 'tools/list':
        return {'tools': [TOOL]}
    if method == 'tools/call':
        try:
            args = params.get('arguments', {})
            if params.get('name') != 'save_record' or set(args) != {'path', 'content'}:
                raise SaveError('unknown tool or invalid arguments')
            result, error = tool.save_record(**args), False
        except (SaveError, TypeError) as exc:
            result, error = {'written': getattr(exc, 'written', False), 'error': str(exc)}, True
        return {'content': [{'type': 'text', 'text': json.dumps(result, ensure_ascii=False)}], 'isError': error}
    raise ValueError('method not found')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--policy', required=True)
    args = parser.parse_args()
    with open(args.policy) as stream:
        tool = SaveTool(json.load(stream))
    for line in sys.stdin:
        request = None
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise TypeError('request must be an object')
            if 'id' not in request:
                continue
            reply = {'jsonrpc': '2.0', 'id': request['id'], 'result': dispatch(request, tool)}
        except (ValueError, TypeError) as exc:
            code = -32700 if request is None else (-32601 if isinstance(exc, ValueError) else -32600)
            reply = {'jsonrpc': '2.0', 'id': request.get('id') if isinstance(request, dict) else None,
                     'error': {'code': code, 'message': str(exc)}}
        print(json.dumps(reply, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
