import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of bp-carousel-container and the end (where bp-dots starts)
pattern = re.compile(r'<!-- Carousel Container -->(.*?)<!-- Carousel Dots -->', re.DOTALL)

new_html = """<!-- Full Screen QR Modal -->
                        <div id="bpQrFullscreen" class="bp-qr-fullscreen" style="display: none;">
                            <div class="bp-qr-modal-content">
                                <div class="bp-qr-close" onclick="closeQRModal()">✕</div>
                                <div class="bp-qr-modal-title">Ready to Scan</div>
                                <img src="qr_code.png" class="bp-qr-modal-img" />
                                <div class="bp-qr-modal-subtitle" id="bpQrModalSubtitle">SEC. 6E2341:001 (LEG 1)</div>
                            </div>
                        </div>

                        <!-- Carousel Container -->
                        <div class="bp-carousel-container" id="bpCarousel">
                            <div class="bp-carousel-track" id="bpTrack">
                                
                                <!-- Passenger 1 -->
                                <div class="bp-slide">
                                    <div class="digital-bp">
                                        <!-- TOP: Boarding Pass Header & Barcode -->
                                        <div class="bp-top-section">
                                            <div class="bp-header">
                                                <div class="bp-title-small">Boarding pass</div>
                                                <div class="bp-pnr-tag">PNR X3K9P2</div>
                                            </div>
                                            
                                            <!-- 3D Flipping Barcode Container -->
                                            <div class="bp-qr-flipper-wrapper" onclick="openQRModal()">
                                                <div class="bp-qr-flipper" id="bpQrFlipper">
                                                    <div class="bp-qr-front">
                                                        <img src="qr_code.png" class="bp-barcode-img" />
                                                        <div class="bp-qr-subtitle">SEC. 6E2341:001</div>
                                                    </div>
                                                    <div class="bp-qr-back">
                                                        <img src="qr_code.png" class="bp-barcode-img" />
                                                        <div class="bp-qr-subtitle">SEC. 6E7892:002</div>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Passenger Name -->
                                            <div class="bp-passenger-name">SHARMA / RAVI</div>
                                        </div>

                                        <!-- TOGGLE BUTTONS (Only visible for multi-city) -->
                                        <div class="bp-leg-toggle multi-only" id="bpLegToggle">
                                            <div class="bp-toggle-btn active" onclick="flipToLeg(1)" id="btnLeg1">DEL ✈ BOM</div>
                                            <div class="bp-toggle-btn" onclick="flipToLeg(2)" id="btnLeg2">BOM ✈ GOI</div>
                                        </div>

                                        <!-- TIMELINE SECTION (Sliding wrapper) -->
                                        <div class="bp-timeline-wrapper">
                                            <div class="bp-timeline-slider" id="bpTimelineSlider">
                                                
                                                <!-- LEG 1 TIMELINE -->
                                                <div class="bp-timeline-leg">
                                                    <div class="bp-timeline-header">
                                                        <div class="bp-tl-flight">
                                                            <div class="lbl">Flight</div>
                                                            <div class="val">6E 2341</div>
                                                            <div class="lbl">25 MAR 2026</div>
                                                        </div>
                                                        <div class="bp-tl-route">
                                                            <div class="city">DEL</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">BOM</div>
                                                        </div>
                                                    </div>
                                                    <div class="bp-timeline-line">
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Bag drop-off limit</div>
                                                            <div class="time">17:25</div>
                                                            <div class="desc">Baggage: 15kg + 7kg cabin</div>
                                                        </div>
                                                        <div class="bp-tl-node active">
                                                            <div class="dot solid"></div>
                                                            <div class="title white">Boarding</div>
                                                            <div class="time white">22:00</div>
                                                            <div class="desc white">Gate 5B / Zone 02</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow red-dot"></div>
                                                            <div class="title blue">Gate closed</div>
                                                            <div class="time">22:25</div>
                                                            <div class="desc">Zone 02</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Seat</div>
                                                            <div class="time bold">12C</div>
                                                            <div class="desc">Economy (SSR: WCHR)</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Arrival</div>
                                                            <div class="time">00:30</div>
                                                            <div class="desc">Terminal 2</div>
                                                        </div>
                                                    </div>
                                                    <div class="bp-tl-warning">
                                                        <div class="red-dot-small"></div> Gate is subject to change. Boarding closes 25 min before departure.
                                                    </div>
                                                </div>

                                                <!-- LEG 2 TIMELINE -->
                                                <div class="bp-timeline-leg">
                                                    <div class="bp-timeline-header">
                                                        <div class="bp-tl-flight">
                                                            <div class="lbl">Flight</div>
                                                            <div class="val">6E 7892</div>
                                                            <div class="lbl">26 MAR 2026</div>
                                                        </div>
                                                        <div class="bp-tl-route">
                                                            <div class="city">BOM</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">GOI</div>
                                                        </div>
                                                    </div>
                                                    <div class="bp-timeline-line">
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Bag drop-off limit</div>
                                                            <div class="time">04:45</div>
                                                            <div class="desc">Baggage: 15kg + 7kg cabin</div>
                                                        </div>
                                                        <div class="bp-tl-node active">
                                                            <div class="dot solid"></div>
                                                            <div class="title white">Boarding</div>
                                                            <div class="time white">05:45</div>
                                                            <div class="desc white">Gate 2A / Zone 01</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow red-dot"></div>
                                                            <div class="title blue">Gate closed</div>
                                                            <div class="time">06:10</div>
                                                            <div class="desc">Zone 01</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Seat</div>
                                                            <div class="time bold">8F</div>
                                                            <div class="desc">Economy (SSR: VGML)</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Arrival</div>
                                                            <div class="time">07:20</div>
                                                            <div class="desc">Terminal 1</div>
                                                        </div>
                                                    </div>
                                                    <div class="bp-tl-warning">
                                                        <div class="red-dot-small"></div> Gate is subject to change. Boarding closes 25 min before departure.
                                                    </div>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Passenger 2 -->
                                <div class="bp-slide">
                                    <div class="digital-bp">
                                        <div class="bp-top-section">
                                            <div class="bp-header">
                                                <div class="bp-title-small">Boarding pass</div>
                                                <div class="bp-pnr-tag">PNR X3K9P2</div>
                                            </div>
                                            <div class="bp-qr-flipper-wrapper" onclick="openQRModal()">
                                                <div class="bp-qr-flipper">
                                                    <div class="bp-qr-front">
                                                        <img src="qr_code.png" class="bp-barcode-img" />
                                                        <div class="bp-qr-subtitle">SEC. 6E2341:002</div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="bp-passenger-name">SHARMA / ISHIKA</div>
                                        </div>
                                        <div class="bp-timeline-wrapper">
                                            <div class="bp-timeline-slider">
                                                <div class="bp-timeline-leg">
                                                    <div class="bp-timeline-header">
                                                        <div class="bp-tl-flight">
                                                            <div class="lbl">Flight</div>
                                                            <div class="val">6E 2341</div>
                                                            <div class="lbl">25 MAR 2026</div>
                                                        </div>
                                                        <div class="bp-tl-route">
                                                            <div class="city">DEL</div>
                                                            <div class="icon">✈</div>
                                                            <div class="city">BOM</div>
                                                        </div>
                                                    </div>
                                                    <div class="bp-timeline-line">
                                                        <div class="bp-tl-node active">
                                                            <div class="dot solid"></div>
                                                            <div class="title white">Boarding</div>
                                                            <div class="time white">22:00</div>
                                                            <div class="desc white">Gate 5B / Zone 02</div>
                                                        </div>
                                                        <div class="bp-tl-node">
                                                            <div class="dot hollow"></div>
                                                            <div class="title blue">Seat</div>
                                                            <div class="time bold">12D</div>
                                                            <div class="desc">Economy</div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        """

content = pattern.sub(new_html, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML Replaced.")
