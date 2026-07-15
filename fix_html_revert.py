import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the fake trip companion card
fake_card_start = '                        <!-- UPCOMING TRIP CARD (Default View) -->'
fake_card_end = '                        <!-- BOARDING PASS UI (Hidden by default) -->\n                        <div id="tripsBoardingPassUI" style="display: none; position: relative;">'

content = content.replace("""                        <!-- UPCOMING TRIP CARD (Default View) -->
                        <div id="tripsCompanionCard" style="padding: 20px;">
                            <div style="background: #fff; border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: center;">
                                <div style="width: 60px; height: 60px; background: rgba(0,95,169,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; font-size: 24px;">🌴</div>
                                <h3 style="margin: 0 0 8px; font-size: 20px; font-weight: 800; color: #0f172a;">Goa Getaway</h3>
                                <p style="margin: 0 0 24px; font-size: 13px; color: #64748b;">Flight XA 201 • Departs in 24 hours</p>
                                
                                <button id="btnCheckIn" onclick="handleCheckIn()" style="width: 100%; padding: 16px; background: var(--xairline-blue); color: #fff; border: none; border-radius: 12px; font-size: 16px; font-weight: 800; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0,95,169,0.2);">Web Check-in Now</button>
                                
                                <button id="btnViewBP" onclick="showBoardingPasses()" style="display: none; width: 100%; padding: 16px; background: #10b981; color: #fff; border: none; border-radius: 12px; font-size: 16px; font-weight: 800; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(16,185,129,0.2);">View Digital Boarding Pass</button>
                            </div>
                        </div>

                        <!-- BOARDING PASS UI (Hidden by default) -->
                        <div id="tripsBoardingPassUI" style="display: none; position: relative;">
                            <!-- Back Button -->
                            <div onclick="hideBoardingPasses()" style="padding: 16px 20px 0; color: var(--xairline-blue); font-weight: 700; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg> Back to Trip
                            </div>""", "")

# Remove the closing div we added for tripsBoardingPassUI
content = content.replace("""                        <!-- Carousel Dots -->
                        <div class="bp-dots" id="bpDots">
                            <div class="bp-dot active" onclick="scrollToSlide(0)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(1)"></div>
                        </div>
                        </div> <!-- End of tripsBoardingPassUI -->

                    </div>""", """                        <!-- Carousel Dots -->
                        <div class="bp-dots" id="bpDots">
                            <div class="bp-dot active" onclick="scrollToSlide(0)"></div>
                            <div class="bp-dot" onclick="scrollToSlide(1)"></div>
                        </div>

                    </div>""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Reverted HTML.")
