import json

steps = [2431, 2514, 2565, 2741, 2774]
out = ""

with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('step_index') in steps:
                for tool in data.get('tool_calls', []):
                    if tool.get('name') == 'multi_replace_file_content':
                        chunks = tool.get('args', {}).get('ReplacementChunks', '[]')
                        if isinstance(chunks, str):
                            chunks = json.loads(chunks)
                        for chunk in chunks:
                            print(f"\n--- STEP {data.get('step_index')} TARGET ---")
                            print(chunk.get('TargetContent', ''))
                            print(f"\n--- STEP {data.get('step_index')} REPLACE ---")
                            print(chunk.get('ReplacementContent', ''))
        except:
            pass
