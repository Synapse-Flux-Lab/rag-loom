/**
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  docsSidebar: [
    'Introduction',
    'overview',
    'roadmap',
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/requirements',
        'getting-started/quickstart',
        'getting-started/structure',
        'getting-started/infrastructure',
      ],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: [
        'architecture/system-design',
      ],
    },
    {
      type: 'category',
      label: 'API',
      items: [
        'api/rest-api',
        'api/script-examples',
      ],
    },
    {
      type: 'category',
      label: 'Operations',
      items: [
        'operations/scaling',
        'operations/security',
        'operations/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Integrations',
      items: [
        'integrations/ollama',
      ],
    },
    'contact-us',
  ],
};

module.exports = sidebars;
