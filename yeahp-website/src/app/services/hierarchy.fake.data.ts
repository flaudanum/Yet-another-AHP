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
    ['goal', 'Service on board'],
    ['goal', 'Reliability'],
    ['goal', 'Pricing'],
    ['Service on board', 'Snack'],
    ['Service on board', 'Crew'],
    ['Pricing', 'Tickets'],
    ['Pricing', 'Additional services'],
    ['Pricing', 'Discounts with partner companies'],
  ],
};

/* export const hierarchyChooseAirline: Hierarchy = {
  goal: 'Choose an airline company',
  criteria: [
    {
      title: 'Service on board',
      subCriteria: [
        {
          title: 'Snack',
          subCriteria: [],
        },
        {
          title: 'Crew',
          subCriteria: [],
        },
      ],
    },
    {
      title: 'Reliability',
      subCriteria: [],
    },
    {
      title: 'Pricing',
      subCriteria: [
        {
          title: 'Tickets',
          subCriteria: [],
        },
        {
          title: 'Additional services',
          subCriteria: [],
        },
        {
          title: 'Discounts with partner companies',
          subCriteria: [],
        },
      ],
    },
  ],
}; */
