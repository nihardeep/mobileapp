import json

content = ""

with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            # Stop if we reach the step where we started making mistakes today
            if data['step_index'] >= 3010: # This is right around my bad inject today
                break
                
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    if call['name'] == 'write_to_file':
                        args = call.get('args', {})
                        if 'index.html' in str(args.get('TargetFile', '')):
                            content = args.get('CodeContent', '')
                            print(f"Loaded full file from step {data['step_index']}")
        except Exception:
            pass

with open('index_latest_write.html', 'w') as f:
    f.write(content)
