export const SITE = {
  name: 'Setpoint Audit',
  tagline: 'A data-first audit for US small businesses — I read what you already have and show you the leaks.',
  description: 'Data-to-Dollars Audit — $2,500 fixed, 5 days. I read your QuickBooks, CRM and calendar, then tell you where your small business is losing money. For US businesses doing $500K–$10M.',
  url: 'https://setpointaudit.com',
  author: 'Setpoint Audit',
  calUrl: 'https://cal.com/ilshatai/audit',
  ctaText: 'Book Your Free Diagnostic',
  ctaUrl: '/contact/',
  formApiKey: '598ae70c-fada-44c2-b48b-0b3b777f4e10',
  email: 'ilshat@setpointaudit.com',
  price: '$2,500',
  currency: 'USD',
  priceNumeric: '2500',
  deliveryDays: 5,
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
    description: 'We plug AI into your business data — CRM exports, spreadsheets, POS, scheduling, invoices — and deliver a report showing exactly where you\'re losing money and what to fix first.',
    icon: 'clipboard-check',
  },
  {
    title: 'Deep Dive Analysis',
    slug: 'roadmap',
    price: 'From $5,000',
    priceNote: 'project-based',
    description: 'A comprehensive analysis with vendor evaluations, integration mapping, and a 90-day action plan — built from your own data, tailored to your industry.',
    icon: 'map',
  },
  {
    title: 'Ongoing Analytics',
    slug: 'retainer',
    price: 'From $2,000/mo',
    priceNote: 'ongoing',
    description: 'Monthly analysis of your business metrics. We track what\'s improving, what\'s not, and give you updated recommendations as your data evolves.',
    icon: 'phone',
  },
] as const;
