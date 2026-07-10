with open('index.html', 'r') as f:
    content = f.read()

start_marker = '<!-- COMPANION CAB DEALS -->'
end_marker = '<!-- ==========================================================\n                     SCREEN 4: FLIGHT RESULTS'

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    # Extract the deals chunk
    # Wait, the closing of screenTrips is right before SCREEN 4?
    # Let's find the exact div closing screenTrips.
    # The deals chunk ends right before the closing div of screenTrips? No, screenTrips is empty now except for header and deals.
    # Actually, we can just extract from start_marker to the last </div> before end_marker.
    chunk = content[start_idx:end_idx].strip()
    # The chunk currently ends with </div>\n                    </div>
    # Let's strip trailing </div> tags that belong to screenTrips
    # If screenTrips is just header + deals, then it has a closing </div>.
    # We should leave one </div> to close screenTrips!
    # Let's find exactly `</div>\n    \n\n                    </div>` and cut there.
    
    # It's safer to just extract the chunk and print the last 100 characters to see.
    print(chunk[-200:])
else:
    print("Markers not found!")
