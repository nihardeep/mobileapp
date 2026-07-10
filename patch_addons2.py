with open('app.js', 'r') as f:
    content = f.read()

start_idx = content.find('function navigateToSeatmapAndMakeFree() {')
if start_idx != -1:
    end_idx = content.find('function showToast(', start_idx) # wait, where is the next function?
    if end_idx == -1:
        # Just find the end of the file or the next function
        end_idx = content.find('function ', start_idx + 10)
    
    if end_idx != -1:
        # replace everything from start_idx to end_idx with new function
        new_fn = """function navigateToSeatmapAndMakeFree() {
    if(typeof triggerHaptic === 'function') triggerHaptic('medium', 'Addons');
    if(typeof navigateTo === 'function') navigateTo('addons');
}

"""
        content = content[:start_idx] + new_fn + content[end_idx:]
        with open('app.js', 'w') as f:
            f.write(content)
        print("Patched navigateToSeatmapAndMakeFree!")
    else:
        print("End function not found")
else:
    print("Function not found")
