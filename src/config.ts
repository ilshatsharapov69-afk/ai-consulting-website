// TODO: replace [YOUR BRAND] after brand-name research (see handoff notes)
export const SITE = {
  name: '[YOUR BRAND]',
  tagline: 'Find the money leaks in your HVAC business — with data, not guesswork.',
  description: 'We analyze your HVAC business — calls, estimates, scheduling, financials — and show you exactly where you\'re losing money. You get a clear report. No guesswork.',
  url: 'https://ai-consulting-website.sherlock753cc.workers.dev',
  author: '[YOUR BRAND]',
  calUrl: 'https://cal.com/YOUR_LINK',
  ctaText: 'Show Me Where I\'m Losing Money',
  ctaUrl: '/contact/',
  formApiKey: 'YOUR_WEB3FORMS_KEY',
  email: 'hello@example.com',
  social: {
    linkedin: '',
    youtube: 'https://youtube.com/@Ilshatai',
  },
} as const;

export const NAV_LINKS = [
  { href: '/services/', label: 'Services' },
  { href: '/blog/', label: 'Blog' },
  { href: '/resources/ai-readiness-quiz/', label: 'Free Quiz' },
  { href: '/about/', label: 'About' },
  { href: '/contact/', label: 'Contact' },
] as const;

export const SERVICES = [
  {
    title: 'AI Business Analysis',
    slug: 'ai-audit',
    price: '$2,500',
    priceNote: 'one-time',
    description: 'We plug AI into your business data — calls, estimates, scheduling, financials — and deliver a detailed report showing exactly where you\'re losing money and what to fix first.',
    icon: 'clipboard-check',
  },
  {
    title: 'Deep Dive Analysis',
    slug: 'roadmap',
    price: 'From $5,000',
    priceNote: 'project-based',
    description: 'A more comprehensive analysis with vendor evaluations, integration mapping, and a 90-day action plan built from your data.',
    icon: 'map',
  },
  {
    title: 'Ongoing Analytics',
    slug: 'retainer',
    price: 'From $2,000/mo',
    priceNote: 'ongoing',
    description: 'Monthly analysis of your business metrics. We track what\'s improving, what\'s not, and give you updated recommendations.',
    icon: 'phone',
  },
] as const;
