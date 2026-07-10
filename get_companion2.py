import json
with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('step_index') in [2085, 2093, 2146]:
                for tool in data.get('tool_calls', []):
                    if tool.get('name') == 'multi_replace_file_content':
                        chunks = tool.get('args', {}).get('ReplacementChunks', '[]')
                        if isinstance(chunks, str):
                            chunks = json.loads(chunks)
                        for chunk in chunks:
                            print(chunk.get('ReplacementContent', '')[:100])
        except:
            pass
