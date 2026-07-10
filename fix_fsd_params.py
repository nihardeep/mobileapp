import re

with open('app.js', 'r') as f:
    js = f.read()

# Fix the template string parameters in renderFlightList and renderRecommendedFlight
js = js.replace(r"openFareSelectionDrawer(event, \'Economy\', \'${f.price}\', \'${f.airline} ${f.code}\', \'${f.depTime}\', \'${f.arrTime}\', \'${f.depCode}\', \'${f.arrCode}\', \'${f.duration}\')", 
                r"openFareSelectionDrawer(event, 'Economy', '${f.price}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')")

js = js.replace(r"openFareSelectionDrawer(event, \'Stretch\', \'${f.stretch || 28000}\', \'${f.airline} ${f.code}\', \'${f.depTime}\', \'${f.arrTime}\', \'${f.depCode}\', \'${f.arrCode}\', \'${f.duration}\')", 
                r"openFareSelectionDrawer(event, 'Stretch', '${f.stretch || 28000}', '${f.id}', '${f.from}', '${f.to}', 'DEL, T1', 'BOM, T2', '${f.dur}')")

with open('app.js', 'w') as f:
    f.write(js)

print("Fixed parameters in app.js")
