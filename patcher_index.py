import json
import os

with open('ios-wrapper/www/index.html', 'r') as f:
    content = f.read()

def apply_chunk(content, target, replacement, allow_multiple):
    if allow_multiple:
        return content.replace(target, replacement)
    else:
        if content.count(target) == 1:
            return content.replace(target, replacement)
        elif content.count(target) == 0:
            print("Target not found.")
            return content
        else:
            print("Multiple targets found, but allow_multiple is false.")
            return content

applied = 0
failed = 0

with open('/Users/nihardip/.gemini/antigravity/brain/e8a85984-df9d-4156-a649-673d547652a3/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    if call['name'] == 'multi_replace_file_content':
                        args = call.get('args', {})
                        if 'index.html' in str(args.get('TargetFile', '')):
                            for chunk in args.get('ReplacementChunks', []):
                                target = chunk.get('TargetContent', '')
                                replacement = chunk.get('ReplacementContent', '')
                                allow_mult = chunk.get('AllowMultiple', False)
                                new_content = apply_chunk(content, target, replacement, allow_mult)
                                if new_content != content:
                                    content = new_content
                                    applied += 1
                                else:
                                    failed += 1
                    elif call['name'] == 'replace_file_content':
                        args = call.get('args', {})
                        if 'index.html' in str(args.get('TargetFile', '')):
                            target = args.get('TargetContent', '')
                            replacement = args.get('ReplacementContent', '')
                            allow_mult = args.get('AllowMultiple', False)
                            new_content = apply_chunk(content, target, replacement, allow_mult)
                            if new_content != content:
                                content = new_content
                                applied += 1
                            else:
                                failed += 1
                    elif call['name'] == 'write_to_file':
                        args = call.get('args', {})
                        if 'index.html' in str(args.get('TargetFile', '')):
                            # This completely overwrites it, wait!
                            # Did we write_to_file on index.html?
                            pass
        except Exception as e:
            pass

print(f"Applied {applied} chunks to index.html, {failed} failed.")
with open('index_recovered.html', 'w') as f:
    f.write(content)
