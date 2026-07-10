with open('style.css', 'r') as f:
    css = f.read()

insta_css = """
/* ==========================================================================
   INSTA STORIES CAROUSEL
   ========================================================================== */
.insta-stories-scroll {
    display: flex;
    overflow-x: auto;
    gap: 12px;
    padding: 0 16px 16px 16px;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
}
.insta-stories-scroll::-webkit-scrollbar {
    display: none;
}

.insta-story-card {
    flex: 0 0 auto;
    width: 140px;
    height: 200px;
    border-radius: 16px;
    background-size: cover;
    background-position: center;
    position: relative;
    scroll-snap-align: start;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    overflow: hidden;
}

/* The gradient ring to indicate unseen story/video */
.insta-story-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    padding: 3px;
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}

.insta-play-ring {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 24px;
    height: 24px;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(4px);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255,255,255,0.3);
}

.insta-story-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 30px 12px 12px 12px;
    background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%);
    color: white;
}

.insta-story-city {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 2px;
}

.insta-story-price {
    font-size: 12px;
    font-weight: 500;
    opacity: 0.9;
}

.explore-all-text {
    text-align: center;
    font-size: 14px;
    font-weight: 400; /* not bold */
    color: var(--indigo-blue);
    margin-top: 4px;
    margin-bottom: 24px;
    cursor: pointer;
}

/* ==========================================================================
   AI DESTINATION HERO VIDEO
   ========================================================================== */
#aiDestHeroVideo {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
}

/* Update ai-dest-hero-img container if needed to support video */
.ai-dest-hero-img {
    position: relative;
    overflow: hidden;
}
"""

if "INSTA STORIES CAROUSEL" not in css:
    with open('style.css', 'a') as f:
        f.write("\n" + insta_css)
    print("Added Insta CSS")
else:
    print("Already added")
