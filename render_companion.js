    // Hide the search widget entirely when trip companion is loaded
    const searchWidget = document.getElementById('searchWidgetSection');
    if (searchWidget) searchWidget.style.display = 'none';
    
    // Expand the placeholder gap for the plane to fly in
    placeholder.style.height = '100px';
    placeholder.style.marginBottom = '16px';
    
    // Transform Recent Searches into Cab Deals
    const recentTitle = document.querySelector('#recentSearchesSection .recent-title');
    const recentGrid = document.getElementById('recentSearchesList');
    if (recentTitle) recentTitle.innerText = 'Cab Deals';
    
    if (recentGrid) {
        recentGrid.innerHTML = `
            <div style="display: flex; align-items: center; background: linear-gradient(135deg, #fff 0%, #f8fafc 100%); border-radius: 16px; padding: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: relative; overflow: hidden; width: 100%;">
                
                <!-- Animated Keychain SVG coming from left -->
                <div style="position: absolute; left: -100px; top: -10px; width: 60px; height: 120px; animation: slideInKeychain 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; transform-origin: top center; z-index: 2;">
                    <!-- Simple SVG representation of the G keychain -->
                    <svg viewBox="0 0 100 200" width="100%" height="100%">
                        <!-- Clip -->
                        <path d="M40 0 L60 0 L60 20 L40 20 Z" fill="#2c1815"/>
                        <path d="M50 20 L50 60" stroke="#94a3b8" stroke-width="4"/>
                        <circle cx="50" cy="55" r="10" fill="none" stroke="#94a3b8" stroke-width="3"/>
                        
                        <!-- Tag -->
                        <rect x="20" y="65" width="60" height="90" rx="8" fill="#e84b38" />
                        <!-- Hole -->
                        <circle cx="50" cy="75" r="4" fill="#f8fafc" />
                        
                        <!-- G Logo inside -->
                        <path d="M 50 95 C 40 95 32 103 32 115 C 32 127 40 135 50 135 C 57 135 63 131 66 125 L 56 125 C 54 128 52 130 50 130 C 44 130 39 125 39 115 C 39 105 44 100 50 100 C 55 100 59 104 60 110 L 68 110 C 66 98 59 95 50 95 Z" fill="#f8ecec"/>
                        <circle cx="38" cy="118" r="4" fill="#f8ecec"/>
                        <rect x="52" y="115" width="16" height="5" fill="#f8ecec"/>
                        <rect x="63" y="115" width="5" height="20" fill="#f8ecec"/>
                    </svg>
                </div>

                <div style="flex: 1; padding-left: 70px; z-index: 3;">
                    <div style="font-size: 15px; font-weight: 800; color: #0f172a; margin-bottom: 2px;">Airport to City</div>
                    <div style="font-size: 13px; font-weight: 600; color: #10b981;">20% OFF</div>
                </div>
                <div style="font-size: 28px; z-index: 3;">🚖</div>
            </div>
            
            <style>
                @keyframes slideInKeychain {
                    0% { left: -100px; transform: rotate(30deg); }
                    60% { left: 10px; transform: rotate(-10deg); }
                    80% { left: 10px; transform: rotate(5deg); }
                    100% { left: 10px; transform: rotate(0deg); }
                }
            </style>
        `;
    }
