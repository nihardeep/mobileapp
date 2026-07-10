import json

app_js_path = '/Users/nihardip/Desktop/Mobile design proptype/ios-wrapper/www/app.js'
with open(app_js_path, 'r') as f:
    content = f.read()

transcript_path = '/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl'

applied_count = 0
failed_count = 0

with open(transcript_path, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'PLANNER_RESPONSE':
                for tool in data.get('tool_calls', []):
                    if tool.get('name') == 'multi_replace_file_content':
                        args = tool.get('args', {})
                        if args.get('TargetFile', '').endswith('app.js'):
                            chunks = args.get('ReplacementChunks', '[]')
                            if isinstance(chunks, str):
                                chunks = json.loads(chunks)
                            
                            # Apply chunks in reverse order to avoid line drift
                            chunks = sorted(chunks, key=lambda x: x.get('StartLine', 0), reverse=True)
                            
                            for chunk in chunks:
                                target = chunk.get('TargetContent', '')
                                replacement = chunk.get('ReplacementContent', '')
                                
                                if target in content:
                                    content = content.replace(target, replacement, 1)
                                    applied_count += 1
                                else:
                                    failed_count += 1
        except Exception as e:
            pass

print(f"Applied: {applied_count}, Failed: {failed_count}")

with open('app_recovered.js', 'w') as f:
    f.write(content)
