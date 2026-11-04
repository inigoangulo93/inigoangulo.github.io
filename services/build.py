#!/usr/bin/env python3
"""Builds the four service pages from one template. Run from the repo root: python3 services/build.py"""
import json, html, os, subprocess, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chrome import header, mobmenu, FOOTER
VER = subprocess.run(["git","rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip() or "0"

GA = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-WWCZNNK7YW"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-WWCZNNK7YW");</script>\n<script src="/analytics.js" defer></script>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'

DOORS = {'ai-product-builder': '<div class="door door--big play">\n<div class="door__art"><svg class="a1" viewBox="0 0 320 150" aria-hidden="true">\n  <!-- lines lead->agents -->\n  <path class="ln" d="M70 75 C100 75 100 40 130 40"/><path class="ln" d="M70 75 H130"/><path class="ln" d="M70 75 C100 75 100 110 130 110"/>\n  <path class="flow f1" d="M70 75 C100 75 100 40 130 40"/><path class="flow f2" d="M70 75 H130"/><path class="flow f3" d="M70 75 C100 75 100 110 130 110"/>\n  <!-- lines agents->prod -->\n  <path class="ln" d="M190 40 C215 40 215 75 236 75"/><path class="ln" d="M190 75 H236"/><path class="ln" d="M190 110 C215 110 215 75 236 75"/>\n  <path class="flow g1" d="M190 40 C215 40 215 75 236 75"/><path class="flow g2" d="M190 75 H236"/><path class="flow g3" d="M190 110 C215 110 215 75 236 75"/>\n  <!-- lead -->\n  <circle class="node lead" cx="52" cy="75" r="18"/><text class="tx" x="52" y="78" text-anchor="middle" fill="var(--t1)">ME</text>\n  <!-- agents -->\n  <rect class="node agent n1" x="130" y="28" width="60" height="24" rx="5"/><text class="tx" x="160" y="43" text-anchor="middle">SCHEMA</text>\n  <rect class="node agent n2" x="130" y="63" width="60" height="24" rx="5"/><text class="tx" x="160" y="78" text-anchor="middle">UI</text>\n  <rect class="node agent n3" x="130" y="98" width="60" height="24" rx="5"/><text class="tx" x="160" y="113" text-anchor="middle">SECURITY</text>\n  <!-- production -->\n  <rect class="prod" x="236" y="55" width="64" height="40" rx="6"/>\n  <text class="tx" x="246" y="69">&gt;_</text><rect class="cur" x="258" y="62" width="4" height="8"/>\n  <text class="tx" x="246" y="86">PROD</text>\n  <path class="tick" d="M276 84 l4 4 l8 -9"/>\n</svg></div>\n<div class="door__body">\n<span class="door__k">01&nbsp;&nbsp;AI build &amp; deployment</span>\n<h3 class="door__h">Working software, not a roadmap slot.</h3>\n<p class="door__p">I scope what&#8217;s worth building, orchestrate a team of AI agents to build it, and own the rollout to production, inside your business.</p>\n</div></div>\n', 'product-consultant-zurich': '<div class="door door--big play">\n<div class="door__art"><svg class="a2" viewBox="0 0 320 150" aria-hidden="true">\n  <defs><pattern id="a2g" width="12" height="12" patternUnits="userSpaceOnUse"><path class="grid" d="M12 0 H0 V12" fill="none"/></pattern></defs>\n  <rect x="46" y="18" width="228" height="114" rx="8" fill="url(#a2g)"/>\n  <rect class="frame" x="46" y="18" width="228" height="114" rx="8"/>\n  <rect class="ph" x="100" y="58" width="120" height="34" rx="5"/>\n  <!-- layer 1: nav -->\n  <rect class="part nav" x="46" y="18" width="228" height="16" rx="8"/>\n  <!-- layer 2: sidebar -->\n  <rect class="part side" x="46" y="34" width="44" height="98"/>\n  <!-- layer 3: cards -->\n  <rect class="part card c1" x="100" y="44" width="50" height="34" rx="4"/>\n  <rect class="part card c2" x="158" y="44" width="50" height="34" rx="4"/>\n  <rect class="part card c3" x="216" y="44" width="48" height="34" rx="4"/>\n  <!-- layer 4: content lines -->\n  <rect class="part line l1" x="100" y="90" width="150" height="5" rx="2.5"/>\n  <rect class="part line l2" x="100" y="100" width="118" height="5" rx="2.5"/>\n  <rect class="part line l3" x="100" y="110" width="80" height="5" rx="2.5"/>\n  <!-- layer 5: cta -->\n  <rect class="part cta" x="206" y="104" width="58" height="18" rx="4"/>\n  <text class="part ctat" x="235" y="116" text-anchor="middle">SHIP</text>\n</svg></div>\n<div class="door__body">\n<span class="door__k">02&nbsp;&nbsp;Product &amp; UX</span>\n<h3 class="door__h">Senior product and design lead, in one person.</h3>\n<p class="door__p">Ten years turning ambiguous, data-heavy problems into products people trust: checkout, onboarding, design systems, dashboards.</p>\n</div></div>\n', 'ux-design-consultant': '<div class="door door--big play">\n<div class="door__art"><svg class="a2" viewBox="0 0 320 150" aria-hidden="true">\n  <defs><pattern id="a2g" width="12" height="12" patternUnits="userSpaceOnUse"><path class="grid" d="M12 0 H0 V12" fill="none"/></pattern></defs>\n  <rect x="46" y="18" width="228" height="114" rx="8" fill="url(#a2g)"/>\n  <rect class="frame" x="46" y="18" width="228" height="114" rx="8"/>\n  <rect class="ph" x="100" y="58" width="120" height="34" rx="5"/>\n  <!-- layer 1: nav -->\n  <rect class="part nav" x="46" y="18" width="228" height="16" rx="8"/>\n  <!-- layer 2: sidebar -->\n  <rect class="part side" x="46" y="34" width="44" height="98"/>\n  <!-- layer 3: cards -->\n  <rect class="part card c1" x="100" y="44" width="50" height="34" rx="4"/>\n  <rect class="part card c2" x="158" y="44" width="50" height="34" rx="4"/>\n  <rect class="part card c3" x="216" y="44" width="48" height="34" rx="4"/>\n  <!-- layer 4: content lines -->\n  <rect class="part line l1" x="100" y="90" width="150" height="5" rx="2.5"/>\n  <rect class="part line l2" x="100" y="100" width="118" height="5" rx="2.5"/>\n  <rect class="part line l3" x="100" y="110" width="80" height="5" rx="2.5"/>\n  <!-- layer 5: cta -->\n  <rect class="part cta" x="206" y="104" width="58" height="18" rx="4"/>\n  <text class="part ctat" x="235" y="116" text-anchor="middle">SHIP</text>\n</svg></div>\n<div class="door__body">\n<span class="door__k">02&nbsp;&nbsp;Product &amp; UX</span>\n<h3 class="door__h">Senior product and design lead, in one person.</h3>\n<p class="door__p">Ten years turning ambiguous, data-heavy problems into products people trust: checkout, onboarding, design systems, dashboards.</p>\n</div></div>\n', 'cro-ecommerce-consultant': '<div class="door door--big play">\n<div class="door__art"><svg class="a3" viewBox="0 0 320 150" aria-hidden="true">\n  <!-- funnel stages -->\n  <path class="stage" d="M80 22 H240 L222 52 H98 Z"/>\n  <path class="stage" d="M100 58 H220 L204 88 H116 Z"/>\n  <path class="stage" d="M120 94 H200 L188 118 H132 Z"/>\n  <!-- flow, fills stage by stage from the top on hover -->\n  <path class="fl f1" d="M80 22 H240 L222 52 H98 Z"/>\n  <path class="fl f2" d="M100 58 H220 L204 88 H116 Z"/>\n  <path class="fl f3" d="M120 94 H200 L188 118 H132 Z"/>\n  <!-- leak between stage 1 and 2 -->\n  <g transform="translate(222 52)"><path class="drop d1" d="M0 0 l3 5 a3 3 0 1 1 -6 0 z"/><path class="drop d2" d="M8 -2 l3 5 a3 3 0 1 1 -6 0 z"/><path class="drop d3" d="M-6 2 l3 5 a3 3 0 1 1 -6 0 z"/></g>\n  <!-- patch: a clamp over the leak, pulses once -->\n  <g class="patch"><circle class="pulse" cx="222" cy="52" r="6"/><path class="clamp" d="M212 56 L222 50 L232 56"/></g>\n  <!-- outlet stream and output bar -->\n  <path class="stream" d="M160 118 V126"/>\n  <rect class="out" x="120" y="126" width="80" height="6" rx="3"/>\n  <text class="lift" x="206" y="133">+11%</text>\n</svg></div>\n<div class="door__body">\n<span class="door__k">03&nbsp;&nbsp;CRO &amp; commerce</span>\n<h3 class="door__h">Find where the funnel leaks. Prove the fix.</h3>\n<p class="door__p">Checkout, onboarding and catalogue audits for ecommerce. Agents trace the funnel, I decide what to test first, every fix ships A/B ready.</p>\n</div></div>\n'}

PAGES = {
"product-consultant-zurich": dict(
  title='Product Consultant in Zurich: strategy, discovery and product leadership / Inigo Angulo',
  h1='Senior product leadership, from strategy to execution.',
  desc='Product consultant and product lead based in Zurich. Discovery, strategy, roadmapping and ownership of outcomes, in your team or on a project. Ten years at GetYourGuide, ING, WPP and Crowdhouse.',
  kicker='Lead: product strategy and leadership',
  lead='Ten years turning ambiguous, data heavy problems into products people trust: discovery and opportunity identification, strategy, roadmapping and prioritisation, ownership of the outcome, and the design and delivery that follow. At GetYourGuide, ING, WPP and Crowdhouse, in product teams of three to thirty. As a product lead or lead product designer in your organisation, or on an independent engagement when that is what the problem needs.',
  proof=[("10 yrs","product, design and growth across commerce and complex systems"),("+11%","checkout conversion at GetYourGuide, ten experiments, four markets"),("5","countries shipping from one design system at ING"),("17 days","idea to production on my own product, Acervo")],
  problems_h='When this makes sense',
  problems=[('Founder led product has stopped scaling', 'You are the product manager, the CEO and the sales lead. Decisions wait for you, and the team builds what is easiest to specify instead of what moves the metric. Someone has to own the product function.'), ('A roadmap full of features, no outcomes', 'Everything on the list is reasonable, nothing is prioritised by evidence. I bring the discipline of measuring before deciding and killing what does not pay, and I stay until the number moves.'), ('A product team without a senior lead', 'After a reorganisation, ahead of a launch that cannot slip, or because the team has outgrown its founders. I take ownership of the product, its roadmap and its design direction, whether that is a permanent seat or a defined engagement.')],
  how_h='How I lead product work',
  how=[("Listen","Two weeks inside your data and your customers: analytics, sales calls, support tickets, the field. I come back with the three problems that matter and the evidence for each."),("Frame","A roadmap with outcomes, not features. Each item has a number it should move and the cheapest experiment that proves it."),("Architect","I design the system and its boundaries with your engineers: what we build, what we buy, what we do not touch."),("Prove","Experiments with pre registered success criteria. A/B tests, prototypes with real users, or a thin slice in production."),("Close the loop","I stay until it ships and the number moves. Decisions are written down with the reasoning, so the team can carry on without me.")],
  case=("GetYourGuide, checkout","+11% checkout conversion from the step nobody was measuring","The team was optimising the wrong step. 38% of converters left checkout and came back with no re-entry experience. Ten experiments later: +11% conversion across four EU markets.","../work/checkout.html","../img/gyg-card.webp"),
  fit_yes=['Series A to C companies with a product team of 3 to 30', 'Founder led products that need a product function', 'E-commerce, marketplaces, fintech and B2B SaaS', 'Product organisations in Zurich, Switzerland or remote across Europe'],
  fit_no=["You want a deck and no involvement in delivery","The decision has already been made and you need a signature","You need someone on site five days a week in Zurich (I work hybrid)"],
  faq=[('Permanent role, contract or independent engagement?', 'All three, and the work is the same: I take responsibility for product outcomes. As a product lead or lead product designer in your organisation, as a contractor for a defined period, or independently on a scoped engagement through my own firm. The format follows the problem, not the other way round.'), ('How does an engagement start?', 'Two weeks inside your data and your customers, and a roadmap of outcomes with the first experiments shipped. For independent work, scoped by days per week with a fixed number after a first conversation.'), ('Do you work on site in Zurich?', 'Hybrid. I am based near Zurich and come on site for workshops, kickoffs and the moments where being in the room matters. The rest is remote.'), ('Do you only do strategy, or do you execute?', 'Both. I run discovery and roadmap, and I stay through design and delivery. I design the flows and the interface myself, and on my own product I shipped the software with AI agent teams; with your team I lead the people who do.'), ('What is the difference between a product consultant and a product lead?', 'A consultant diagnoses and recommends. A product lead owns outcomes inside the team. I do the second, which includes the first, whichever contract it sits on.'), ('Which languages do you work in?', 'English and Spanish, both at working level for product and stakeholder work.')],
  also=[('ai-product-builder', 'Build', 'AI native development'), ('cro-ecommerce-consultant', 'Optimize', 'Conversion and growth'), ('ux-design-consultant', 'UX', 'Hands-on product design')],
  service_type='Product strategy and product leadership consulting',
  covers=['Product discovery', 'Opportunity identification', 'Product strategy', 'Roadmapping and prioritisation', 'Product leadership', 'Cross functional alignment', 'Product execution', 'UX and design direction'],
  cta=('Explore a product challenge', 'Tell me where the product is stuck. Thirty minutes, no deck; I will tell you how I would approach it and whether I am the right person.'),
  first_step=('A first step that fits most situations', 'Product opportunity assessment. Two weeks to understand the business opportunity, identify what should be built, define an initial scope, name the risks and dependencies, and recommend an execution approach. It stands on its own and it is how most engagements start, whether what follows is a build, a product lead in the team or nothing at all.'),
),
"ux-design-consultant": dict(
  title='Senior UX and Product Designer, Zurich: research, flows, design systems / Inigo Angulo',
  h1='Product design that ships, from the first flow to the design system.',
  desc='Senior product and UX designer in Zurich. Research, information architecture, interaction design for complex workflows, design systems and the hand off to engineering. GetYourGuide, ING, WPP, Enso, Acervo.',
  kicker='Senior product design',
  lead='Ten years as a hands-on product designer: research and synthesis, product thinking, UX architecture, interaction design for complex workflows, design systems, Figma and prototyping, and the collaboration with engineering that gets the work built as designed. On my own product I shipped it too, which is why the hand off is a spec and not a picture. Senior or lead product designer in a product organisation, or on a defined project.',
  proof=[("+34%","booking conversion at Enso across four European markets"),("4x","adoption of the Enso tenant platform after the redesign"),("5","countries on one design system at ING, tokens first"),("26","components in the Acervo library, built and shipped")],
  problems_h='The design problems I get called for',
  problems=[("A flow that leaks users","Checkout, onboarding, sign up, KYC. I map where people drop, why, and redesign the step with a measurable target, not a prettier screen."),("A product that grew without a system","Twelve shades of the same button, three date pickers. I build the design system from the tokens up, and I make sure engineering adopts it, which is the hard part."),("Complex data, no clear interface","Dashboards, admin panels, operational tools. Products where the user is on a deadline and ambiguity costs money.")],
  how_h="How I work with design and engineering",
  how=[("Research with a question","Not a persona exercise. Interviews, session recordings and analytics aimed at one decision we need to make."),("Flows before screens","The state machine of the product first: every path, every error, every empty state. Screens come after, and they are faster."),("Figma that mirrors code","Components, variables and tokens named like the codebase. Engineers get a spec, not a picture."),("Measured hand off","Each change ships with the metric it should move and how we will read it."),("The library stays alive","I leave a documented system and a routine for keeping it in sync with production.")],
  case=("Enso Co-living","4x adoption and +34% booking conversion on one platform","Two product challenges, one platform: a tenant app nobody used and a booking flow that lost people at the end. Rebuilt both across Lisbon, Valencia, Madrid and Barcelona.","../work/enso.html","../img/enso-card.webp"),
  fit_yes=["Product teams of 2 to 20 with engineers but no senior designer","E-commerce, marketplaces, fintech, operational B2B tools","Redesigns with a metric attached","Design system builds with engineering buy in"],
  fit_no=["Brand identity or marketing campaigns","Pixel polishing without access to data or users","Agency style deliverables with no contact with the team"],
  faq=[('Permanent role, contract or project?', 'All three. Senior or lead product designer in your organisation, a contract for a redesign, or a scoped project such as a design system. The craft is the same; the contract follows the need.'), ('Do you do research as well as UI?', 'Yes. Most of what makes a redesign work is upstream of the interface. I run interviews and read analytics before I open Figma.'), ('Can you work with our existing design system?', 'Yes, and I prefer it. I audit what exists, fix what blocks the team, and extend rather than replace.'), ('How do you work with engineering?', 'Components, variables and tokens named like the codebase, a spec rather than a picture, and a routine for keeping the library in sync with production. I ship production software on my own product with AI agent teams, so I know what a Figma file costs to build.'), ('Where are you based?', 'Near Zurich, Switzerland. Hybrid for Swiss teams, remote across Europe.')],
  also=[('ai-product-builder', 'Build', 'AI native development'), ('product-consultant-zurich', 'Lead', 'Product strategy and design'), ('cro-ecommerce-consultant', 'Optimize', 'Conversion and growth')],
  service_type='Product and UX design',
  covers=['Research and synthesis', 'Product thinking', 'UX architecture', 'Interaction design', 'Complex workflows', 'Design systems', 'Figma and prototyping', 'Collaboration with engineering', 'Design implementation quality'],
  cta=('Discuss a design problem', 'A flow that leaks, a product without a system, an interface nobody can read. Thirty minutes to look at it together.'),
),
"cro-ecommerce-consultant": dict(
  title="Conversion Optimization Consultant for E-commerce / Inigo Angulo",
  h1="Find where the funnel leaks. Prove the fix.",
  desc="CRO consultant for e-commerce and marketplaces. Checkout, onboarding and catalogue audits, experiments with pre registered criteria. +11% checkout conversion at GetYourGuide.",
  kicker='Optimize: conversion and growth',
  lead='Measurable product and commercial performance for e-commerce and marketplace teams: a funnel audit that finds the real leak, conversion research, a prioritised experiment plan, and fixes that ship A/B ready. Ten years in commerce at GetYourGuide, WPP and Enso.',
  proof=[("+11%","checkout conversion at GetYourGuide, four EU markets"),("38%","of converters were leaving checkout and coming back: the leak nobody measured"),("10","experiments in the programme, each with a written hypothesis"),("+34%","booking conversion at Enso after the flow redesign")],
  problems_h="The leaks I find most often",
  problems=[("The step you are not measuring","Most funnels are instrumented at the stage level. The drop is between stages: the back button, the tab switch, the return visit with no memory of the cart."),("Trust gaps, not payment problems","Shipping, returns, price surprises and reassurance at the moment of commitment convert more than another payment method."),("Catalogue and search friction","Filters that hide inventory, product pages that answer the wrong questions, search that returns the catalogue instead of the answer.")],
  how_h="How a CRO engagement runs",
  how=[("Audit","Two weeks: analytics, session recordings, support tickets and a walk through your funnel on a real phone. Output: the ranked list of leaks with the evidence for each."),("Plan","Experiments ordered by expected impact and cost, with success criteria written before anything is built."),("Build","I design the fix and work with your engineers, or with AI agents if you have no bandwidth, so every test ships A/B ready."),("Read","Statistical reads with sample sizes agreed in advance. No peeking, no calling winners at 80% confidence."),("Compound","The wins go into a playbook your team keeps running after I leave.")],
  case=("GetYourGuide, checkout","Ten experiments, +11% conversion, four markets","The team was optimising the wrong step. The problem was not payment, it was the re-entry experience nobody had measured. The case walks through all ten experiments, including the ones that lost.","../work/checkout.html","../img/gyg-card.webp"),
  fit_yes=["E-commerce and marketplaces with enough traffic to test (roughly 10k conversions a year or more)","Teams with a developer available or willing to let AI agents build the variants","Retail media and catalogue heavy businesses","DTC brands at the point where paid traffic stops scaling"],
  fit_no=["Sites with too little traffic for experiments (I will tell you, and suggest what to do instead)","Pure SEO or paid media work: I touch the funnel, not the acquisition"],
  faq=[('How is this priced?', 'A fixed scope for the audit, then a monthly cadence for the experiment programme, usually three to six months. Numbers after a first conversation and a look at your traffic.'), ('Do you need access to our analytics?', 'Yes. GA4 or equivalent, session recordings if you have them, and read access to the experiment tool. Without data it is opinion, and you can get opinion for free.'), ('What if we do not have an A/B testing tool?', 'I set one up. For most stacks that is a day of work, and for low traffic sites I will tell you when sequential tests are a better idea than a tool.'), ('Can AI agents build the test variants?', 'Yes, that is how I work on my own product. For a CRO programme it means variants ship in days, not sprints, and your engineers review instead of build.'), ('Which markets do you know?', 'Mainly Europe: Switzerland, Germany, Spain, Portugal, UK, with multi market checkout experience from GetYourGuide and Enso.')],
  also=[('ai-product-builder', 'Build', 'AI native development'), ('product-consultant-zurich', 'Lead', 'Product strategy and design'), ('ux-design-consultant', 'UX', 'Hands-on product design')],
  service_type="Conversion rate optimization consulting",
  covers=['Funnel analysis', 'Checkout optimisation', 'Conversion research', 'Experimentation', 'E-commerce UX', 'Data informed prioritisation'],
  cta=('Explore a conversion opportunity', 'Send me the funnel and the number you want to move. Thirty minutes to tell you where I would look first.'),
),
"ai-product-builder": dict(
  title='AI Product Builder: from opportunity to production with AI agent teams / Inigo Angulo',
  desc='AI native product development: product definition and scope, agent orchestration, human review and quality gates, testing, security, deployment and handover. One person takes a product from opportunity to production. Acervo: first production deploy in 17 days.',
  kicker='Build: AI native development',
  lead='For companies and founders who need to turn an idea, an opportunity or an internal problem into working software. The same product judgment I have applied for ten years, carried further: I define and scope the product, orchestrate a team of AI coding agents to build it under human review and quality gates, and own testing, security, deployment and the handover. Not a prototype: a system in production that your team can continue. I did it on my own product first.',
  proof=[('17 days', 'first commit to first production deploy on Acervo: a thin first version, not the finished product'), ('445', 'pull requests merged in seven weeks, every one through five checks'), ('15', 'gated releases, each with a security report and one human approval'), ('0', 'production incidents caused by an agent change')],
  problems_h="What this is for",
  problems=[("An internal tool nobody has time to build","Operations, back office, a customer portal. The business case is obvious and it has been on the backlog for a year. Weeks, not quarters."),("A product bet you want to test with real software","Not a Figma prototype and not a no code mock. A thin product in production with real users, so the decision is made on evidence."),("A team that wants to adopt agents safely","You have engineers and you want the method: how to split work, what gates to put in, what to never let an agent touch. I bring the system I run and adapt it to yours.")],
  how_h="How a build runs",
  how=[('Define and scope', 'One week. What the product must do, what it must never do, the data model and the security boundaries. Written as tickets with acceptance criteria. If you are not sure what to build yet, the product opportunity assessment below is this step on its own.'), ('Build with gates', 'Agents work in isolated branches. Every change passes lint, types, tests, a secrets scan and a review before it reaches main. No agent has production credentials.'), ('Human approval', 'Releases are promoted by a person, after a security pass. The approval is one id and one letter, and it is logged.'), ('Ship and measure', 'Production from week two or three. Analytics and an audit log from day one, so we know what is used.'), ('Hand over or operate', 'Documentation, decision log and the agent playbook. Your team keeps the system, or I keep operating it for a period.')],
  case=("Acervo","A production platform for car collections, one person plus eight agents","I defined the product, designed it and shipped it with an AI engineering team under two human gates. The case shows the real numbers from the GitHub API: 445 merges, 1,456 CI runs, 15 releases, and the day the security gate said no.","../work/acervo.html","../img/acervo-card.webp"),
  fit_yes=["Companies with a clear problem and no engineering bandwidth","Founders who want a real product in production before raising or hiring","Engineering leads who want to introduce agents with guardrails","Internal tools, portals, dashboards, workflow products"],
  fit_no=["Hard real time systems, embedded, or anything where a mistake is physical","Regulated workloads that require certified processes I do not hold","Projects where nobody on your side can own the product after hand over"],
  faq=[('Is this no code?', 'No. It is real code in a real repository, with tests and a release process, written mostly by AI agents under my direction and review. You own it and any engineer can continue it.'), ('How do you keep agents from breaking production?', 'Isolation and gates. Agents never hold production credentials, every change passes automated checks and a review, and promotion to production is a human decision with a security report attached. The Acervo case documents the whole flow.'), ('What is included in a typical engagement?', 'Scope, design, build, testing, security review, deployment and a documented handover. The first version is a sprint of two to six weeks; after that, either your team continues or I keep shipping for a period. Agent costs are a few hundred francs a month and I pass them through at cost.'), ('What does 17 days to production prove, and what does it not?', 'That one person with a scoped product and the right gates can have a thin first version in production in under three weeks. It does not mean a finished product: the fifteen releases after it are where most of the product lives.'), ('Which stack?', 'TypeScript, Next.js, Postgres (Supabase), Vercel for most products, because agents are strongest there and the ecosystem is boring in the good way. I adapt to yours when there is a reason.'), ('Do you work on site?', 'Hybrid near Zurich, remote across Europe. A build needs one kickoff in the room and weekly demos; the rest does not.')],
  also=[('product-consultant-zurich', 'Lead', 'Product strategy and design'), ('cro-ecommerce-consultant', 'Optimize', 'Conversion and growth'), ('ux-design-consultant', 'UX', 'Hands-on product design')],
  service_type="AI software development with agent teams",
  h1='From opportunity to production, with AI agent teams and human gates.',
  covers=['Product definition and scope', 'AI native development workflows', 'Agent orchestration', 'Human review and quality gates', 'Testing, security and deployment', 'Production ownership and handover'],
  cta=('Discuss a product idea', 'Tell me the problem and who it is for. Thirty minutes, no deck; I will say whether it should be built, and how.'),
  first_step=('A first step that fits most situations', 'Product opportunity assessment. Two weeks to understand the business opportunity, identify what should be built, define an initial scope, name the risks and dependencies, and recommend an execution approach. It stands on its own, and a build that starts from it starts from a written scope instead of a conversation.'),
),
}

def esc(s): return html.escape(s, quote=True)

def page(slug, d):
    url = f"https://inigoangulo.com/{slug}/"
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]}
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":d["title"].split(" / ")[0],"serviceType":d["service_type"],"url":url,"provider":{"@id":"https://inigoangulo.com/#person","@type":"Person","name":"Inigo Angulo","url":"https://inigoangulo.com/"},"areaServed":[{"@type":"City","name":"Zurich"},{"@type":"Country","name":"Switzerland"},{"@type":"Place","name":"Europe (remote)"}],"description":d["desc"]}
    bc_ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inigo Angulo","item":"https://inigoangulo.com/"},{"@type":"ListItem","position":2,"name":d["kicker"],"item":url}]}
    proof = "".join(f"<div><b>{esc(b)}</b><span>{esc(s)}</span></div>" for b,s in d["proof"])
    problems = "".join(f'<article><span class="n">0{i+1}</span><h3>{esc(h)}</h3><p>{esc(p)}</p></article>' for i,(h,p) in enumerate(d["problems"]))
    how = "".join(f"<li><div><b>{esc(h)}</b><span>{esc(p)}</span></div></li>" for h,p in d["how"])
    tag,ch,cp,chref,cimg = d["case"]
    yes = "".join(f"<li>{esc(x)}</li>" for x in d["fit_yes"]); no = "".join(f"<li>{esc(x)}</li>" for x in d["fit_no"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in d["faq"])
    also = "".join(f'<a class="path" href="../{s}/"><b>{esc(n)}</b><span>{esc(t)}</span></a>' for s,n,t in d["also"])
    covers = "".join(f"<li>{esc(x)}</li>" for x in d.get("covers",[]))
    cta_label, cta_text = d["cta"]
    fs = d.get("first_step")
    first_step = f'<section><div class="mx"><div class="first"><span class="k">{esc(fs[0])}</span><p>{esc(fs[1])}</p><a class="more" href="https://cal.com/inigoangulo/30min" data-cal-link="inigoangulo/30min">Start with the assessment &#8594;</a></div></div></section>' if fs else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(d["title"])}</title>
<meta name="description" content="{esc(d["desc"])}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:title" content="{esc(d["title"].split(" / ")[0])}">
<meta property="og:description" content="{esc(d["desc"])}">
<meta property="og:image" content="https://inigoangulo.com/img/og.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/services/services.css?v={VER}">
<link rel="stylesheet" href="/services/doors.css?v={VER}">
{GA}
<script type="application/ld+json">{json.dumps(svc_ld,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bc_ld,ensure_ascii=False)}</script>
</head>
<body>
{header('services','Services')}{mobmenu('services')}
<script src="/services/bar.js?v={VER}" defer></script>

<main>
<div class="hero"><div class="mx hero__grid">
<div>
<span class="k">{esc(d["kicker"])}</span>
<h1>{esc(d["h1"])}</h1>
<p class="lead">{esc(d["lead"])}</p>
<ul class="covers">{covers}</ul>
<div class="ctas"><a class="btn" href="https://cal.com/inigoangulo/30min" data-cal-link="inigoangulo/30min">{esc(cta_label)} &#8594;</a><a class="btn btn--o" href="mailto:inigoangulo@gmail.com">Email me</a></div>
</div>
{DOORS[slug]}
</div>
<div class="mx"><div class="proof">{proof}</div></div></div>

<section><div class="mx"><h2>{esc(d["problems_h"])}</h2><div class="grid">{problems}</div></div></section>

<section><div class="mx"><h2>{esc(d["how_h"])}</h2><ol class="steps">{how}</ol></div></section>
{first_step}

<section><div class="mx"><h2>Proof, not promises</h2>
<div class="case"><div><span class="tag">{esc(tag)}</span><h3>{esc(ch)}</h3><p>{esc(cp)}</p><a class="more" href="{chref}">Read the case study &#8594;</a></div><a href="{chref}"><img src="{cimg}" alt="{esc(ch)}" loading="lazy" decoding="async"></a></div>
</div></section>

<section><div class="mx"><h2>Who this is for</h2>
<div class="fit"><div><h3>A good fit</h3><ul>{yes}</ul></div><div class="no"><h3>Probably not</h3><ul>{no}</ul></div></div>
</div></section>

<section class="faq"><div class="mx"><h2>Questions I get asked</h2>{faq}</div></section>

<section><div class="mx">
<div class="cta"><div><h2>{esc(cta_label)}.</h2><p>{esc(cta_text)}</p></div><div class="ctas"><a class="btn" href="https://cal.com/inigoangulo/30min" data-cal-link="inigoangulo/30min">{esc(cta_label)} &#8594;</a><a class="btn btn--o" href="mailto:inigoangulo@gmail.com">Email</a></div></div>
<h2 style="margin-top:40px;font-size:1.1rem">The same profile, other directions</h2><p class="paths__p">Build, lead and optimize are three dimensions of one product practice, with hands-on design in all of them. The <a href="/#work">case studies</a> show the same person doing each.</p><div class="paths">{also}</div>
</div></section>
</main>

{FOOTER}
<script>(function(C,A,L){{let p=function(a,ar){{a.q.push(ar)}};let d=C.document;C.Cal=C.Cal||function(){{let cal=C.Cal;let ar=arguments;if(!cal.loaded){{cal.ns={{}};cal.q=cal.q||[];d.head.appendChild(d.createElement("script")).src=A;cal.loaded=true}}if(ar[0]===L){{const api=function(){{p(api,arguments)}};const namespace=ar[1];api.q=api.q||[];if(typeof namespace==="string"){{cal.ns[namespace]=cal.ns[namespace]||api;p(cal.ns[namespace],ar);p(cal,["initNamespace",namespace])}}else p(cal,ar);return}}p(cal,ar)}}}})(window,"https://app.cal.com/embed/embed.js","init");Cal("init",{{origin:"https://app.cal.com"}});Cal("ui",{{"theme":"dark","cssVarsPerTheme":{{"dark":{{"cal-brand":"#2dd4bf"}}}},"hideEventTypeDetails":false,"layout":"month_view"}});</script>
</body>
</html>
'''

if __name__ == "__main__":
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        open(f"{slug}/index.html","w").write(page(slug,d))
        print("built", slug)
