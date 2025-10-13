// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {
  themes: { github: lightCodeTheme, dracula: darkCodeTheme },
} = require('prism-react-renderer');

const config = {
  title: 'RAG Loom Docs',
  tagline: 'Documentation hub for the RAG Loom project',
  favicon: 'img/logo.svg',

  url: 'https://ragloom.pages.dev/',
  baseUrl: '/',
  organizationName: 'Synapse-Flux-Lab',
  projectName: 'rag-loom-docs',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */ ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/Synapse-Flux-Lab/rag-loom/tree/main/docs',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        searchResultLimits: 8,
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */ ({
      navbar: {
        title: 'RAG Loom',
        logo: {
          alt: 'RAG Loom Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/Synapse-Flux-Lab/rag-loom',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/Introduction',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Issues',
                href: 'https://github.com/Synapse-Flux-Lab/rag-loom/issues',
              },
            ],
          },
          {
            title: 'SynapseFluxLab',
            items: [
              {
                label: 'Visit Parent Studio',
                href: 'https://synapsefluxlab.pages.dev/',
              },
            ],
          },
        ],
        copyright: `© ${new Date().getFullYear()} Synapse-Flux-Lab. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
