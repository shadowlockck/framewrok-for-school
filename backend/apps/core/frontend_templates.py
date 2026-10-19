"""Three independent visual identities for the component-based public site."""

FRONTEND_TEMPLATES = {
    "classic": {
        "name": "Класичний",
        "label": "Офіційний вебсайт закладу освіти",
        "description": "Темно-синя шапка, світла горизонтальна навігація та стриманий вступний блок.",
        "css": r"""
/* Civic identity: a compact navy school masthead and a calm, open introduction. */
.school-site--classic {
  --ink: #17304a; --muted: #56677a; --canvas: #f4f5f3; --surface: #fff;
  --line: #d9dfdf; --accent: #173a59; --accent-ink: #fff; --soft: #edf2f5;
  --radius: 2px; --shadow: none;
  display: flex; flex-direction: column;
}
.school-site--classic .utility-bar { background: #e6d5ad; color: #17304a; padding-inline: max(1rem, calc((100vw - 1250px) / 2)); }
.school-site--classic .utility-actions button { border-color: #8c7852; }
.school-site--classic .utility-actions button[aria-pressed='true'] { background: #17304a; color: #fff; }
.school-site--classic .utility-divider { background: #8c7852; }
.school-site--classic .site-header { order: 1; min-height: 118px; padding: 1.4rem max(1rem, calc((100vw - 1250px) / 2)); background: #17304a; border: 0; }
.school-site--classic .brand { color: #fff; }
.school-site--classic .brand-mark { border-radius: 4px; border: 1px solid #bfa468; background: #e6d5ad; color: #17304a; height: 3.7rem; flex-basis: 3.7rem; }
.school-site--classic .brand-copy strong { font-size: clamp(1.4rem, 2.2vw, 2rem); }
.school-site--classic .brand-copy small { color: #d3dce2; }
.school-site--classic .brand-eyebrow { color: #e6cb8f; letter-spacing: .15em; }
.school-site--classic .header-note { padding: .55rem .8rem; border: 1px solid #688199; color: #e6d5ad; }
.school-site--classic .mobile-menu { color: #fff; }
.school-site--classic .site-nav { order: 2; display: flex; flex-direction: row; flex-wrap: nowrap; align-self: auto; justify-content: flex-start; gap: 0; overflow-x: auto; padding: 0 max(1rem, calc((100vw - 1250px) / 2)); border-bottom: 1px solid #d9dfdf; background: #fff; color: #17304a; }
.school-site--classic .nav-heading, .school-site--classic .nav-chevron { display: none; }
.school-site--classic .nav-link { width: auto; flex: 0 0 auto; border-radius: 0; padding: 1rem .9rem; font-size: .82rem; white-space: nowrap; }
.school-site--classic .nav-link:hover { background: #eef2f5; color: #17304a; }
.school-site--classic .nav-link[aria-current='page'] { color: #17304a; background: #eef2f5; box-shadow: inset 0 -4px #bc9958; }
.school-site--classic .nav-admin { flex: 0 0 auto; margin: 0 0 0 auto; padding: 1rem .5rem; color: #17304a !important; white-space: nowrap; }
.school-site--classic .site-main { order: 3; width: 100%; max-width: 1320px; margin: 0 auto; padding: 2rem 2rem 5rem; }
.school-site--classic .site-footer { order: 4; background: #142d47; color: #fff; border: 0; padding-inline: max(1rem, calc((100vw - 1250px) / 2)); }
.school-site--classic .site-footer :is(a, .footer-brand span, .footer-links) { color: #e0e9ec; }
.school-site--classic .hero { grid-template-columns: 1.4fr .6fr; min-height: 340px; background: #e8edf0; color: #17304a; border-radius: 0; }
.school-site--classic .hero-copy { padding: clamp(2rem, 4vw, 3.6rem); }
.school-site--classic .hero h1 { font-size: clamp(2.5rem, 4.2vw, 4rem); }
.school-site--classic .hero .eyebrow { color: #8c6528; }
.school-site--classic .hero p { color: #4b6071; }
.school-site--classic .hero-art { background: repeating-linear-gradient(90deg, #1a3852 0 1px, #17304a 1px 36px); }
.school-site--classic .hero-art::before { content: 'ШКОЛА'; display: grid; place-items: center; width: 75%; height: 56%; border: 2px solid #e6d5ad; border-radius: 0; box-shadow: 12px 12px 0 #e6d5ad2b; color: #e6d5ad; font: 700 clamp(2rem, 3vw, 2.8rem) Georgia, serif; letter-spacing: .12em; }
.school-site--classic .hero-art span { display: none; }
.school-site--classic .button-primary { background: #17304a; color: #fff; border-color: #17304a; border-radius: 0; }
.school-site--classic .button-primary:hover { background: #294d6e; }
.school-site--classic .button-secondary { color: #17304a; border-color: #17304a; border-radius: 0; }
.school-site--classic .button-secondary:hover { background: #d7e2e8; }
.school-site--classic .stat-grid { gap: 0; border: 1px solid var(--line); }
.school-site--classic .stat { border: 0; border-right: 1px solid var(--line); }.school-site--classic .stat:last-child { border: 0; }
.school-site--classic .feature-grid { gap: 0; border: 1px solid var(--line); }
.school-site--classic .feature-card { border: 0; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.school-site--classic .feature-card:hover { background: #f5f8fa; transform: none; }
.school-site--classic .section-heading { border-bottom: 2px solid #173a59; padding-bottom: 1.1rem; }
.school-site--classic .resource-card, .school-site--classic .panel, .school-site--classic .story-card { border-radius: 0; }
@media (max-width: 760px) {
  .school-site--classic .site-header { order: 1; padding: 1rem; }
  .school-site--classic .site-nav { position: fixed; z-index: 60; top: 0; bottom: 0; left: 0; width: min(310px, 85vw); display: flex; flex-direction: column; align-items: stretch; flex-wrap: nowrap; justify-content: start; overflow-y: auto; padding: 2rem .85rem; transform: translateX(-105%); border: 0; background: #17304a; color: #fff; }
  .school-site--classic .site-nav.is-open { transform: translateX(0); }
  .school-site--classic .nav-heading { display: flex; }.school-site--classic .nav-link { width: 100%; }.school-site--classic .nav-link:hover { background: #294d6e; color: #fff; }.school-site--classic .nav-link[aria-current='page'] { color: #17304a; background: #e6d5ad; }.school-site--classic .nav-admin { margin: auto 0 0; color: #e6d5ad !important; }
  .school-site--classic .hero { grid-template-columns: 1fr; min-height: 0; }.school-site--classic .hero-copy { padding: 2rem 1.5rem; }
  .school-site--classic .site-main { padding: 1.4rem 1rem 3rem; }.school-site--classic .stat-grid { gap: 0; }.school-site--classic .stat { border-right: 0; border-bottom: 1px solid var(--line); }
}
""",
    },
    "editorial": {
        "name": "Редакційний",
        "label": "Шкільний вісник · офіційні матеріали",
        "description": "Газетний дизайн із великим заголовком, теплим папером і колонками статей.",
        "css": r"""
/* School journal: paper, ink, generous type and newspaper rules. */
.school-site--editorial {
  --ink: #292920; --muted: #635f54; --canvas: #f3efe5; --surface: #fbf9f2;
  --line: #c8c0af; --accent: #9d3f2a; --accent-ink: #fff; --soft: #eee7d9;
  --radius: 0; --shadow: none;
  display: flex; flex-direction: column;
  font-family: Georgia, 'Times New Roman', serif;
}
.school-site--editorial .utility-bar { background: #292920; font-family: system-ui, sans-serif; }
.school-site--editorial .site-header { order: 1; justify-content: center; padding: 3.5rem 1rem 2.3rem; background: var(--canvas); border: 0; }
.school-site--editorial .brand { flex-direction: column; gap: .7rem; text-align: center; }
.school-site--editorial .brand-mark { width: 3rem; height: 3rem; flex-basis: 3rem; border: 1px solid #9d3f2a; background: transparent; color: #9d3f2a; }
.school-site--editorial .brand-copy strong { max-width: 850px; font-size: clamp(2.8rem, 6vw, 5.4rem); letter-spacing: -.055em; }
.school-site--editorial .brand-eyebrow { margin-bottom: 1rem; letter-spacing: .3em; }
.school-site--editorial .brand-copy small { margin-top: .8rem; font-size: .95rem; }
.school-site--editorial .header-note { display: none; }
.school-site--editorial .site-nav { order: 2; display: flex; flex-direction: row; flex-wrap: wrap; align-self: auto; justify-content: center; gap: 0; padding: 0 1rem; border-top: 4px double #292920; border-bottom: 4px double #292920; background: var(--canvas); color: #292920; }
.school-site--editorial .nav-heading, .school-site--editorial .nav-chevron, .school-site--editorial .nav-link svg { display: none; }
.school-site--editorial .nav-link { width: auto; border-radius: 0; padding: .9rem .8rem; font-family: Georgia, serif; font-size: .9rem; }
.school-site--editorial .nav-link:hover { background: #e7dfd0; color: #292920; }
.school-site--editorial .nav-link[aria-current='page'] { color: #9d3f2a; background: transparent; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: .45rem; }
.school-site--editorial .nav-admin { margin: 0 0 0 .5rem; padding: .9rem; color: #9d3f2a !important; }
.school-site--editorial .site-main { order: 3; width: 100%; max-width: 1360px; margin: 0 auto; padding: 3rem 2rem 5rem; }
.school-site--editorial .site-footer { order: 4; background: #292920; color: #fff; border-top: 4px solid #9d3f2a; }
.school-site--editorial .site-footer :is(a, .footer-brand span, .footer-links) { color: #e8e3d8; }
.school-site--editorial .hero { grid-template-columns: 1.15fr .85fr; min-height: 430px; border-top: 1px solid #292920; border-bottom: 1px solid #292920; background: transparent; color: #292920; }
.school-site--editorial .hero-copy { padding-left: 0; }.school-site--editorial .hero .eyebrow { color: #9d3f2a; }
.school-site--editorial .hero h1 { font-size: clamp(3.2rem, 6vw, 5.8rem); }.school-site--editorial .hero p { color: #635f54; }
.school-site--editorial .hero-art { border-left: 1px solid #292920; background: repeating-linear-gradient(-25deg, #e4dac5 0 3px, #f3efe5 3px 27px); }
.school-site--editorial .hero-art::before { width: 12rem; height: 12rem; border-color: #9d3f2a; box-shadow: 0 0 0 3rem #9d3f2a12, 0 0 0 6rem #9d3f2a0b; }
.school-site--editorial .hero-art span { background: #292920; color: #fff; border: 0; border-radius: 0; }
.school-site--editorial .button-primary { background: #9d3f2a; border-color: #9d3f2a; color: #fff; border-radius: 0; }
.school-site--editorial .button-secondary { color: #292920; border-color: #292920; border-radius: 0; }
.school-site--editorial .stat-grid { gap: 0; margin-top: 2rem; border-top: 4px solid #292920; border-bottom: 1px solid #292920; }
.school-site--editorial .stat { border: 0; border-right: 1px solid #c8c0af; background: transparent; padding: 1.5rem; }.school-site--editorial .stat:last-child { border: 0; }
.school-site--editorial .section-heading { border-bottom: 4px double #292920; padding-bottom: 1.2rem; }
.school-site--editorial .section-heading h2, .school-site--editorial .page-intro h1 { font-size: clamp(2.6rem, 4.5vw, 4.5rem); }
.school-site--editorial .feature-grid { gap: 0; }
.school-site--editorial .feature-card { border: 0; border-right: 1px solid #c8c0af; border-bottom: 1px solid #c8c0af; background: transparent; padding: 1.6rem; }
.school-site--editorial .feature-card:hover { transform: none; background: #eae1d2; }
.school-site--editorial .feature-card strong, .school-site--editorial .story-card h3 { font-size: 1.65rem; }
.school-site--editorial .story-card { border: 0; border-top: 1px solid #292920; background: transparent; }
.school-site--editorial .story-card > div:last-child { padding-left: 0; padding-right: 0; }
.school-site--editorial .story-card > img, .school-site--editorial .image-placeholder { filter: grayscale(1); }
.school-site--editorial .resource-card, .school-site--editorial .panel, .school-site--editorial .menu-card { background: transparent; }
@media (max-width: 760px) {
  .school-site--editorial .site-header { justify-content: space-between; padding: 1rem; }
  .school-site--editorial .brand { flex-direction: row; text-align: left; }.school-site--editorial .brand-mark { display: none; }
  .school-site--editorial .brand-copy strong { font-size: 1.4rem; }.school-site--editorial .brand-copy small { display: none; }
  .school-site--editorial .site-nav { position: fixed; z-index: 60; top: 0; bottom: 0; left: 0; width: min(310px, 85vw); display: flex; flex-direction: column; align-items: stretch; flex-wrap: nowrap; justify-content: start; overflow-y: auto; padding: 2rem .85rem; transform: translateX(-105%); background: var(--canvas); }
  .school-site--editorial .site-nav.is-open { transform: translateX(0); }.school-site--editorial .nav-heading { display: flex; }
  .school-site--editorial .nav-link { width: 100%; }.school-site--editorial .nav-admin { margin: auto 0 0; }
  .school-site--editorial .site-main { padding: 1.4rem 1rem 3rem; }.school-site--editorial .hero-copy { padding: 1rem 0; }
  .school-site--editorial .stat-grid { gap: 0; }.school-site--editorial .stat { border-right: 0; border-bottom: 1px solid #c8c0af; }
}
""",
    },
    "portal": {
        "name": "Портал",
        "label": "Цифровий портал закладу",
        "description": "Сучасна зелена панель із бічною навігацією, великим вступним блоком і плитками розділів.",
        "css": r"""
/* Contemporary workspace, distinct from the formal and journal layouts. */
.school-site--portal .site-nav { background: #17372c; }
.school-site--portal .site-header { min-height: 105px; }
.school-site--portal .hero { box-shadow: 0 20px 50px rgba(19, 60, 41, .12); }
.school-site--portal .stat:nth-child(1) { background: #eff4df; }
.school-site--portal .stat:nth-child(2) { background: #f7eddd; }
.school-site--portal .stat:nth-child(3) { background: #dcece7; }
.school-site--portal .feature-card:nth-child(3n+2) .feature-top { color: #a55b30; }
.school-site--portal .feature-card:nth-child(3n+3) .feature-top { color: #506c9e; }
.school-site--portal .page-intro { padding-top: 2rem; }
""",
    },
}
