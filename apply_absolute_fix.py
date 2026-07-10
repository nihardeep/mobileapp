import sys

with open('style.css', 'r') as f:
    css = f.read()

old_sb = """.status-bar {
    height: 48px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0 26px 8px 26px;
    font-size: 11px;
    font-weight: 700;
    color: var(--indigo-navy);
    z-index: 100;
    background: transparent;
}"""

new_sb = """.status-bar {
    height: 48px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0 26px 8px 26px;
    font-size: 11px;
    font-weight: 700;
    color: var(--indigo-navy);
    z-index: 100;
    background: transparent;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
}"""

if old_sb in css:
    css = css.replace(old_sb, new_sb)
    print("Fixed status-bar")
else:
    print("Could not find status-bar exact match!")

old_hh = """.home-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    margin-top: 4px;
}"""

new_hh = """.home-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    margin-top: 4px;
    padding-top: 52px;
}"""

if old_hh in css:
    css = css.replace(old_hh, new_hh)
    print("Fixed home-header")
else:
    print("Could not find home-header exact match!")


with open('style.css', 'w') as f:
    f.write(css)

