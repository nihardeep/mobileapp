with open('style.css', 'a', encoding='utf-8') as f:
    f.write("""
/* ==========================================================================
   NEW TICKET BOARDING PASS DESIGN
   ========================================================================== */
.bp-ticket-wrapper {
    padding: 0 24px 40px;
    position: relative;
    z-index: 10;
}
.bp-ticket-route-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    margin-bottom: 24px;
    padding: 0 12px;
}
.bp-ticket-city-col {
    display: flex;
    flex-direction: column;
}
.bp-ticket-city-col.right { text-align: right; }
.bp-ticket-route-header .city-name { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
.bp-ticket-route-header .city-code { font-size: 40px; font-weight: 800; letter-spacing: 1px; margin-bottom: 2px; }
.bp-ticket-route-header .city-full { font-size: 11px; font-weight: 400; opacity: 0.8; }
.bp-ticket-route-header .plane-icon { font-size: 32px; transform: rotate(90deg); margin: 0 20px; opacity: 0.9; }

.bp-ticket-card {
    background: #e5e7eb; /* off white/grey */
    border-radius: 12px;
    color: #1e3a8a;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.bp-ticket-top {
    padding: 24px;
}
.bp-ticket-grid-top {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 24px;
}
.bp-ticket-grid-top:last-child { margin-bottom: 0; }

.bp-ticket-label { font-size: 12px; font-weight: 700; color: #64748b; margin-bottom: 4px; }
.bp-ticket-value { font-size: 15px; font-weight: 500; color: #1e40af; }
.bp-ticket-value.large { font-size: 16px; font-weight: 600; color: #1e40af;}
.bp-ticket-value .time { font-size: 22px; font-weight: 800; color: #1e40af; display: inline-block; }
.bp-ticket-value .sub { font-size: 10px; font-weight: 600; color: #1e40af; opacity: 0.8; }
.bp-ticket-value .date-sub { font-size: 11px; font-weight: 500; color: #1e40af; display: block; margin-top: 4px; opacity: 0.9; }

.bp-ticket-logo img { height: 20px; object-fit: contain; }

.bp-ticket-divider {
    height: 2px;
    background: repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(30, 58, 138, 0.2) 8px, rgba(30, 58, 138, 0.2) 16px);
    margin: 0;
    position: relative;
}
/* The semi circle cutouts on the sides */
.bp-ticket-divider::before, .bp-ticket-divider::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 30px;
    height: 30px;
    background: #041029; /* Approx background color */
    border-radius: 50%;
    transform: translateY(-50%);
}
.bp-ticket-divider::before { left: -15px; }
.bp-ticket-divider::after { right: -15px; }

.bp-ticket-bottom {
    padding: 24px;
    display: flex;
    gap: 16px;
    justify-content: space-between;
}
.bp-ticket-grid-bottom {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    flex-grow: 1;
}
.bp-ticket-qr-block {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
.bp-ticket-qr-block img {
    width: 100px;
    height: 100px;
    mix-blend-mode: multiply; /* Make white bg transparent against the grey */
}
.bp-ticket-footer {
    text-align: center;
    font-size: 10px;
    color: #64748b;
    padding-bottom: 20px;
    font-weight: 500;
}
""")
print("CSS Appended")
