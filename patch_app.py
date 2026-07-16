import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Update setFlightState to call updateTimelineState(state)
js = js.replace(
    '''    // Render the custom content based on state
    renderFlightStateCard(state);''',
    '''    // Render the custom content based on state
    renderFlightStateCard(state);
    
    // Update the timeline milestones
    if (typeof updateTimelineState === 'function') {
        updateTimelineState(state);
    }'''
)

# 2. Append new timeline functions
new_js = '''

// ==========================================================================
// TIMELINE LOGIC
// ==========================================================================

function toggleTimelineDrawer() {
    const drawer = document.getElementById('companionTimelineDrawer');
    const btn = document.getElementById('timelineToggleBtn');
    if (!drawer || !btn) return;
    
    if (drawer.style.height === '0px' || drawer.style.height === '') {
        const content = document.getElementById('verticalTimelineContent');
        drawer.style.height = content.offsetHeight + 'px';
        btn.classList.add('open');
        triggerHaptic('light', 'Timeline Expand');
    } else {
        drawer.style.height = '0px';
        btn.classList.remove('open');
        triggerHaptic('light', 'Timeline Collapse');
    }
}

function updateTimelineState(state) {
    // 5 Milestones: 
    // 1. Check-in (checkin_open, checked_in)
    // 2. Airport (airport_checkin, go_to_counter)
    // 3. Gate (gate_open, gate_update)
    // 4. Boarding (delayed could map here, or gate)
    // 5. Departed (cancelled could map to an error state)
    
    let activeNodeIndex = 1; // 1 to 5
    
    if (['checkin_open'].includes(state)) activeNodeIndex = 1;
    else if (['checked_in', 'airport_checkin', 'go_to_counter'].includes(state)) activeNodeIndex = 2;
    else if (['gate_open', 'gate_update'].includes(state)) activeNodeIndex = 3;
    else if (['delayed', 'baggage_tracking'].includes(state)) activeNodeIndex = 4;
    else if (['cancelled'].includes(state)) activeNodeIndex = 1; // reset or handle specially
    
    // Update horizontal nodes
    for (let i = 1; i <= 5; i++) {
        const node = document.getElementById('tlNode' + i);
        if (!node) continue;
        
        node.className = 'timeline-node'; // reset
        if (i < activeNodeIndex) {
            node.classList.add('completed');
        } else if (i === activeNodeIndex) {
            node.classList.add('active');
        }
    }
    
    // Update progress bar width
    const progress = document.getElementById('timelineProgress');
    if (progress) {
        // 5 nodes means 4 segments. 
        // Index 1 = 0%, Index 2 = 25%, Index 3 = 50%, Index 4 = 75%, Index 5 = 100%
        const percentage = ((activeNodeIndex - 1) / 4) * 100;
        progress.style.width = percentage + '%';
    }
    
    // Render vertical timeline content
    renderVerticalTimeline(activeNodeIndex, state);
    
    // Auto-adjust drawer height if it's currently open
    const drawer = document.getElementById('companionTimelineDrawer');
    if (drawer && drawer.style.height !== '0px' && drawer.style.height !== '') {
        setTimeout(() => {
            const content = document.getElementById('verticalTimelineContent');
            drawer.style.height = content.offsetHeight + 'px';
        }, 50);
    }
}

function renderVerticalTimeline(activeIndex, state) {
    const container = document.getElementById('verticalTimelineContent');
    if (!container) return;
    
    // Base data
    const milestones = [
        { time: '12:30', title: 'Check-in Opened', sub: '24 April' },
        { time: '14:00', title: 'Airport Arrival', sub: 'Bag drop counter 45' },
        { time: '15:15', title: 'Gate Open', sub: 'Gate 5B, Terminal 2' },
        { time: '16:00', title: 'Boarding', sub: 'Zones 1-3' },
        { time: '16:45', title: 'Departure', sub: 'On time' }
    ];
    
    // Modify labels based on specific states
    if (state === 'delayed') {
        milestones[3].sub = 'Estimated 17:30';
        milestones[4].sub = 'Delayed';
        milestones[4].time = '18:15';
    } else if (state === 'gate_update') {
        milestones[2].sub = 'Gate changed to 12C';
    }
    
    let html = '';
    milestones.forEach((m, i) => {
        let nodeClass = 'vertical-node';
        if (i < activeIndex - 1) nodeClass += ' completed';
        else if (i === activeIndex - 1) nodeClass += ' active';
        
        html += `
            <div class="${nodeClass}">
                <div class="time-label">${m.time}</div>
                <div class="v-node-icon"></div>
                <div class="event-label">
                    <div class="event-label-title">${m.title}</div>
                    <div class="event-label-sub">${m.sub}</div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}
'''

js += new_js

with open('app.js', 'w') as f:
    f.write(js)

print("App patched")
