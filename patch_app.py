import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Update setFlightState mapping
mapping_old = """    const targetBtnId = {
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
        'baggage_tracking': 'btnStateBaggage'
    }[state];"""
js = js.replace(mapping_old, mapping_new)

# 2. Update renderFlightStateCard
render_old = """function renderFlightStateCard(state) {
    const container = document.getElementById('companionSubcardContent');
    if (!container) return;
    
    let html = '';
    
    if (state === 'checkin_open') {"""

render_new = """function renderFlightStateCard(state) {
    const container = document.getElementById('companionSubcardContent');
    if (!container) return;
    
    let html = '';
    
    if (state === 'upcoming_trip') {
        html = `
            <div class="state-title-row">
                <span class="state-title" style="color: #0f172a;">Upcoming Trip</span>
                <span class="state-date" style="color: #64748b;">15 Days to go</span>
            </div>
            <p class="state-desc" style="color: #475569; font-weight: 500;">
                Online check-in opens 48hrs before departure.
            </p>
            
            <div style="margin: 20px 0; display: flex; align-items: center; justify-content: space-between; position: relative;">
                <div style="position: absolute; top: 50%; left: 16px; right: 16px; height: 2px; background: #e2e8f0; transform: translateY(-50%); z-index: 1;"></div>
                <div style="position: absolute; top: 50%; left: 16px; width: 10%; height: 2px; background: var(--xairline-blue); transform: translateY(-50%); z-index: 2;"></div>
                
                <div style="z-index: 3; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 14px; height: 14px; border-radius: 50%; background: var(--xairline-blue); box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2);"></div>
                    <div style="font-size: 10px; font-weight: 700; color: var(--xairline-navy); margin-top: 6px; white-space: nowrap;">Booked</div>
                </div>
                
                <div style="z-index: 3; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #e2e8f0; border: 2px solid white;"></div>
                    <div style="font-size: 10px; font-weight: 600; color: #64748b; margin-top: 6px; white-space: nowrap;">Check-in (13 Days)</div>
                </div>
                
                <div style="z-index: 3; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #e2e8f0; border: 2px solid white;"></div>
                    <div style="font-size: 10px; font-weight: 600; color: #64748b; margin-top: 6px; white-space: nowrap;">Depart</div>
                </div>
            </div>

            <div class="action-row-buttons">
                <button class="btn-secondary-action" onclick="alert('Manage Booking clicked')" style="width: 100%; justify-content: center; background: #f8fafc; color: var(--xairline-navy); border: 1px solid #e2e8f0;">Manage Booking</button>
            </div>
        `;
        triggerHaptic('light', 'Companion State: Upcoming Trip');
        triggerDynamicIsland('Upcoming Trip', '15 days to go', 'Booked');
        
    } else if (state === 'checkin_open') {"""
js = js.replace(render_old, render_new)

# 3. Update updateTimelineState
timeline_old = """function updateTimelineState(state) {
    // 5 Milestones: """
timeline_new = """function updateTimelineState(state) {
    const header = document.getElementById('companionTimelineHeader');
    const drawer = document.getElementById('companionTimelineDrawer');
    
    if (state === 'upcoming_trip') {
        if (header) header.style.display = 'none';
        if (drawer) drawer.style.display = 'none';
        return;
    } else {
        if (header) header.style.display = 'flex';
        if (drawer) drawer.style.display = 'block';
    }

    // 5 Milestones: """
js = js.replace(timeline_old, timeline_new)

with open('app.js', 'w') as f:
    f.write(js)

print("Patch applied to app.js")
