import { Hierarchy } from '../models/hierarchy.model';

export const hierarchyChooseAirline: Hierarchy = {
  goal: 'Choose an airline company',
  criteria: [
    'Service on board',
    'Snack',
    'Crew',
    'Reliability',
    'Pricing',
    'Tickets',
    'Additional services',
    'Discounts with partner companies',
  ],
  dependencies: [
    ['Choose an airline company', 'Service on board'],
    ['Choose an airline company', 'Reliability'],
    ['Choose an airline company', 'Pricing'],
    ['Service on board', 'Snack'],
    ['Service on board', 'Crew'],
    ['Pricing', 'Tickets'],
    ['Pricing', 'Additional services'],
    ['Pricing', 'Discounts with partner companies'],
  ],
};
