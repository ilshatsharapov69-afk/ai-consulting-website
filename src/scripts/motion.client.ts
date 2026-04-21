import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import SplitType from 'split-type';
import VanillaTilt from 'vanilla-tilt';

type TiltEl = HTMLElement & { vanillaTilt?: { destroy: () => void } };

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isCoarsePointer = window.matchMedia('(pointer: coarse)').matches;

gsap.registerPlugin(ScrollTrigger);

// ---- SplitText-style reveal on H2 ----
const SPLIT_SELECTORS = [
  '.sf-heading',
  '.sample-section-heading',
  '.process-heading',
  '.ba-heading',
  '.faq-heading',
  '.final-heading',
];

function splitAndReveal(el: HTMLElement): void {
  if (reduceMotion) return;
  const split = new SplitType(el, { types: 'chars, words' });
  if (!split.chars) return;

  gsap.set(split.chars, {
    opacity: 0,
    y: 40,
    rotateX: -40,
    transformPerspective: 600,
  });

  gsap.to(split.chars, {
    opacity: 1,
    y: 0,
    rotateX: 0,
    duration: 0.7,
    ease: 'power3.out',
    stagger: 0.025,
    scrollTrigger: {
      trigger: el,
      start: 'top 82%',
      once: true,
    },
  });
}

SPLIT_SELECTORS.forEach((sel) => {
  document.querySelectorAll<HTMLElement>(sel).forEach(splitAndReveal);
});

// ---- 3D-entrance for pain-quote cards & phase cards ----
function stagger3D(selector: string, trigger: string | HTMLElement): void {
  const els = document.querySelectorAll<HTMLElement>(selector);
  if (!els.length || reduceMotion) return;

  gsap.set(els, {
    opacity: 0,
    y: 50,
    rotateX: 10,
    transformPerspective: 800,
  });

  gsap.to(els, {
    opacity: 1,
    y: 0,
    rotateX: 0,
    duration: 0.8,
    ease: 'power2.out',
    stagger: 0.12,
    scrollTrigger: {
      trigger,
      start: 'top 78%',
      once: true,
    },
  });
}

stagger3D('.sf-card', '.sf-wall');
stagger3D('.phase', '.process-phases');

// ---- Tilt on cards (desktop only) ----
if (!isCoarsePointer && !reduceMotion) {
  const tiltTargets = document.querySelectorAll<TiltEl>('.sf-card, .phase, .prac-portrait-frame');
  tiltTargets.forEach((el) => {
    VanillaTilt.init(el, {
      max: 5,
      speed: 400,
      glare: true,
      'max-glare': 0.12,
      scale: 1.015,
      reset: true,
    });
  });
}

// ---- SignalDivider draw-on-scroll (add .is-visible when in view) ----
const signalIO = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        signalIO.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.3 }
);

document.querySelectorAll('.signal-divider').forEach((el) => signalIO.observe(el));

// ---- Phase icons — add --phase-delay based on index of their parent .phase ----
document.querySelectorAll<HTMLElement>('.phase').forEach((phase, idx) => {
  const icon = phase.querySelector<HTMLElement>('.phase-icon');
  if (icon) icon.style.setProperty('--phase-delay', String(idx));
});

// ---- Load img-comparison-slider only if Before/After section exists ----
if (document.querySelector('img-comparison-slider')) {
  import('img-comparison-slider');
}

// ---- Scroll progress bar (thin amber line atop header) ----
const progressBar = document.querySelector<HTMLElement>('.scroll-progress');
if (progressBar && !reduceMotion) {
  let rafBusy = false;
  const updateProgress = () => {
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const current = window.scrollY;
    const pct = total > 0 ? Math.min(1, Math.max(0, current / total)) : 0;
    progressBar.style.transform = `scaleX(${pct})`;
    rafBusy = false;
  };
  const onScroll = () => {
    if (rafBusy) return;
    rafBusy = true;
    requestAnimationFrame(updateProgress);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  updateProgress();
}

// Refresh ScrollTrigger after everything is wired (fonts may shift layout)
window.addEventListener('load', () => {
  ScrollTrigger.refresh();
});
