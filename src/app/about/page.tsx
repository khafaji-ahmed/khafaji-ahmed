'use client';

import { useEffect } from 'react';
import Image from 'next/image';
import Layout from '../../components/Layout';

export default function About() {
  useEffect(() => {
    // Animate about hero
    const aboutHero = document.querySelectorAll('.about-hero');
    aboutHero.forEach((hero, index) => {
      setTimeout(() => {
        hero.classList.add('animate');
      }, index * 300 * 3); // delayMultiplier = 3 like original
    });

    // Animate tiles
    const tileElements = document.querySelectorAll('.tile');
    tileElements.forEach((tile, index) => {
      setTimeout(() => {
        tile.classList.add('animate');
      }, (index * 300) * 2); // delayMultiplier = 2 like original
    });
  }, []);

  return (
    <Layout>
      <section className="hero">
        <h1 className="about-hero">
          About Me
        </h1>
      </section>

      <section className="tiles-section">
        <div className="tiles">
          {/* Image Tile - tile-3 */}
          <div className="tile tile-3 image">
            <Image src="/setup.png" alt="Setup" className="Setup" width={400} height={300} unoptimized /> 
            <Image src="/selfie.png" alt="Selfie" className="Selfie" width={200} height={200} unoptimized />
          </div>

          {/* Intro Tile */}
          <div className="tile intro">
            <h1 className="about-hi">Hey, I&apos;m Ahmed 👋🏻</h1>
            <h3 className="occupation">Founder & Lead Engineer</h3>
            <p style={{ fontSize: '14px', marginTop: '8px', color: '#666' }}>Toronto, Canada</p>
          </div>

          {/* Experience Tile */}
          <div className="tile experience">
            <h1>Experience</h1>
            <ul className="experience-list">
              <li><strong>Founder & Lead Engineer</strong> - CAYDE SERVICES INC. (2022 - Present)</li>
              <li><strong>Senior Full-Stack Developer</strong> - Wood Manufacturer (Feb 2024 - Present)</li>
              <li><strong>Senior Full-Stack Developer & Team Lead</strong> - Lightring AI (Nov 2022 - Present)</li>
            </ul>
          </div>

          {/* About Me Tile - tile-3 */}
          <div className="tile tile-3">
            <h1>About Me</h1>
            <p className="about-me-description">
              I&apos;m a passionate Software Engineering student at York University and founder of CAYDE SERVICES INC., a Canadian software company delivering government and campus-scale solutions. As a Senior Full-Stack Developer and Team Lead, I&apos;ve built scalable applications including yuMeet (a university social platform with 55k+ users), enterprise billing systems processing 100k+ daily transactions, and government e-visa platforms. I specialize in React, Next.js, Node.js, PostgreSQL, and modern development practices including CI/CD and DevOps.
            </p>
          </div>
        </div>
      </section>
    </Layout>
  );
}