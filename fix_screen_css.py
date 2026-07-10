with open('style.css', 'a') as f:
    f.write("""
/* Fix for Passenger Screen Scrolling */
#screenPassenger {
    height: 100%;
    overflow-y: auto;
    position: relative;
    padding-bottom: 80px; /* space for the sticky footer */
}
""")
