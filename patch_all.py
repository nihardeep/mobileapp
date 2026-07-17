import re

# 1. Patch index.html
with open('index.html', 'r') as f:
    html = f.read()

# Insert the new dev console buttons
target_buttons = """                    <button class="dev-trigger-btn" id="btnStateStudentPersona" onclick="toggleStudentPersona()">
                        🎓 Student Persona
                        <div class="dev-btn-indicator"></div>
                    </button>"""
new_buttons = """                    <button class="dev-trigger-btn" id="btnStateConnecting" onclick="setFlightState('connecting')">
                        10. Layover
                        <div class="dev-btn-indicator"></div>
                    </button>
                    <button class="dev-trigger-btn" id="btnStateMissed" onclick="setFlightState('missed_flight')">
                        11. Missed Flight
                        <div class="dev-btn-indicator"></div>
                    </button>
                    <button class="dev-trigger-btn" id="btnStateStudentPersona" onclick="toggleStudentPersona()">
                        🎓 Student Persona
                        <div class="dev-btn-indicator"></div>
                    </button>"""
html = html.replace(target_buttons, new_buttons)

with open('index.html', 'w') as f:
    f.write(html)


# 2. Patch app.js
with open('app.js', 'r') as f:
    js = f.read()

# Update setFlightState mapping
mapping_old = """    const targetBtnId = {
        'upcoming_trip': 'btnStateUpcomingTrip',
        'checkin_open': 'btnStateCheckinOpen',
        'checked_in': 'btnStateCheckedIn',
        'gate_open': 'btnStateGateOpen',
        'airport_checkin': 'btnStateAirportCheckin',
        'go_to_counter': 'btnStateGoToCounter',
        'gate_update': 'btnStateGateUpdate',
        'delayed': 'btnStateDelayed',
        'cancelled': 'btnStateCancelled',
        'baggage_tracking': 'btnStateBaggage'
    }[state];"""
mapping_new = """    const targetBtnId = {
        'upcoming_trip': 'btnStateUpcomingTrip',
        'checkin_open': 'btnStateCheckinOpen',
        'checked_in': 'btnStateCheckedIn',
        'gate_open': 'btnStateGateOpen',
        'airport_checkin': 'btnStateAirportCheckin',
        'go_to_counter': 'btnStateGoToCounter',
        'gate_update': 'btnStateGateUpdate',
        'delayed': 'btnStateDelayed',
        'cancelled': 'btnStateCancelled',
        'baggage_tracking': 'btnStateBaggage',
        'connecting': 'btnStateConnecting',
        'missed_flight': 'btnStateMissed'
    }[state];"""
js = js.replace(mapping_old, mapping_new)

# Update renderFlightStateCard
render_old = """        triggerDynamicIsland('Check-in Open', 'Online check-in closes in 1h 10m', 'Check-in');
        
    } else if (state === 'baggage_tracking') {"""
render_new = """        triggerDynamicIsland('Check-in Open', 'Online check-in closes in 1h 10m', 'Check-in');
        
    } else if (state === 'connecting') {
        html = `
            <div class="state-title-row">
                <span class="state-title">Layover in Mumbai</span>
                <span class="state-date">Next flight in 2h 15m</span>
            </div>
            <p class="state-desc">Your flight to Goa boards at Gate 22B.</p>
            <div class="action-row-buttons">
                <button class="btn-primary-action" onclick="alert('Navigating to Gate 22B...')">Get Directions to Gate ➔</button>
            </div>
        `;
        triggerHaptic('light', 'Companion State: Connecting Flight');
        triggerDynamicIsland('Layover in BOM', 'Next flight to GOI in 2h 15m', 'Connecting');
        
    } else if (state === 'missed_flight') {
        html = `
            <div class="state-title-row">
                <span class="state-title" style="color: #ef4444;">Flight Missed</span>
                <span class="state-date" style="color: #ef4444;">Status: Closed</span>
            </div>
            <p class="state-desc" style="color: #991b1b; background: #fef2f2; padding: 12px; border-radius: 8px; border-left: 4px solid #ef4444; margin-top: 8px; margin-bottom: 12px; font-weight: 500;">
                You missed the boarding window for your flight to Mumbai. Don't worry, let's look at Plan B.
            </p>
            <div class="action-row-buttons">
                <button class="btn-primary-action" style="background: #ef4444; border: none; width: 100%; justify-content: center;" onclick="alert('Fetching alternative flights and rebooking options...')">Explore Plan B Options</button>
            </div>
        `;
        triggerHaptic('heavy', 'Companion State: Missed Flight');
        triggerDynamicIsland('Missed Flight', 'Boarding closed', 'Error');
        
    } else if (state === 'baggage_tracking') {"""
js = js.replace(render_old, render_new)

# Update updateTimelineState
timeline_old = """    if (['checkin_open'].includes(state)) activeNodeIndex = 1;
    else if (['checked_in', 'airport_checkin', 'go_to_counter'].includes(state)) activeNodeIndex = 2;
    else if (['gate_open', 'gate_update'].includes(state)) activeNodeIndex = 3;
    else if (['delayed', 'baggage_tracking'].includes(state)) activeNodeIndex = 4;
    else if (['cancelled'].includes(state)) activeNodeIndex = 1; // reset or handle specially"""
timeline_new = """    if (['checkin_open'].includes(state)) activeNodeIndex = 1;
    else if (['checked_in', 'airport_checkin', 'go_to_counter'].includes(state)) activeNodeIndex = 2;
    else if (['gate_open', 'gate_update', 'connecting'].includes(state)) activeNodeIndex = 3;
    else if (['delayed', 'baggage_tracking', 'missed_flight'].includes(state)) activeNodeIndex = 4;
    else if (['cancelled'].includes(state)) activeNodeIndex = 1; // reset or handle specially"""
js = js.replace(timeline_old, timeline_new)

# Update renderVerticalTimeline for missed_flight
render_vert_old = """    if (state === 'delayed') {
        milestones[3].sub = 'Estimated 17:30';
        milestones[4].sub = 'Delayed';
        milestones[4].time = '18:15';
    } else if (state === 'gate_update') {"""
render_vert_new = """    if (state === 'delayed') {
        milestones[3].sub = 'Estimated 17:30';
        milestones[4].sub = 'Delayed';
        milestones[4].time = '18:15';
    } else if (state === 'connecting') {
        milestones[2].title = 'Layover in BOM';
        milestones[2].sub = 'Arrived at Terminal 2';
        milestones[3].title = 'Boarding (Next Flight)';
        milestones[3].sub = 'Gate 22B, Terminal 2';
    } else if (state === 'missed_flight') {
        milestones[3].title = 'Missed Boarding';
        milestones[3].sub = 'Gates closed at 16:15';
    } else if (state === 'gate_update') {"""
js = js.replace(render_vert_old, render_vert_new)

# Apply red styling for missed flight on horizontal timeline node
timeline_nodes_old = """        if (i < activeNodeIndex) {
            node.classList.add('completed');
        } else if (i === activeNodeIndex) {
            node.classList.add('active');
        }"""
timeline_nodes_new = """        if (i < activeNodeIndex) {
            node.classList.add('completed');
        } else if (i === activeNodeIndex) {
            node.classList.add('active');
            if (state === 'missed_flight') {
                node.style.borderColor = '#ef4444';
                node.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.2)';
            } else {
                node.style.borderColor = '';
                node.style.boxShadow = '';
            }
        } else {
            node.style.borderColor = '';
            node.style.boxShadow = '';
        }"""
js = js.replace(timeline_nodes_old, timeline_nodes_new)

with open('app.js', 'w') as f:
    f.write(js)

print("Patch applied to index.html and app.js")
