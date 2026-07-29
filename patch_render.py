import re

with open('app.js', 'r') as f:
    js = f.read()

target = """    } else if (state === 'missed_flight') {
        html = `
            <div class="state-title-row">
                <span class="state-title" style="color: #ef4444;">Flight Missed</span>
                <span class="state-date" style="color: #ef4444;">Status: Closed</span>
            </div>
            <p class="state-desc" style="color: #991b1b; background: #fef2f2; padding: 12px; border-radius: 8px; border-left: 4px solid #ef4444; margin-top: 8px; margin-bottom: 12px; font-weight: 500;">
                You missed the boarding window for your connecting flight to London. Don't worry, let's look at Plan B.
            </p>
            <div class="action-row-buttons">
                <button class="btn-primary-action" style="background: #ef4444; border: none; width: 100%; justify-content: center;" onclick="alert('Fetching alternative flights and rebooking options...')">Explore Plan B Options</button>
            </div>
        `;
        triggerHaptic('heavy', 'Companion State: Missed Flight');
        triggerDynamicIsland('Missed Flight', 'Boarding closed', 'Error');"""

replacement = """    } else if (state === 'connection_risk') {
        html = `
            <div style="background: #fdf2f8; padding: 12px; border-radius: 12px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; margin-top: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #db2777; font-size: 16px;">❤️</span>
                    <div>
                        <div style="font-size: 12px; font-weight: 700; color: #1e293b;">We've informed the gate</div>
                        <div style="font-size: 10px; color: #64748b; font-weight: 500;">Priority boarding for you</div>
                    </div>
                </div>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#db2777" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </div>
            <button class="btn-primary-action" style="width: 100%; justify-content: center; background: transparent; border: 1px solid #ef4444; color: #ef4444;" onclick="triggerHaptic('medium', 'Directions')">Step-by-step directions</button>
        `;
        triggerHaptic('heavy', 'Companion State: Connection Risk');
        triggerDynamicIsland('Connection at risk', '55 min to reach your next gate', 'Warning');

    } else if (state === 'missed_flight') {
        html = `
            <div style="background: #ef4444; color: #fff; padding: 16px; border-radius: 16px; text-align: center; margin-bottom: 16px; margin-top: -10px;">
                <div style="font-size: 16px; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 4px;">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    Connection Missed
                </div>
                <div style="font-size: 11px; font-weight: 500; opacity: 0.9;">Don't worry, we're here for you ❤️</div>
            </div>
            <div style="font-size: 12px; font-weight: 700; color: #1e293b; margin-bottom: 4px;">What happened?</div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 16px; line-height: 1.4;">Your arrival was delayed.<br>We're arranging the best options.</div>

            <div style="font-size: 11px; font-weight: 700; color: #ef4444; margin-bottom: 8px;">Auto Rebooked For You</div>
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 16px;">
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: #1e293b; margin-bottom: 4px;">LKO ➔ LON</div>
                    <div style="font-size: 11px; color: #64748b;">25 Jun, 10:30 | Terminal 1</div>
                    <div style="font-size: 11px; font-weight: 700; color: #1e293b; margin-top: 4px;">XAir 1522</div>
                </div>
                <div style="font-size: 11px; font-weight: 700; color: #005eb8; cursor: pointer;">View details</div>
            </div>

            <div style="display: flex; gap: 8px; margin-bottom: 16px;">
                <button style="flex: 1; padding: 12px 8px; border-radius: 12px; background: #fff; border: 1px solid #e2e8f0; display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 10px; font-weight: 600; color: #334155; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#005eb8" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
                    Hotel<br>Voucher
                </button>
                <button style="flex: 1; padding: 12px 8px; border-radius: 12px; background: #fff; border: 1px solid #e2e8f0; display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 10px; font-weight: 600; color: #334155; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#005eb8" stroke-width="2"><path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path><line x1="6" y1="1" x2="6" y2="4"></line><line x1="10" y1="1" x2="10" y2="4"></line><line x1="14" y1="1" x2="14" y2="4"></line></svg>
                    Meal<br>Voucher
                </button>
                <button style="flex: 1; padding: 12px 8px; border-radius: 12px; background: #eff6ff; border: 1px solid #3b82f6; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; font-size: 12px; font-weight: 800; color: #005eb8; cursor: pointer;" onclick="alert('Viewing Plan-B rebooking options')">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#005eb8" stroke-width="2.5"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.2-1.1.5l-1.5 2c-.3.4-.2 1 .2 1.3L9 12l-5 5-3-1-1 1 3 4 4 3 1-1-1-3 5-5 2 6.6c.3.4.9.5 1.3.2l2-1.5c.3-.2.6-.6.5-1.1z"></path></svg>
                    Plan-B
                </button>
            </div>

            <div style="display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 600; color: #0f172a; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#10b981" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                Your bags are being transferred
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#10b981" stroke-width="3" style="margin-left: auto;"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </div>

            <div style="background: linear-gradient(90deg, #005eb8, #ef4444); border-radius: 24px; padding: 12px; display: flex; align-items: center; justify-content: space-between; cursor: pointer; margin-bottom: 8px;" onclick="toggleChat()">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 24px; height: 24px; background: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 800; color: #005eb8;">XAi</div>
                    <div style="color: #fff; font-size: 12px; font-weight: 700;">AI powered helpdesk</div>
                </div>
            </div>
        `;
        triggerHaptic('heavy', 'Companion State: Missed Flight');
        triggerDynamicIsland('Missed Flight', 'Boarding closed', 'Error');"""

if target in js:
    js = js.replace(target, replacement)
    with open('app.js', 'w') as f:
        f.write(js)
    print("renderFlightStateCard patched successfully")
else:
    print("Could not find target string in app.js")
