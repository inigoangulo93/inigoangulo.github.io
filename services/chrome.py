# Header, mobile menu and footer shared by every generated page (services and writing).
# Mirrors the markup of index.html so the site reads as one piece. Links are absolute.

LI = "https://www.linkedin.com/in/i%C3%B1igo-angulo-1ab25a134/"

def header(active, mini_label):
    """active: 'work' | 'how-i-think' | 'about' | 'writing' | 'lab' | 'services'"""
    def btn(href, label, key):
        on = " on" if key == active else ""
        return f'<a class="bar__btn{on}" href="{href}">{label}</a>'
    nav = btn("/#work", "Work", "work") + btn("/#how-i-think", "How I think", "how-i-think") + btn("/#about", "About", "about") + btn("/lab/", "Lab", "lab") + btn("/writing/", "Writing", "writing")
    return (f'<header class="bar"><div class="bar__inner"><a class="bar__name" href="/">Inigo Angulo</a>'
            f'<nav class="bar__nav">{nav}</nav>'
            f'<a class="bar__cta" href="/#contact">Contact</a>'
            f'<div class="bar__ham" id="hamBtn" onclick="toggleMenu()"><span></span><span></span><span></span></div></div>'
            f'<div class="bar__mini" aria-hidden="true"><i></i><span>{mini_label}</span></div></header>')

def mobmenu(active):
    def link(href, label, num, key):
        on = " on" if key == active else ""
        return f'<a class="mob-menu__link{on}" href="{href}"><span>{label}</span><span class="mob-menu__link-num">{num}</span></a>'
    return ('<div class="mob-menu" id="mobMenu"><div class="mob-menu__bg" onclick="toggleMenu()"></div><div class="mob-menu__inner">'
            + link("/#work", "Work", "01", "work") + link("/#how-i-think", "How I think", "02", "how-i-think")
            + link("/#about", "About", "03", "about") + link("/lab/", "Lab", "04", "lab") + link("/writing/", "Writing", "05", "writing")
            + '<div class="mob-menu__cta"><a href="/#contact">Get in touch &#8594;</a></div>'
            + f'<div class="mob-menu__contact"><a href="mailto:inigoangulo@gmail.com">Email</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="tel:+41799528321">Phone</a></div>'
            + '</div></div>')

FOOTER = f'''<footer class="footer">
<div class="footer__inner">
<div><span class="footer__brand">Inigo Angulo</span><p class="footer__desc">Senior product designer and product builder. Strategy, design and AI native development, from scope to production. Based in Zurich, 9+ years building systems that move metrics.</p></div>
<div><p class="footer__col-title">Navigation</p><div class="footer__links"><a href="/#work">Work</a><a href="/#how-i-think">How I think</a><a href="/#about">About</a></div></div>
<div><p class="footer__col-title">Connect</p><div class="footer__links"><a href="mailto:inigoangulo@gmail.com">Email</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="tel:+41799528321">Phone</a><a href="https://github.com/inigoangulo93" target="_blank" rel="noopener">GitHub</a></div></div>
<div><p class="footer__col-title">Work with me</p><div class="footer__links"><a href="/ai-product-builder/">Build: AI native development</a><a href="/product-consultant-zurich/">Lead: product strategy and design</a><a href="/cro-ecommerce-consultant/">Optimize: conversion and growth</a><a href="/ux-design-consultant/">Senior product design</a></div></div>
<div><p class="footer__col-title">Resources</p><div class="footer__links"><a href="/lab/">Lab</a><a href="/writing/">Writing</a><a href="/inigo-angulo-cv-2026.pdf" download>Download CV</a></div></div>
</div>
<div class="footer__bottom"><span class="footer__copy">2026 Inigo Angulo</span><span class="footer__built">Built with code, not templates</span></div>
</footer>'''
