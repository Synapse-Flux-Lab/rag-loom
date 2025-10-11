import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

const Hero = () => (
  <header className={clsx('hero hero--primary', styles.heroBanner)}>
    <div className="container">
      <h1 className="hero__title">RAG Loom Documentation</h1>
      <p className="hero__subtitle">
        Learn how to develop, deploy, and operate the RAG Loom microservice.
      </p>
      <div className={styles.buttons}>
        <Link
          className="button button--secondary button--lg"
          to="/docs/Introduction"
        >
          Start Reading
        </Link>
      </div>
    </div>
  </header>
);

export default function Home() {
  return (
    <Layout>
      <Hero />
      <main className={styles.mainContent}>
        <section className="container">
          <div className="row">
            <div className="col col--4">
              <h2>Overview</h2>
              <p>Understand the architecture and capabilities of RAG Loom.</p>
            </div>
            <div className="col col--4">
              <h2>Operate</h2>
              <p>Spin up the service locally or in production-ready environments.</p>
            </div>
            <div className="col col--4">
              <h2>Extend</h2>
              <p>Adopt best practices when integrating or customizing the platform.</p>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
