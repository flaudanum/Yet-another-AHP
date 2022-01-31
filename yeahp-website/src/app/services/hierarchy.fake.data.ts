export const hierarchyChooseAirline: Hierarchy = {
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
};
