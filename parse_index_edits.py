import json

edits = []
with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if 'tool_calls' in data:
            for call in data['tool_calls']:
                if call['name'] in ['multi_replace_file_content', 'replace_file_content', 'write_to_file']:
                    if 'index.html' in str(call.get('args', {})).lower():
                        edits.append({
                            'step_index': data['step_index'],
                            'created_at': data['created_at'],
                            'tool': call['name'],
                        })

print(f"Found {len(edits)} edits to index.html:")
for edit in edits:
    print(edit)
