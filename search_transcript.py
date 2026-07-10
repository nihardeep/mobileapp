import json
import re

with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'PLANNER_RESPONSE':
                for tool in data.get('tool_calls', []):
                    if tool.get('name') == 'multi_replace_file_content':
                        chunks = tool.get('args', {}).get('ReplacementChunks', '[]')
                        if isinstance(chunks, str):
                            chunks = json.loads(chunks)
                        for chunk in chunks:
                            rc = chunk.get('ReplacementContent', '')
                            if 'screenTrips' in rc or 'companion' in rc.lower():
                                print(f"Found in step {data.get('step_index')}")
                                print("--- CHUNK ---")
                                print(rc[:200])
                                print("-------------")
        except Exception as e:
            pass
