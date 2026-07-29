import re

with open('app.js', 'r') as f:
    js = f.read()

# 1. Update setFlightState mapping
js = js.replace(
    "'connecting': 'btnStateConnecting',",
    "'connecting': 'btnStateConnecting',\n        'connection_risk': 'btnStateRisk',"
)

# 2. Update updateTimelineState activeNodeIndex
js = js.replace(
    "else if (['gate_open', 'gate_update', 'connecting'].includes(state)) activeNodeIndex = 3;",
    "else if (['gate_open', 'gate_update', 'connecting', 'connection_risk'].includes(state)) activeNodeIndex = 3;"
)

# 3. Update updateTimelineState horizontal node styling
node_styling = """        } else if (i === activeNodeIndex) {
            node.classList.add('active');
            if (state === 'missed_flight') {
                node.style.borderColor = '#ef4444';
                node.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.2)';
            } else {
                node.style.borderColor = '';
                node.style.boxShadow = '';
            }"""

new_node_styling = """        } else if (i === activeNodeIndex) {
            node.classList.add('active');
            if (state === 'missed_flight') {
                node.style.borderColor = '#ef4444';
                node.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.2)';
                node.innerHTML = `<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="margin-top:5px; margin-left:5px;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`;
            } else if (state === 'connection_risk') {
                node.style.borderColor = '#f97316';
                node.style.boxShadow = '0 0 0 3px rgba(249, 115, 22, 0.2)';
                node.innerHTML = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#f97316" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-top:4px; margin-left:4px;"><path d="M15 14c-2 0-3 2-3 4"></path><path d="M11.5 8c-.5-1.5-2-2.5-3.5-2.5-2.5 0-2.5 4 0 4 1.5 0 3-1 3.5-2.5z"></path><path d="M14 6c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2z"></path><path d="M21 16l-3.5-2-2-4.5"></path><path d="M3 19l4-3 1-4"></path></svg>`;
                node.classList.add('running-risk');
            } else {
                node.style.borderColor = '';
                node.style.boxShadow = '';
            }"""

js = js.replace(node_styling, new_node_styling)

# 4. Update timelineProgress background
progress_styling = """    const progress = document.getElementById('timelineProgress');
    if (progress) {
        // 5 nodes means 4 segments. 
        // Index 1 = 0%, Index 2 = 25%, Index 3 = 50%, Index 4 = 75%, Index 5 = 100%
        const percentage = ((activeNodeIndex - 1) / 4) * 100;
        progress.style.width = percentage + '%';
    }"""

new_progress_styling = """    const progress = document.getElementById('timelineProgress');
    if (progress) {
        const percentage = ((activeNodeIndex - 1) / 4) * 100;
        progress.style.width = percentage + '%';
        if (state === 'missed_flight') progress.style.background = '#ef4444';
        else if (state === 'connection_risk') progress.style.background = '#f97316';
        else progress.style.background = '';
    }"""
js = js.replace(progress_styling, new_progress_styling)

# 5. Update renderVerticalTimeline
vert_tl = """    // Modify labels based on specific states
    if (state === 'delayed') {
        milestones[3].sub = 'Estimated 17:30';
        milestones[4].sub = 'Delayed';
        milestones[4].time = '18:15';
    } else if (state === 'connecting') {
        milestones[2].title = 'Layover in DEL';
        milestones[2].sub = 'Arrived at Terminal 2';
        milestones[3].title = 'Boarding (Next Flight)';
        milestones[3].sub = 'Gate 22B, Terminal 2';
    } else if (state === 'missed_flight') {
        milestones[3].title = 'Missed Boarding';
        milestones[3].sub = 'Gates closed at 16:15';
    } else if (state === 'gate_update') {
        milestones[2].sub = 'Gate changed to 12C';
    }"""

new_vert_tl = """    // Modify labels based on specific states
    if (state === 'delayed') {
        milestones[3].sub = 'Estimated 17:30';
        milestones[4].sub = 'Delayed';
        milestones[4].time = '18:15';
    } else if (state === 'connecting') {
        milestones[2].title = 'Layover in DEL';
        milestones[2].sub = 'Arrived at Terminal 2';
        milestones[3].title = 'Boarding (Next Flight)';
        milestones[3].sub = 'Gate 22B, Terminal 2';
    } else if (state === 'missed_flight') {
        return container.innerHTML = `
            <div style="padding: 16px;">
                <div style="display: flex; gap: 16px; align-items: stretch; position: relative;">
                    <div style="width: 2px; background: #e2e8f0; position: absolute; left: 11px; top: 12px; bottom: 12px; z-index: 0;"></div>
                    <div style="display: flex; flex-direction: column; gap: 24px; width: 100%; position: relative; z-index: 1;">
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #cbd5e1; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #cbd5e1;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Arriving at BOM</div><div style="font-size: 11px; color: #10b981; font-weight: 600;">On time</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #334155;">09:15</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #ef4444; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #ef4444;">Missed Boarding</div><div style="font-size: 11px; color: #ef4444;">Gates closed at 10:10</div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
    } else if (state === 'connection_risk') {
        return container.innerHTML = `
            <div style="padding: 16px; background: #fff8f1; border-bottom: 1px solid rgba(249, 115, 22, 0.1);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                    <div style="font-size: 20px;">⚠️</div>
                    <div>
                        <div style="font-size: 14px; font-weight: 800; color: #c2410c;">Connection at risk!</div>
                        <div style="font-size: 11px; color: #ea580c; font-weight: 600;">You have 55 min to reach your next gate</div>
                    </div>
                </div>
                <div style="display: flex; gap: 16px; align-items: stretch; position: relative; margin-top: 24px;">
                    <div style="width: 2px; background: #e2e8f0; position: absolute; left: 11px; top: 12px; bottom: 12px; z-index: 0;"></div>
                    <div style="display: flex; flex-direction: column; gap: 24px; width: 100%; position: relative; z-index: 1;">
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #eab308; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #eab308;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Arriving at DEL</div><div style="font-size: 11px; color: #10b981; font-weight: 600;">On time</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #334155;">09:15</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #f97316; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #f97316;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Layover at DEL</div><div style="font-size: 11px; color: #64748b; font-weight: 500;">Terminal 2 ➔ T1</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #10b981; background: #ecfdf5; padding: 2px 6px; border-radius: 12px;">1h 45m</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 12px;">
                            <div style="width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 2px solid #ef4444; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"><div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div></div>
                            <div style="flex: 1; display: flex; justify-content: space-between; align-items: center;">
                                <div><div style="font-size: 13px; font-weight: 700; color: #334155;">Next: Depart DEL</div><div style="font-size: 11px; color: #64748b; font-weight: 500;">10:10</div></div>
                                <div style="font-size: 11px; font-weight: 700; color: #ef4444;">Gate 32</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
    } else if (state === 'gate_update') {
        milestones[2].sub = 'Gate changed to 12C';
    }"""
js = js.replace(vert_tl, new_vert_tl)


with open('app.js', 'w') as f:
    f.write(js)
print("updateTimelineState patched successfully")
