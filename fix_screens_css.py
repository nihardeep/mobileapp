with open('style.css', 'r') as f:
    css = f.read()

target_results = """#screenResults.active {
    display: flex;
    flex-direction: column;
    height: 100%;"""
replacement_results = """#screenResults.active {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    background: #F4F6F9;"""
css = css.replace(target_results, replacement_results)

target_passenger = """#screenPassenger {
    height: 100%;
    overflow-y: auto;"""
replacement_passenger = """#screenPassenger {
    min-height: 100%;
    background: #F4F6F9;
    overflow-y: auto;"""
css = css.replace(target_passenger, replacement_passenger)

with open('style.css', 'w') as f:
    f.write(css)
