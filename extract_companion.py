import json

found_code = None

with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'PLANNER_RESPONSE':
                for tool in data.get('tool_calls', []):
                    if tool.get('name') == 'multi_replace_file_content':
                        chunks = tool.get('args', {}).get('ReplacementChunks')
                        if isinstance(chunks, str):
                            chunks = json.loads(chunks)
                        for chunk in chunks:
                            rc = chunk.get('ReplacementContent', '')
                            if 'renderCompanionState' in rc:
                                found_code = rc
                                break
        except Exception as e:
            pass
        if found_code:
            # We want the FIRST one we find that creates the function!
            if 'function renderCompanionState' in found_code:
                break

if found_code:
    with open('companion.html', 'w') as f:
        f.write(found_code)
    print("Extracted to companion.html")
else:
    print("Not found")
