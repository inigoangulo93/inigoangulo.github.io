/* Portfolio analytics: conversion events, SPA page views and chapter depth on top of GA4.
   Nothing personal is sent: no emails, no form contents, only which control was used and where. */
(function(){
  function ev(name,params){
    if(typeof window.gtag!=='function')return;
    var p=params||{};
    p.page_path=location.pathname+location.hash;
    window.gtag('event',name,p);
  }
  function where(el){
    var s=el.closest('section[id], [id^="v-"], .layer[id], footer, nav, header, .hero-wrap');
    if(!s)return 'page';
    if(s.tagName==='FOOTER')return 'footer';
    if(s.tagName==='NAV'||s.tagName==='HEADER')return 'nav';
    if(s.classList.contains('hero-wrap'))return 'hero';
    return s.id||'page';
  }
  function caseName(){
    var m=location.pathname.match(/\/work\/([a-z0-9-]+)\.html/);
    return m?m[1]:'home';
  }

  /* 1. Conversions and outbound clicks, by delegation so new links are covered automatically */
  document.addEventListener('click',function(e){
    var a=e.target.closest('a,button');if(!a)return;
    var href=a.getAttribute('href')||'';
    var base={location:where(a),case_name:caseName(),label:(a.textContent||'').trim().slice(0,40)};
    if(href.indexOf('mailto:')===0){ev('contact_email',base);return}
    if(href.indexOf('tel:')===0){ev('contact_phone',base);return}
    if(a.hasAttribute('data-cal-link')||href.indexOf('cal.com')>-1){ev('book_call',base);return}
    if(href.indexOf('linkedin.com')>-1){ev('contact_linkedin',base);return}
    if(a.hasAttribute('download')||/\.pdf(\?|$)/i.test(href)){
      ev(/cv/i.test(href)?'cv_download':'file_download_click',Object.assign({file_name:href.split('/').pop()},base));return}
    if(a.classList.contains('hero__cta')||a.classList.contains('hero__cta2')){ev('cta_click',base);return}
    if(a.classList.contains('svc__main')){ev('service_open',Object.assign({},base,{service:(href.match(/^\/?([a-z-]+)/)||[])[1]||href}));return}
    if(a.classList.contains('svc__pf')){ev('case_open',Object.assign({},base,{location:'services',case_name:href.replace(/^.*\/|\.html$/g,'')}));return}
    if(/^\/?writing\/kit\//.test(href)&&caseName()!=='kit'){ev('kit_open',Object.assign({},base,{target:href}));return}
    if(/^\/?lab\//.test(href)&&location.pathname.indexOf('/lab/')!==0){ev('lab_open',Object.assign({},base,{target:href}));return}
    if(a.classList.contains('cd')||a.closest('.cd')){var c=a.closest('.cd')||a;ev('case_open',Object.assign({},base,{case_name:(c.getAttribute('href')||'').replace(/^.*\/|\.html$/g,'')}));return}
    if(/^https?:\/\//.test(href)&&href.indexOf(location.host)===-1){ev('outbound',Object.assign({link_url:href},base))}
  },true);

  /* 2. Contact form */
  var f=document.getElementById('contactForm');
  if(f)f.addEventListener('submit',function(){ev('contact_form_submit',{location:'contact',case_name:'home'})});

  /* 3. SPA views on the home page: Work, How I think, About become page views */
  if(typeof window.render==='function'){
    var _r=window.render,last=null;
    window.render=function(n){
      _r.apply(this,arguments);
      var path={index:'/',logs:'/how-i-think',about:'/how-i-think'}[n]||('/'+n);
      if(path!==last){last=path;if(typeof window.gtag==='function')window.gtag('event','page_view',{page_path:path,page_title:document.title,page_location:location.origin+path})}
    };
  }

  /* 4. Chapter depth on case studies: one event per chapter the first time it is 40% visible */
  if('IntersectionObserver' in window){
    var secs=document.querySelectorAll('.cs__section[id], section.v[id]');
    var seen={};
    var io=new IntersectionObserver(function(es){es.forEach(function(x){
      if(!x.isIntersecting)return;var id=x.target.id;if(seen[id])return;seen[id]=1;
      var h=x.target.querySelector('h2,h3');
      ev('chapter_view',{case_name:caseName(),chapter:id,chapter_title:h?(h.textContent||'').trim().slice(0,40):''});
    })},{threshold:.15});
    secs.forEach(function(s){io.observe(s)});
  }

  /* 5. Interactions worth knowing about */
  document.addEventListener('click',function(e){
    var t=e.target.closest('.jd__c,.door,.cs__more summary,.flow__step,.hx__tab,.cs__try-btn');
    if(!t)return;
    ev('ui_interaction',{control:t.className.split(' ')[0],label:(t.textContent||'').trim().slice(0,40),case_name:caseName()});
  },true);
})();
