javascript
const HTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeckBoss - Presentation Platform</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --accent: #f59e0b;
            --bg: #0f172a;
            --surface: #1e293b;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        
        /* Navigation */
        nav {
            padding: 1.5rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .nav-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--accent);
            text-decoration: none;
            transition: opacity 0.3s;
        }
        
        .logo:hover {
            opacity: 0.9;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-link:hover {
            color: var(--accent);
        }
        
        .cta-button {
            background: var(--accent);
            color: var(--bg);
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: 600;
            text-decoration: none;
            transition: transform 0.3s, opacity 0.3s;
            display: inline-block;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            opacity: 0.95;
        }
        
        /* Hero */
        .hero {
            padding: 5rem 0;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            line-height: 1.2;
        }
        
        .hero p {
            font-size: 1.25rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto 2.5rem;
        }
        
        /* Features */
        .features {
            padding: 5rem 0;
            background: rgba(0,0,0,0.2);
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }
        
        .feature-card {
            background: var(--surface);
            padding: 2rem;
            border-radius: 1rem;
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
        }
        
        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        /* Pricing */
        .pricing {
            padding: 5rem 0;
        }
        
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .pricing-card {
            background: var(--surface);
            padding: 2.5rem 2rem;
            border-radius: 1rem;
            text-align: center;
            position: relative;
            transition: transform 0.3s;
        }
        
        .pricing-card:hover {
            transform: translateY(-5px);
        }
        
        .pricing-card.popular {
            border: 2px solid var(--accent);
        }
        
        .popular-badge {
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--accent);
            color: var(--bg);
            padding: 0.5rem 1.5rem;
            border-radius: 2rem;
            font-weight: 600;
            font-size: 0.875rem;
        }
        
        .price {
            font-size: 3rem;
            font-weight: 700;
            margin: 1.5rem 0;
            color: var(--accent);
        }
        
        .price span {
            font-size: 1rem;
            color: var(--text-muted);
        }
        
        .pricing-features {
            list-style: none;
            margin: 2rem 0;
        }
        
        .pricing-features li {
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Footer */
        footer {
            padding: 3rem 0;
            border-top: 1px solid rgba(255,255,255,0.1);
            text-align: center;
            color: var(--text-muted);
        }
        
        /* Mobile */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .nav-links {
                display: none;
            }
            
            .mobile-menu {
                display: block;
                background: none;
                border: none;
                color: var(--text);
                font-size: 1.5rem;
                cursor: pointer;
            }
            
            .pricing-grid {
                grid-template-columns: 1fr;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-menu {
                display: none;
            }
        }
    </style>
</head>
<body>
    <nav>
        <div class="container nav-content">
            <a href="#" class="logo">DeckBoss</a>
            <div class="nav-links">
                <a href="#features" class="nav-link">Features</a>
                <a href="#pricing" class="nav-link">Pricing</a>
                <a href="#" class="nav-link">Documentation</a>
                <a href="#" class="cta-button">Get Started</a>
            </div>
            <button class="mobile-menu">☰</button>
        </div>
    </nav>

    <section class="hero">
        <div class="container">
            <h1>Create Presentations That Captivate</h1>
            <p>DeckBoss gives teams the tools to build, share, and present stunning decks that win clients and inspire action.</p>
            <a href="#pricing" class="cta-button">Start Free Trial</a>
        </div>
    </section>

    <section id="features" class="features">
        <div class="container">
            <h2 class="section-title">Powerful Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <h3>Smart Templates</h3>
                    <p>Professionally designed templates that adapt to your content automatically.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🤝</div>
                    <h3>Team Collaboration</h3>
                    <p>Real-time editing and comments for seamless team workflow.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Data Visualization</h3>
                    <p>Transform complex data into clear, engaging charts and graphs.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="pricing" class="pricing">
        <div class="container">
            <h2 class="section-title">Simple Pricing</h2>
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3>Free</h3>
                    <div class="price">$0<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>3 Presentations</li>
                        <li>Basic Templates</li>
                        <li>1 GB Storage</li>
                        <li>Community Support</li>
                    </ul>
                    <a href="#" class="cta-button">Get Started</a>
                </div>
                <div class="pricing-card popular">
                    <div class="popular-badge">Most Popular</div>
                    <h3>Pro</h3>
                    <div class="price">$9<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>50 Presentations</li>
                        <li>All Templates</li>
                        <li>10 GB Storage</li>
                        <li>Priority Support</li>
                    </ul>
                    <a href="#" class="cta-button">Try Free for 14 Days</a>
                </div>
                <div class="pricing-card">
                    <h3>Team</h3>
                    <div class="price">$29<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>Unlimited Presentations</li>
                        <li>Custom Templates</li>
                        <li>100 GB Storage</li>
                        <li>Dedicated Support</li>
                    </ul>
                    <a href="#" class="cta-button">Contact Sales</a>
                </div>
                <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <div class="price">$99<span>/month</span></div>
                    <ul class="pricing-features">
                        <li>Everything in Team</li>
                        <li>SAML SSO</li>
                        <li>Custom Branding</li>
                        <li>24/7 Phone Support</li>
                    </ul>
                    <a href="#" class="cta-button">Contact Sales</a>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>© 2024 DeckBoss. All rights reserved.</p>
            <p style="margin-top: 1rem; font-size: 0.875rem;">Presentation platform for modern teams</p>
        </div>
    </footer>

    <script>
        // Minimal mobile menu toggle
        document.querySelector('.mobile-menu').addEventListener('click', function() {
            const navLinks = document.querySelector('.nav-links');
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        });
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // Health endpoint
    if (url.pathname === '/health') {
      return new Response(
        JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }),
        {
          headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
          }
        }
      );
    }
    
    // Main landing page
    return new Response(HTML, {
      headers: {
        'Content-Type': 'text/html;charset=UTF-8',
        'Content-Security-Policy': "default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self'",
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff'
      }
    });
  }
};