import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Close trendingInstaContainer before carousel-dots
target1 = """                                </div>
                                <div class="carousel-dots" id="trendingInstaDots">"""
replacement1 = """                                </div>
                                </div> <!-- close trendingInstaContainer -->
                                <div class="carousel-dots" id="trendingInstaDots">"""
html = html.replace(target1, replacement1)

# 2. Remove one </div> before Explore Communities
target2 = """                            </div>
                            </div>
                            <!-- Explore Communities -->"""
replacement2 = """                            </div>
                            <!-- Explore Communities -->"""
html = html.replace(target2, replacement2)

with open('index.html', 'w') as f:
    f.write(html)
