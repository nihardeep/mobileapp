import json

found_html = None

with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    if call['name'] in ['multi_replace_file_content', 'replace_file_content']:
                        chunks = call.get('args', {}).get('ReplacementChunks', [])
                        if not chunks and 'ReplacementContent' in call.get('args', {}):
                            chunks = [call['args']]
                        if isinstance(chunks, str):
                            chunks = json.loads(chunks)
                        for chunk in chunks:
                            rc = chunk.get('ReplacementContent', '')
                            if 'id="screenGame"' in rc:
                                found_html = rc
                    elif call['name'] == 'write_to_file':
                        rc = call.get('args', {}).get('CodeContent', '')
                        if 'id="screenGame"' in rc:
                            # if it's the whole file we need to extract just the game screen
                            found_html = rc
        except Exception as e:
            pass

if found_html:
    with open('game_html.txt', 'w') as f:
        f.write(found_html)
    print("Extracted HTML!")
else:
    print("Not found")
